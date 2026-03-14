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

# Resolve config path relative to this script
BRIDGE_DIR = Path(__file__).parent
CONFIG_PATH = BRIDGE_DIR / "config.json"
FALLBACK_PATH = BRIDGE_DIR / "events.jsonl"

DEFAULT_CONFIG = {
    "api_url": "http://localhost:8001",
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
    timeout: int = 10,
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
        print(f"❌ API error {e.code}: {e.reason}")
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
    results = []
    url = f"{api_url.rstrip('/')}/flyee/projects/{project_id}/documents"

    for doc in docs:
        try:
            with open(doc["path"], "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            results.append({**doc, "status": "error", "error": str(e)})
            continue

        resp = api_request("POST", url, api_key, {
            "title": doc["title"],
            "type": doc["type"],
            "content": content,
        })

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
                   implement_feature, run_tests, generate_docs
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

    default_url = config.get("api_url", "http://localhost:8001")
    url = input(f"API URL [{default_url}]: ").strip()
    config["api_url"] = url or default_url

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
