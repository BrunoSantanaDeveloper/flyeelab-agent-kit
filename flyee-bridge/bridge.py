#!/usr/bin/env python3
"""flyee-bridge — Connects the .agent runtime to the Flyee Platform via structured events.

Usage:
    # Test connectivity
    python bridge.py --test

    # Emit an event
    python bridge.py emit "dev.task_completed" '{"task": "T1.1", "files": ["sdk.ts"]}'

    # Configure interactively (with project creation + doc registration)
    python bridge.py --setup

    # List projects on the platform
    python bridge.py --list-projects

    # Scan and register local docs
    python bridge.py --register-docs
"""

import glob
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Union

# Resolve config path relative to project root
BRIDGE_DIR = Path(__file__).parent
PROJECT_ROOT = BRIDGE_DIR.parent.parent
CONFIG_PATH = PROJECT_ROOT / "flyee.json"
FALLBACK_PATH = BRIDGE_DIR / "events.jsonl"

PROD_API_URL = "https://flyee-api.flyeelab.com"

DEFAULT_CONFIG = {
    "api_url": PROD_API_URL,
    "project_id": "",
    "api_key": "",
    "enabled": False,
    "opted_out": False,
    "fallback_file": str(FALLBACK_PATH),
}


def load_config() -> dict:
    """Load bridge config, creating default if absent."""
    if not CONFIG_PATH.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_PATH) as f:
        return json.load(f)


def save_config(config: dict) -> None:
    """Persist config to disk."""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def is_configured(config: dict) -> bool:
    """Check if bridge is properly configured for event emission."""
    if config.get("opted_out"):
        return False
    return bool(
        config.get("enabled")
        and config.get("api_key")
        and config.get("project_id")
    )


# ---------------------------------------------------------------------------
# API Helpers — Project & Document management
# ---------------------------------------------------------------------------

def api_request(
    method: str,
    url: str,
    api_key: str,
    data: Optional[dict] = None,
    timeout: int = 15,
) -> Any:
    """Make an authenticated HTTP request to the Flyee API. Returns parsed JSON or None."""
    import urllib.request
    import urllib.error

    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
        "X-Bridge-API-Key": api_key,
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            pass
        print(f"❌ API error {e.code}: {e.reason}")
        if detail:
            print(f"   Detail: {detail}")
        return None
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return None


def list_projects(api_url: str, api_key: str) -> Optional[list]:
    """List all projects on the Flyee Platform."""
    url = f"{api_url.rstrip('/')}/flyee/projects/"
    return api_request("GET", url, api_key)


def create_project(
    api_url: str, api_key: str, name: str, description: str = ""
) -> Optional[dict]:
    """Create a new project on the Flyee Platform. Returns project dict with 'id'."""
    url = f"{api_url.rstrip('/')}/flyee/projects/"
    return api_request("POST", url, api_key, {
        "name": name,
        "description": description or f"Project created via flyee-bridge on {datetime.now().strftime('%Y-%m-%d')}",
        "status": "active",
    })


def _detect_doc_type(filepath: str) -> tuple:
    """Detect document type from filepath. Returns (doc_type, title)."""
    name = os.path.basename(filepath)
    name_no_ext = os.path.splitext(name)[0]

    if re.match(r"PRD-", name, re.IGNORECASE):
        return "prd", name_no_ext.replace("PRD-", "PRD — ")
    if re.match(r"TDD-", name, re.IGNORECASE):
        return "tdd", name_no_ext.replace("TDD-", "TDD — ")
    if "BREAKDOWN" in name.upper():
        return "other", "Task Breakdown"
    if "PROJECT-PROGRESS" in name.upper():
        return "other", "Project Progress"
    if "OKR" in name.upper():
        return "okr", name_no_ext
    return "other", name_no_ext


def scan_docs(project_root: Optional[str] = None) -> list:
    """Scan docs/ for known document files. Returns list of {path, type, title}."""
    if project_root is None:
        # Walk up from bridge dir to find project root
        project_root = str(BRIDGE_DIR.parent.parent)

    docs_dir = os.path.join(project_root, "docs")
    if not os.path.isdir(docs_dir):
        return []

    patterns = [
        os.path.join(docs_dir, "PRD-*.md"),
        os.path.join(docs_dir, "design", "TDD-*.md"),
        os.path.join(docs_dir, "BREAKDOWN-*.md"),
        os.path.join(docs_dir, "PROJECT-PROGRESS.md"),
    ]

    found = []
    for pattern in patterns:
        for filepath in glob.glob(pattern):
            doc_type, title = _detect_doc_type(filepath)
            found.append({"path": filepath, "type": doc_type, "title": title})

    return found


def register_documents(
    api_url: str, api_key: str, project_id: str, docs: list
) -> list:
    """Register local documents on the Flyee Platform. Returns list of results."""
    MAX_CONTENT_SIZE = 500_000  # 500KB max per document
    results = []
    url = f"{api_url.rstrip('/')}/flyee/projects/{project_id}/documents"

    for doc in docs:
        try:
            with open(doc["path"], "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            results.append({**doc, "status": "error", "error": str(e)})
            continue

        if len(content) > MAX_CONTENT_SIZE:
            content = content[:MAX_CONTENT_SIZE] + "\n\n[... truncated at 500KB ...]"

        resp = api_request("POST", url, api_key, {
            "title": doc["title"],
            "type": doc["type"],
            "content": content,
        }, timeout=30)

        if resp:
            results.append({**doc, "status": "registered", "id": resp.get("id")})
        else:
            results.append({**doc, "status": "failed"})

    return results


# ---------------------------------------------------------------------------
# Task Management — Create, update, list, get tasks on Flyee
# ---------------------------------------------------------------------------

def create_task(
    api_url: str,
    api_key: str,
    project_id: str,
    task_type: str = "implement_feature",
    name: str = "",
    description: str = "",
    priority: str = "normal",
    source: str = "system",
    parent_task_id: Optional[str] = None,
    meta: Optional[dict] = None,
) -> Any:
    """Create a task on the Flyee Platform.

    Args:
        task_type: One of create_prd, create_tdd, breakdown_tasks,
                   implement_feature, run_tests, generate_docs,
                   document_requirements, document_architecture,
                   design_system, implement_tests, verify_quality, generic
        name: Human-readable task name (stored in input.name)
        description: Task description (stored in input.description)
        priority: One of low, normal, high, critical
        source: One of api, slack, ui, system
        meta: Additional metadata dict
    """
    url = f"{api_url.rstrip('/')}/flyee/projects/{project_id}/tasks"
    payload = {
        "type": task_type,
        "priority": priority,
        "source": source,
        "input": {
            "name": name,
            "description": description,
        },
        "meta": meta or {},
        "max_retries": 0,
        "timeout_seconds": 3600,
    }
    if parent_task_id:
        payload["parent_task_id"] = parent_task_id
    return api_request("POST", url, api_key, payload)


def update_task(
    api_url: str,
    api_key: str,
    task_id: str,
    status: Optional[str] = None,
    result_status: Optional[str] = None,
    output: Optional[dict] = None,
    metrics: Optional[dict] = None,
    meta: Optional[dict] = None,
) -> Any:
    """Update a task on the Flyee Platform.

    Args:
        status: One of pending, queued, running, completed, failed, cancelled
        result_status: One of success, partial, failed, error
        output: Task output data (summary, files changed, etc.)
        metrics: Execution metrics (time_spent, etc.)
        meta: Additional metadata updates
    """
    url = f"{api_url.rstrip('/')}/flyee/tasks/{task_id}"
    payload: dict = {}
    if status:
        payload["status"] = status
    if result_status:
        payload["result_status"] = result_status
    if output:
        payload["output"] = output
    if metrics:
        payload["metrics"] = metrics
    if meta:
        payload["meta"] = meta
    return api_request("PUT", url, api_key, payload)


def list_tasks(
    api_url: str,
    api_key: str,
    project_id: str,
    status: Optional[str] = None,
) -> Any:
    """List tasks for a project on the Flyee Platform."""
    url = f"{api_url.rstrip('/')}/flyee/projects/{project_id}/tasks"
    if status:
        url += f"?status={status}"
    return api_request("GET", url, api_key)


def get_task(api_url: str, api_key: str, task_id: str) -> Any:
    """Get a single task by ID from the Flyee Platform."""
    url = f"{api_url.rstrip('/')}/flyee/tasks/{task_id}"
    return api_request("GET", url, api_key)


def create_okr(
    api_url: str,
    api_key: str,
    project_id: str,
    objective: str,
    key_results: Optional[dict] = None,
    period: Optional[str] = None,
    owner: Optional[str] = None,
    status: str = "active",
) -> Any:
    """Create an OKR on the Flyee Platform.

    Args:
        objective: The objective statement (e.g. 'Launch MVP by Q2 2026')
        key_results: Dict of key results (e.g. {'kr1': '100 beta users', 'kr2': 'NPS > 40'})
        period: Time period (e.g. 'Q1 2026')
        owner: OKR owner name
        status: One of draft, active, completed, cancelled
    """
    url = f"{api_url.rstrip('/')}/flyee/projects/{project_id}/okrs"
    payload = {
        "objective": objective,
        "status": status,
    }
    if key_results:
        payload["key_results"] = key_results
    if period:
        payload["period"] = period
    if owner:
        payload["owner"] = owner
    return api_request("POST", url, api_key, payload)


def list_okrs(
    api_url: str,
    api_key: str,
    project_id: str,
) -> Any:
    """List OKRs for a project on the Flyee Platform."""
    url = f"{api_url.rstrip('/')}/flyee/projects/{project_id}/okrs"
    return api_request("GET", url, api_key)


def create_decision(
    api_url: str,
    api_key: str,
    project_id: str,
    decision: str,
    actor: str = "agent",
    reason: Optional[str] = None,
    impact: Optional[str] = None,
    task_id: Optional[str] = None,
) -> Any:
    """Record a governance decision on the Flyee Platform.

    Args:
        decision: The decision taken (e.g. 'Use Next.js App Router')
        actor: Who made it (e.g. 'agent', 'user', 'system')
        reason: Rationale for the decision
        impact: Expected impact of the decision
        task_id: Related task ID, if any
    """
    url = f"{api_url.rstrip('/')}/flyee/projects/{project_id}/decisions"
    payload: dict = {
        "actor": actor,
        "decision": decision,
    }
    if reason:
        payload["reason"] = reason
    if impact:
        payload["impact"] = impact
    if task_id:
        payload["task_id"] = task_id
    return api_request("POST", url, api_key, payload)


def list_decisions(
    api_url: str,
    api_key: str,
    project_id: str,
) -> Any:
    """List decisions for a project on the Flyee Platform."""
    url = f"{api_url.rstrip('/')}/flyee/projects/{project_id}/decisions"
    return api_request("GET", url, api_key)


# ---------------------------------------------------------------------------
# API Helpers — Knowledge Hub (collections linked to a project)
# ---------------------------------------------------------------------------

def list_collections(
    api_url: str,
    api_key: str,
    project_id: str,
) -> Any:
    """List Airweave collections linked to a project via Knowledge Hub."""
    url = f"{api_url.rstrip('/')}/flyee/projects/{project_id}/collections"
    result = api_request("GET", url, api_key)
    # Distinguish None (API error) from [] (no collections)
    return result


def search_collections(
    api_url: str,
    api_key: str,
    project_id: str,
    query: str,
    limit: int = 5,
    min_score: float = 0.01,
) -> dict:
    """Search all linked collections for context relevant to a query.

    1. Lists collections linked to the project.
    2. Searches each collection via Airweave Search API.
    3. Returns aggregated results filtered by min_score.
    """
    collections = list_collections(api_url, api_key, project_id)

    # None means API error (auth, network, server error)
    if collections is None:
        return {
            "status": "error",
            "message": "Failed to list collections — check API key permissions and project_id",
            "collections_searched": 0,
            "results": [],
        }

    # Empty list means no collections linked to this project
    if not collections:
        return {
            "status": "ok",
            "message": "No collections linked to this project. Link collections via Knowledge Hub.",
            "collections_searched": 0,
            "results": [],
        }

    all_results = []
    errors = []
    for col in collections:
        readable_id = col.get("collection_readable_id")
        col_name = col.get("collection_name", "")
        if not readable_id:
            continue

        search_url = f"{api_url.rstrip('/')}/collections/{readable_id}/search"
        # Search with higher limit to capture all chunks of matching documents
        search_body = {
            "query": query,
            "limit": 50,
            "strategy": "hybrid",
        }
        # Increased timeout to 180s because backend uses rate-limited embedding APIs.
        # Backend handles 429s with exponential backoff, which may take ~1-2 minutes.
        resp = api_request("POST", search_url, api_key, search_body, timeout=180)
        if not resp:
            errors.append(f"Search failed for collection '{col_name}' ({readable_id})")
            continue

        # Group chunks by original document (original_entity_id) and reconstruct
        # full documents by concatenating chunks sorted by chunk_index.
        doc_groups = {}
        for hit in resp.get("results", []):
            score = hit.get("score", 0)
            if score < min_score:
                continue
            sys_meta = hit.get("system_metadata", {})
            src_fields = hit.get("source_fields", {})
            entity_id = sys_meta.get("original_entity_id", hit.get("entity_id", ""))
            chunk_idx = sys_meta.get("chunk_index", 0)
            content = hit.get("textual_representation") or hit.get("md_content") or ""

            if entity_id not in doc_groups:
                doc_groups[entity_id] = {
                    "title": hit.get("name", src_fields.get("title", entity_id)),
                    "source": sys_meta.get("source_name", hit.get("source_name", "")),
                    "best_score": score,
                    "chunks": [],
                }
            doc = doc_groups[entity_id]
            doc["best_score"] = max(doc["best_score"], score)
            doc["chunks"].append((chunk_idx, content))

        # Reconstruct full documents from sorted chunks
        matches = []
        for entity_id, doc in doc_groups.items():
            doc["chunks"].sort(key=lambda c: c[0])
            full_content = "\n".join(chunk[1] for chunk in doc["chunks"])
            matches.append({
                "title": doc["title"],
                "content": full_content,
                "score": round(doc["best_score"], 3),
                "source": doc["source"],
                "chunks_count": len(doc["chunks"]),
            })
        # Sort by best score descending
        matches.sort(key=lambda m: m["score"], reverse=True)
        if matches:
            all_results.append({
                "collection": col_name,
                "readable_id": readable_id,
                "matches": matches[:limit],
            })

    result = {
        "status": "ok",
        "collections_searched": len(collections),
        "collections_found": [c.get("collection_name", "") for c in collections],
        "results": all_results,
    }
    if errors:
        result["warnings"] = errors
    return result


def _suggest_project_name() -> str:
    """Suggest a project name from the current directory or PROJECT-PROGRESS.md."""
    project_root = str(BRIDGE_DIR.parent.parent)

    # Try to extract from PROJECT-PROGRESS.md
    progress_file = os.path.join(project_root, "docs", "PROJECT-PROGRESS.md")
    if os.path.exists(progress_file):
        try:
            with open(progress_file, "r") as f:
                for line in f:
                    match = re.search(r"\|\s*Projeto\s*\|\s*(.+?)\s*\|", line)
                    if match:
                        return match.group(1).strip()
        except Exception:
            pass

    # Fallback to directory name
    return os.path.basename(project_root).replace("-", " ").replace("_", " ").title()


# ---------------------------------------------------------------------------
# Interactive Setup
# ---------------------------------------------------------------------------

def setup_interactive() -> dict:
    """Interactive setup with project selection/creation and doc registration."""
    config = load_config()

    print("\n🔗 Flyee Bridge — Setup")
    print("=" * 40)
    print()
    print("O flyee-bridge conecta este projeto à plataforma Flyee,")
    print("enviando eventos de desenvolvimento (tasks, testes, deploys)")
    print("e registrando documentação automaticamente.")
    print()

    choice = input("Deseja integrar com a plataforma Flyee? (s/n): ").strip().lower()

    if choice in ("n", "nao", "não", "no"):
        config["opted_out"] = True
        config["enabled"] = False
        save_config(config)
        print("\n✅ Integração desabilitada. Eventos NÃO serão enviados.")
        print("   Para reconfigurar: python .agent/flyee-bridge/bridge.py --setup")
        return config

    # --- Step 1: Authentication ---
    print("\n📡 Passo 1/4 — Autenticação")
    print("-" * 30)

    config["api_url"] = PROD_API_URL
    print(f"   API URL: {PROD_API_URL} (padrão prod)")

    print()
    print("📋 Obtenha sua API Key na plataforma Flyee:")
    print("   Settings → API Keys → Generate Key")
    print()
    api_key = input("API Key: ").strip()
    if not api_key:
        print("❌ API Key é obrigatória.")
        return config
    config["api_key"] = api_key

    # --- Step 2: Project Selection/Creation ---
    print("\n📂 Passo 2/4 — Selecionar ou Criar Projeto")
    print("-" * 30)

    projects = list_projects(config["api_url"], api_key)

    if projects is None:
        print("⚠️  Não foi possível listar projetos. Verificar API URL e API Key.")
        project_id = input("\nProject ID (UUID manual, ou Enter para criar novo): ").strip()
        if not project_id:
            project_id = _create_project_interactive(config["api_url"], api_key)
            if not project_id:
                return config
        config["project_id"] = project_id
    elif len(projects) == 0:
        print("Nenhum projeto encontrado na plataforma.")
        project_id = _create_project_interactive(config["api_url"], api_key)
        if not project_id:
            return config
        config["project_id"] = project_id
    else:
        print(f"\n{'#':<4} {'Projeto':<30} {'Status':<12}")
        print("-" * 50)
        for i, p in enumerate(projects, 1):
            name = p.get("name", "Sem nome")
            status = p.get("status", "?")
            print(f"{i:<4} {name:<30} {status:<12}")
        print(f"{len(projects)+1:<4} {'➕ Criar novo projeto':<30}")

        sel = input(f"\nSelecione [1-{len(projects)+1}]: ").strip()
        try:
            idx = int(sel)
            if 1 <= idx <= len(projects):
                config["project_id"] = str(projects[idx - 1]["id"])
                print(f"✅ Projeto selecionado: {projects[idx - 1]['name']}")
            else:
                project_id = _create_project_interactive(config["api_url"], api_key)
                if not project_id:
                    return config
                config["project_id"] = project_id
        except (ValueError, IndexError):
            project_id = _create_project_interactive(config["api_url"], api_key)
            if not project_id:
                return config
            config["project_id"] = project_id

    # --- Step 3: Document Registration ---
    print("\n📄 Passo 3/4 — Registrar Documentação Existente")
    print("-" * 30)

    docs = scan_docs()
    if docs:
        print(f"Encontrados {len(docs)} documento(s) em docs/:")
        for d in docs:
            print(f"   • {os.path.basename(d['path'])} ({d['type']})")
        print()
        reg = input("Registrar estes documentos no Flyee? (s/n) [s]: ").strip().lower()
        if reg not in ("n", "nao", "não", "no"):
            results = register_documents(
                config["api_url"], api_key, config["project_id"], docs
            )
            print()
            for r in results:
                icon = "✅" if r["status"] == "registered" else "❌"
                print(f"   {icon} {r['title']} — {r['status']}")
        else:
            print("⏭️  Registro de documentos ignorado.")
    else:
        print("Nenhum documento encontrado em docs/.")
        print("Documentos serão registrados automaticamente quando criados.")

    # --- Step 4: Save Config ---
    print("\n💾 Passo 4/4 — Salvar Configuração")
    print("-" * 30)

    config["enabled"] = True
    config["opted_out"] = False
    save_config(config)

    print("\n✅ Flyee Bridge configurado com sucesso!")
    print(f"   API:     {config['api_url']}")
    print(f"   Project: {config['project_id']}")
    print("   Eventos serão enviados automaticamente pelos workflows.")
    return config


def _create_project_interactive(api_url: str, api_key: str) -> Optional[str]:
    """Interactive project creation. Returns project_id or None."""
    suggested = _suggest_project_name()
    name = input(f"Nome do projeto [{suggested}]: ").strip()
    name = name or suggested

    desc = input("Descrição (opcional): ").strip()

    print(f"\nCriando projeto '{name}'...")
    project = create_project(api_url, api_key, name, desc)
    if project:
        pid = str(project["id"])
        print(f"✅ Projeto criado: {name} (ID: {pid})")
        return pid
    else:
        print("❌ Falha ao criar projeto.")
        return None


def emit_event(
    event_type: str,
    payload: Optional[dict] = None,
    config: Optional[dict] = None,
) -> bool:
    """Emit a structured event to the Flyee Platform.

    Returns True if event was sent or queued, False if bridge is disabled.
    """
    if config is None:
        config = load_config()

    # Skip silently if opted out or not configured
    if config.get("opted_out") or not is_configured(config):
        return False

    event_data = {
        "project_id": config["project_id"],
        "entity_type": event_type.split(".")[0],
        "event_type": event_type,
        "payload": {
            **(payload or {}),
            "_timestamp": datetime.now(timezone.utc).isoformat(),
            "_agent_runtime": ".agent",
        },
        "source": "flyee-bridge",
    }

    # Try sending via HTTP
    url = f"{config['api_url'].rstrip('/')}/flyee/events/ingest"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": config["api_key"],
        "X-Bridge-API-Key": config["api_key"],
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            import urllib.request

            req = urllib.request.Request(
                url,
                data=json.dumps(event_data).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status in (200, 201):
                    return True
        except Exception as e:
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                time.sleep(wait)
            else:
                # Fallback: write to local file
                _fallback_write(event_data, config)
                return True

    return False


def _fallback_write(event_data: dict, config: dict) -> None:
    """Write event to local JSONL file as fallback."""
    fallback = config.get("fallback_file", str(FALLBACK_PATH))
    with open(fallback, "a") as f:
        f.write(json.dumps(event_data) + "\n")


def test_connection(config: dict) -> None:
    """Send a test event to verify connectivity."""
    print(f"\n🔗 Testing connection to {config['api_url']}...")

    if not is_configured(config):
        print("❌ Bridge not configured. Run: python bridge.py --setup")
        return

    success = emit_event(
        "dev.test_run",
        {"test": True, "message": "flyee-bridge connectivity test"},
        config,
    )

    if success:
        print("✅ Test event sent successfully!")
    else:
        print("❌ Failed to send test event. Check API URL and API key.")


def main():
    args = sys.argv[1:]

    if not args or "--help" in args:
        print(__doc__)
        return

    if "--setup" in args:
        setup_interactive()
        return

    config = load_config()

    # First-run detection: if not configured and not opted out, prompt
    if not config.get("opted_out") and not is_configured(config):
        if sys.stdin.isatty():
            print("\n⚠️  Flyee Bridge não está configurado.")
            config = setup_interactive()
            if not is_configured(config):
                return
        else:
            # Non-interactive: skip silently
            return

    if "--test" in args:
        test_connection(config)
        return

    if "--list-projects" in args:
        if not config.get("api_key"):
            print("❌ API Key não configurada. Execute --setup primeiro.")
            return
        projects = list_projects(
            config.get("api_url", "http://localhost:8001"), config["api_key"]
        )
        if projects:
            print(f"\n{'#':<4} {'Projeto':<30} {'Status':<12} {'ID'}")
            print("-" * 80)
            for i, p in enumerate(projects, 1):
                print(f"{i:<4} {p.get('name', '?'):<30} {p.get('status', '?'):<12} {p.get('id', '?')}")
        else:
            print("Nenhum projeto encontrado ou erro de conexão.")
        return

    if "--register-docs" in args:
        if not is_configured(config):
            print("❌ Bridge não configurado. Execute --setup primeiro.")
            return
        docs = scan_docs()
        if not docs:
            print("Nenhum documento encontrado em docs/.")
            return
        print(f"Registrando {len(docs)} documento(s)...")
        results = register_documents(
            config["api_url"], config["api_key"], config["project_id"], docs
        )
        for r in results:
            icon = "✅" if r["status"] == "registered" else "❌"
            print(f"   {icon} {r['title']} — {r['status']}")
        return

    if "--create-task" in args:
        if not is_configured(config):
            print("❌ Bridge não configurado. Execute --setup primeiro.")
            return
        # Parse arguments
        name = ""
        task_type = "implement_feature"
        description = ""
        priority = "normal"
        i = 0
        while i < len(args):
            if args[i] == "--name" and i + 1 < len(args):
                name = args[i + 1]
                i += 2
            elif args[i] == "--type" and i + 1 < len(args):
                task_type = args[i + 1]
                i += 2
            elif args[i] == "--description" and i + 1 < len(args):
                description = args[i + 1]
                i += 2
            elif args[i] == "--priority" and i + 1 < len(args):
                priority = args[i + 1]
                i += 2
            else:
                i += 1
        if not name:
            print("❌ --name é obrigatório. Ex: --create-task --name 'Fix login bug'")
            return
        result = create_task(
            config["api_url"],
            config["api_key"],
            config["project_id"],
            task_type=task_type,
            name=name,
            description=description,
            priority=priority,
        )
        if result:
            task_id = result.get("id", "unknown")
            emit_event("task.created", {
                "task_id": task_id,
                "name": name,
                "type": task_type,
                "priority": priority,
                "actor": "agent",
            }, config)
            print(json.dumps({"status": "created", "task_id": task_id, "name": name}))
        else:
            print(json.dumps({"status": "error", "message": "Failed to create task"}))
        return

    if "--update-task" in args:
        if not is_configured(config):
            print("❌ Bridge não configurado. Execute --setup primeiro.")
            return
        task_id = None
        status = None
        result_status = None
        i = 0
        while i < len(args):
            if args[i] == "--update-task" and i + 1 < len(args):
                task_id = args[i + 1]
                i += 2
            elif args[i] == "--status" and i + 1 < len(args):
                status = args[i + 1]
                i += 2
            elif args[i] == "--result" and i + 1 < len(args):
                result_status = args[i + 1]
                i += 2
            else:
                i += 1
        if not task_id:
            print("❌ task_id é obrigatório. Ex: --update-task <id> --status completed")
            return
        result = update_task(
            config["api_url"],
            config["api_key"],
            task_id,
            status=status,
            result_status=result_status,
        )
        if result:
            if status == "completed":
                emit_event("task.completed", {
                    "task_id": task_id,
                    "result": result_status or "success",
                    "actor": "agent",
                }, config)
            elif status == "running":
                emit_event("task.started", {
                    "task_id": task_id,
                    "actor": "agent",
                }, config)
            print(json.dumps({"status": "updated", "task_id": task_id}))
        else:
            print(json.dumps({"status": "error", "message": "Failed to update task"}))
        return

    if "--list-tasks" in args:
        if not is_configured(config):
            print("❌ Bridge não configurado. Execute --setup primeiro.")
            return
        status_filter = None
        i = 0
        while i < len(args):
            if args[i] == "--status" and i + 1 < len(args):
                status_filter = args[i + 1]
                i += 2
            else:
                i += 1
        tasks = list_tasks(
            config["api_url"],
            config["api_key"],
            config["project_id"],
            status=status_filter,
        )
        if tasks:
            print(f"\n{'#':<4} {'Task':<40} {'Status':<12} {'ID'}")
            print("-" * 100)
            for i, t in enumerate(tasks, 1):
                task_name = t.get("input", {}).get("name", t.get("type", "?"))
                print(f"{i:<4} {task_name:<40} {t.get('status', '?'):<12} {t.get('id', '?')}")
        else:
            print("Nenhuma task encontrada.")
        return

    if "--create-okr" in args:
        if not is_configured(config):
            print("❌ Bridge não configurado. Execute --setup primeiro.")
            return
        objective = ""
        key_results_str = ""
        period = ""
        owner = ""
        okr_status = "active"
        i = 0
        while i < len(args):
            if args[i] == "--objective" and i + 1 < len(args):
                objective = args[i + 1]
                i += 2
            elif args[i] == "--key-results" and i + 1 < len(args):
                key_results_str = args[i + 1]
                i += 2
            elif args[i] == "--period" and i + 1 < len(args):
                period = args[i + 1]
                i += 2
            elif args[i] == "--owner" and i + 1 < len(args):
                owner = args[i + 1]
                i += 2
            elif args[i] == "--okr-status" and i + 1 < len(args):
                okr_status = args[i + 1]
                i += 2
            else:
                i += 1
        if not objective:
            print("❌ --objective é obrigatório. Ex: --create-okr --objective 'Lançar MVP'")
            return
        key_results = json.loads(key_results_str) if key_results_str else None
        result = create_okr(
            config["api_url"],
            config["api_key"],
            config["project_id"],
            objective=objective,
            key_results=key_results,
            period=period or None,
            owner=owner or None,
            status=okr_status,
        )
        if result:
            okr_id = result.get("id", "unknown")
            emit_event("decision.okr_created", {
                "okr_id": okr_id,
                "objective": objective,
                "period": period,
                "actor": "agent",
            }, config)
            print(json.dumps({"status": "created", "okr_id": okr_id, "objective": objective}))
        else:
            print(json.dumps({"status": "error", "message": "Failed to create OKR"}))
        return

    if "--list-okrs" in args:
        if not is_configured(config):
            print("❌ Bridge não configurado. Execute --setup primeiro.")
            return
        okrs = list_okrs(
            config["api_url"],
            config["api_key"],
            config["project_id"],
        )
        if okrs:
            print(f"\n{'#':<4} {'Objective':<50} {'Status':<12} {'Progress':<10} {'ID'}")
            print("-" * 120)
            for i, o in enumerate(okrs, 1):
                progress = f"{o.get('progress', 0) * 100:.0f}%"
                print(f"{i:<4} {o.get('objective', '?')[:48]:<50} {o.get('status', '?'):<12} {progress:<10} {o.get('id', '?')}")
        else:
            print("Nenhum OKR encontrado.")
        return

    if "--create-decision" in args:
        if not is_configured(config):
            print("❌ Bridge não configurado. Execute --setup primeiro.")
            return
        decision_text = ""
        actor = "agent"
        reason = ""
        impact = ""
        task_id_ref = ""
        i = 0
        while i < len(args):
            if args[i] == "--decision" and i + 1 < len(args):
                decision_text = args[i + 1]
                i += 2
            elif args[i] == "--actor" and i + 1 < len(args):
                actor = args[i + 1]
                i += 2
            elif args[i] == "--reason" and i + 1 < len(args):
                reason = args[i + 1]
                i += 2
            elif args[i] == "--impact" and i + 1 < len(args):
                impact = args[i + 1]
                i += 2
            elif args[i] == "--task-id" and i + 1 < len(args):
                task_id_ref = args[i + 1]
                i += 2
            else:
                i += 1
        if not decision_text:
            print("❌ --decision é obrigatório. Ex: --create-decision --decision 'Usar Next.js'")
            return
        result = create_decision(
            config["api_url"],
            config["api_key"],
            config["project_id"],
            decision=decision_text,
            actor=actor,
            reason=reason or None,
            impact=impact or None,
            task_id=task_id_ref or None,
        )
        if result:
            dec_id = result.get("id", "unknown")
            emit_event("decision.recorded", {
                "decision_id": dec_id,
                "decision": decision_text,
                "actor": actor,
                "reason": reason,
            }, config)
            print(json.dumps({"status": "created", "decision_id": dec_id, "decision": decision_text}))
        else:
            print(json.dumps({"status": "error", "message": "Failed to create decision"}))
        return

    if "--list-decisions" in args:
        if not is_configured(config):
            print("❌ Bridge não configurado. Execute --setup primeiro.")
            return
        decisions = list_decisions(
            config["api_url"],
            config["api_key"],
            config["project_id"],
        )
        if decisions:
            print(f"\n{'#':<4} {'Decision':<45} {'Actor':<10} {'Date':<20} {'ID'}")
            print("-" * 130)
            for i, d in enumerate(decisions, 1):
                date_str = d.get("created_at", "?")[:19]
                print(f"{i:<4} {d.get('decision', '?')[:43]:<45} {d.get('actor', '?'):<10} {date_str:<20} {d.get('id', '?')}")
        else:
            print("Nenhuma decision encontrada.")
        return

    if "--register-metrics" in args:
        if not is_configured(config):
            print("❌ Bridge não configurado. Execute --setup primeiro.")
            return
        metric_type = ""
        metric_payload = "{}"
        i = 0
        while i < len(args):
            if args[i] == "--type" and i + 1 < len(args):
                metric_type = args[i + 1]
                i += 2
            elif args[i] == "--data" and i + 1 < len(args):
                metric_payload = args[i + 1]
                i += 2
            else:
                i += 1
        if not metric_type:
            print("❌ --type é obrigatório. Tipos: session_started, files_changed, tests_passed")
            return
        event_type = f"dev.{metric_type}"
        payload_data = json.loads(metric_payload)
        success = emit_event(event_type, payload_data, config)
        if success:
            print(json.dumps({"status": "emitted", "event": event_type}))
        else:
            print(json.dumps({"status": "skipped", "event": event_type}))
        return

    if "--list-collections" in args:
        if not is_configured(config):
            print("❌ Bridge não configurado. Execute --setup primeiro.")
            return
        collections = list_collections(
            config["api_url"],
            config["api_key"],
            config["project_id"],
        )
        if collections is None:
            print(json.dumps({"status": "error", "message": "Failed to list collections"}))
        elif not collections:
            print(json.dumps({"status": "ok", "collections": [], "total": 0}))
        else:
            print(json.dumps({
                "status": "ok",
                "total": len(collections),
                "collections": [
                    {
                        "id": c.get("collection_id", ""),
                        "name": c.get("collection_name", ""),
                        "readable_id": c.get("collection_readable_id", ""),
                    }
                    for c in collections
                ],
            }))
        return

    if "--search-context" in args:
        if not is_configured(config):
            print(json.dumps({"status": "skipped", "reason": "bridge not configured"}))
            return
        query = ""
        limit = 5
        min_score = 0.01
        i = 0
        while i < len(args):
            if args[i] == "--search-context" and i + 1 < len(args):
                query = args[i + 1]
                i += 2
            elif args[i] == "--limit" and i + 1 < len(args):
                limit = int(args[i + 1])
                i += 2
            elif args[i] == "--min-score" and i + 1 < len(args):
                min_score = float(args[i + 1])
                i += 2
            else:
                i += 1
        if not query:
            print(json.dumps({"status": "error", "message": "Query is required after --search-context"}))
            return
        results = search_collections(
            config["api_url"],
            config["api_key"],
            config["project_id"],
            query=query,
            limit=limit,
            min_score=min_score,
        )
        print(json.dumps(results, ensure_ascii=False))
        return

    # ── Test Checklist Commands ──────────────────────────────────

    if "--generate-tests" in args:
        idx = args.index("--generate-tests")
        task_id = args[idx + 1] if idx + 1 < len(args) else None
        if not task_id:
            print(json.dumps({"status": "error", "message": "Usage: --generate-tests <task_id>"}))
            return
        if not is_configured(config):
            print(json.dumps({"status": "skipped", "reason": "bridge not configured"}))
            return
        # Fetch the task to read acceptance criteria from meta
        base = config["api_url"].rstrip("/")
        task_data = api_request("GET", f"{base}/flyee/tasks/{task_id}", config["api_key"])
        if not task_data:
            print(json.dumps({"status": "error", "message": f"Task {task_id} not found"}))
            return
        meta = task_data.get("meta") or {}
        # Acceptance criteria source: meta.acceptance_criteria or input.description
        ac_text = ""
        if meta.get("acceptance_criteria"):
            ac_text = str(meta["acceptance_criteria"])
        elif task_data.get("input", {}) and task_data["input"].get("description"):
            ac_text = str(task_data["input"]["description"])
        # Generate steps from criteria (basic heuristic: one step per line/bullet)
        steps = []
        lines = [l.strip() for l in ac_text.replace("- [ ]", "").replace("- [x]", "").split("\n") if l.strip() and len(l.strip()) > 5]
        for i, line in enumerate(lines, 1):
            # Clean markdown bullets
            clean = line.lstrip("-*•").strip()
            if not clean:
                continue
            steps.append({
                "id": f"ts-{i}",
                "description": clean,
                "type": "manual",
                "category": "manual",
                "status": "pending",
                "result_comment": None,
                "tested_by": None,
                "tested_at": None,
            })
        if not steps:
            # Fallback: generate a single generic step
            steps = [{
                "id": "ts-1",
                "description": f"Verify implementation of task: {task_data.get('type', 'unknown')}",
                "type": "manual",
                "category": "manual",
                "status": "pending",
                "result_comment": None,
                "tested_by": None,
                "tested_at": None,
            }]
        checklist = {
            "steps": steps,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generated_by": "agent",
            "all_passed": False,
        }
        # Save to task.meta.test_checklist
        meta["test_checklist"] = checklist
        result = api_request("PUT", f"{base}/flyee/tasks/{task_id}", config["api_key"], {"meta": meta})
        if result:
            print(json.dumps({"status": "ok", "task_id": task_id, "steps_generated": len(steps)}))
        else:
            print(json.dumps({"status": "error", "message": "Failed to save test checklist"}))
        return

    if "--report-test" in args:
        idx = args.index("--report-test")
        remaining = args[idx + 1:]
        if len(remaining) < 3:
            print(json.dumps({"status": "error", "message": "Usage: --report-test <task_id> <step_id> passed|failed [comment]"}))
            return
        task_id, step_id, status = remaining[0], remaining[1], remaining[2]
        comment = remaining[3] if len(remaining) > 3 else None
        if status not in ("passed", "failed", "skipped"):
            print(json.dumps({"status": "error", "message": f"Invalid status: {status}. Use passed|failed|skipped"}))
            return
        if not is_configured(config):
            print(json.dumps({"status": "skipped", "reason": "bridge not configured"}))
            return
        base = config["api_url"].rstrip("/")
        payload = {"step_id": step_id, "status": status, "tested_by": "agent"}
        if comment:
            payload["result_comment"] = comment
        result = api_request("PUT", f"{base}/flyee/tasks/{task_id}/test-results", config["api_key"], payload)
        if result:
            tc = (result.get("meta") or {}).get("test_checklist", {})
            print(json.dumps({
                "status": "ok",
                "step_id": step_id,
                "step_status": status,
                "all_passed": tc.get("all_passed", False),
            }))
        else:
            print(json.dumps({"status": "error", "message": "Failed to update test result"}))
        return

    if "--pending-tests" in args:
        idx = args.index("--pending-tests")
        task_id = args[idx + 1] if idx + 1 < len(args) else None
        if not task_id:
            print(json.dumps({"status": "error", "message": "Usage: --pending-tests <task_id>"}))
            return
        if not is_configured(config):
            print(json.dumps({"status": "skipped", "reason": "bridge not configured"}))
            return
        base = config["api_url"].rstrip("/")
        task_data = api_request("GET", f"{base}/flyee/tasks/{task_id}", config["api_key"])
        if not task_data:
            print(json.dumps({"status": "error", "message": f"Task {task_id} not found"}))
            return
        tc = (task_data.get("meta") or {}).get("test_checklist", {})
        steps = tc.get("steps", [])
        pending = [s for s in steps if s.get("status") in ("pending", "failed")]
        print(json.dumps({
            "status": "ok",
            "task_id": task_id,
            "total": len(steps),
            "pending_count": len(pending),
            "pending": [{"id": s["id"], "description": s["description"], "status": s["status"],
                         "category": s.get("category", ""), "type": s.get("type", "")} for s in pending],
        }))
        return

    if "--test-summary" in args:
        idx = args.index("--test-summary")
        task_id = args[idx + 1] if idx + 1 < len(args) else None
        if not task_id:
            print(json.dumps({"status": "error", "message": "Usage: --test-summary <task_id>"}))
            return
        if not is_configured(config):
            print(json.dumps({"status": "skipped", "reason": "bridge not configured"}))
            return
        base = config["api_url"].rstrip("/")
        task_data = api_request("GET", f"{base}/flyee/tasks/{task_id}", config["api_key"])
        if not task_data:
            print(json.dumps({"status": "error", "message": f"Task {task_id} not found"}))
            return
        tc = (task_data.get("meta") or {}).get("test_checklist", {})
        steps = tc.get("steps", [])
        passed = sum(1 for s in steps if s.get("status") == "passed")
        failed_steps = [s["id"] for s in steps if s.get("status") == "failed"]
        skipped = sum(1 for s in steps if s.get("status") == "skipped")
        pending = sum(1 for s in steps if s.get("status") == "pending")
        print(json.dumps({
            "status": "ok",
            "task_id": task_id,
            "total": len(steps),
            "passed": passed,
            "failed": len(failed_steps),
            "skipped": skipped,
            "pending": pending,
            "failed_ids": failed_steps,
            "all_passed": tc.get("all_passed", False),
        }))
        return

    if args[0] == "emit" and len(args) >= 2:
        event_type = args[1]
        payload = json.loads(args[2]) if len(args) > 2 else {}
        success = emit_event(event_type, payload, config)
        if success:
            print(f"✅ Event '{event_type}' emitted")
        else:
            print(f"⚠️  Event '{event_type}' skipped (bridge disabled)")
        return

    print(f"Unknown command: {args}")
    print("Use --help for usage info")


if __name__ == "__main__":
    main()
