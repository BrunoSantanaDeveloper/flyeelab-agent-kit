#!/usr/bin/env python3
"""
doc-sync-check.py — Detecta divergências entre codebase e documentação.

Verifica:
  1. Features em frontend/src/features/ vs PRD Sec 6.1
  2. SDK modules em frontend/src/lib/flyee-sdk/ vs SDD Sec 3.2
  3. Implementation Order no SDD vs estado real dos sprints
  4. Arquivos em docs/ vs INDEX.md

Uso:
  python3 .agent/scripts/doc-sync-check.py
  python3 .agent/scripts/doc-sync-check.py --verbose
  python3 .agent/scripts/doc-sync-check.py --section prd
  python3 .agent/scripts/doc-sync-check.py --section sdd
  python3 .agent/scripts/doc-sync-check.py --section index
"""

import os
import re
import sys
import argparse
from pathlib import Path

# ─── Paths ──────────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.parent.parent  # /home/bruno/flyee
FEATURES_DIR = ROOT / "frontend/src/features"
SDK_DIR = ROOT / "frontend/src/lib/flyee-sdk"
PRD_PATH = ROOT / "docs/PRD-flyee.md"
SDD_PATH = ROOT / "docs/design/SDD-flyee.md"
INDEX_PATH = ROOT / "docs/INDEX.md"

# ─── ANSI colors ────────────────────────────────────────────────────────────

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

ok = f"{GREEN}✅{RESET}"
warn = f"{YELLOW}⚠️ {RESET}"
err = f"{RED}❌{RESET}"


# ─── Helpers ────────────────────────────────────────────────────────────────

def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def section(title: str):
    print(f"\n{BOLD}{CYAN}{'─'*60}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*60}{RESET}")


# ─── Check 1: Features vs PRD ───────────────────────────────────────────────

def check_features_vs_prd(verbose: bool) -> int:
    section("1. Features implementadas vs PRD Sec 6.1")
    issues = 0

    if not FEATURES_DIR.exists():
        print(f"  {warn} features dir não encontrado: {FEATURES_DIR}")
        return 1

    implemented = sorted([d.name for d in FEATURES_DIR.iterdir() if d.is_dir()])
    prd_text = read_file(PRD_PATH)

    # Extract feature table rows from PRD (lines with | F\d+ |)
    prd_feature_rows = re.findall(r"\|\s*(F\d+)\s*\|.*?\|.*?\|\s*(✅[^|]*|⏳[^|]*|\?[^|]*)\|", prd_text)
    prd_statuses = {f_id.strip(): status.strip() for f_id, status in prd_feature_rows}

    # Map known feature dirs to F-IDs (extend as project grows)
    feature_map = {
        "activity":     ("F7",  "Activity Feed"),
        "decisions":    ("F5",  "Decision Log"),
        "dev-activity": ("F7",  "Activity Feed (Dev)"),
        "documents":    ("F4",  "Document Viewer + Planning History"),
        "health":       (None,  "Health check (internal)"),
        "knowledge":    ("F6",  "Knowledge Hub"),
        "okrs":         ("F10", "OKR Dashboard"),
        "projects":     ("F2",  "Project CRUD"),
        "proposals":    ("F9",  "Proposal Module"),
        "tasks":        ("F3",  "Task Management + F10 QA Gate"),
    }

    print(f"  {'Feature Dir':<20} {'F-ID':<8} {'PRD Status':<30} {'Check'}")
    print(f"  {'─'*20} {'─'*8} {'─'*30} {'─'*10}")

    for feat_dir in implemented:
        mapping = feature_map.get(feat_dir)
        if mapping is None:
            if verbose:
                print(f"  {warn} {feat_dir:<20} {'?':<8} {'Not in feature_map':<30} {warn} unmapped")
            issues += 1
            continue

        f_id, label = mapping
        if f_id is None:
            if verbose:
                print(f"  {feat_dir:<22} {'—':<8} {'Internal':<30} {ok}")
            continue

        # Check if f_id documented in PRD
        documented = f_id in prd_statuses
        status_in_prd = prd_statuses.get(f_id, "NOT IN PRD")
        has_done = "Done" in status_in_prd or "✅" in status_in_prd

        if not documented:
            symbol = err
            issues += 1
        elif not has_done:
            symbol = warn
            issues += 1
        else:
            symbol = ok

        print(f"  {feat_dir:<22} {f_id:<8} {status_in_prd[:30]:<32} {symbol}")

    # Check if PRD has F-IDs that don't map to any feature dir
    all_known_fids = {v[0] for v in feature_map.values() if v[0]}
    for f_id, status in prd_statuses.items():
        if f_id not in all_known_fids:
            if verbose:
                print(f"  {warn} PRD has {f_id} but no matching feature dir")

    return issues


# ─── Check 2: SDK modules vs SDD ────────────────────────────────────────────

def check_sdk_vs_sdd(verbose: bool) -> int:
    section("2. SDK modules vs SDD Sec 3.2")
    issues = 0

    if not SDK_DIR.exists():
        print(f"  {warn} SDK dir não encontrado: {SDK_DIR}")
        return 1

    sdk_files = sorted([f.stem for f in SDK_DIR.glob("*.ts") if f.stem not in ("index", "client")])
    sdd_text = read_file(SDD_PATH)

    # Extract SDK module rows only from Section 3.2 of SDD
    # Look for the table between "### 3.2 Flyee SDK Layer" and the next "###"
    sdk_section_match = re.search(
        r"### 3\.2 Flyee SDK Layer(.+?)(?=^###|\.\.\.END)",
        sdd_text, re.DOTALL | re.MULTILINE
    )
    sdk_section = sdk_section_match.group(1) if sdk_section_match else sdd_text
    sdd_sdk_rows = re.findall(r"\|\s*`([a-z][a-z0-9\-]+\.ts)`\s*\|", sdk_section)
    sdd_modules = {r.replace(".ts", "") for r in sdd_sdk_rows}

    # Only check files actually in flyee-sdk/ (not stores or other libs)
    sdk_files_to_check = [f for f in sdk_files if f != "types"]  # types.ts is internal

    # Known stores (live in lib/stores/, NOT in flyee-sdk/) — exclude from SDD check
    known_stores = {"auth-store", "collections", "organizations", "sources", "usage", "user", "webhooks",
                    "activityStore", "decisionsStore", "projectsStore", "sidePanelStore", "tasksStore",
                    "okrsStore", "documentsStore", "apiKeys", "authProviders", "uiStore", "index"}

    print(f"  {'SDK File':<30} {'In SDD':<10} {'Status'}")
    print(f"  {'─'*30} {'─'*10} {'─'*10}")

    for sdk_file in sdk_files_to_check:
        in_sdd = sdk_file in sdd_modules
        symbol = ok if in_sdd else err
        if not in_sdd:
            issues += 1
        print(f"  {sdk_file+'.ts':<32} {'✓' if in_sdd else 'MISSING':<10} {symbol}")

    # Modules in SDD but not in filesystem and not in known_stores
    for sdd_mod in sorted(sdd_modules):
        if sdd_mod in known_stores:
            continue  # skip stores — they live in lib/stores/, not lib/flyee-sdk/
        actual_file = SDK_DIR / f"{sdd_mod}.ts"
        if not actual_file.exists():
            print(f"  {warn} SDD documenta `{sdd_mod}.ts` mas arquivo não existe no SDK dir")
            issues += 1

    return issues


# ─── Check 3: Implementation Order vs sprints ────────────────────────────────

def check_impl_order(verbose: bool) -> int:
    section("3. SDD Sec 13 — Implementation Order")
    issues = 0

    sdd_text = read_file(SDD_PATH)

    # Find Implementation Order table rows: | N | Description | Status | Dependency |
    rows = re.findall(
        r"\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(✅[^|]*|⏳[^|]*|\?[^|]*|[^|]+)\s*\|\s*([^|]+)\s*\|",
        sdd_text
    )

    if not rows:
        print(f"  {warn} Não encontrei tabela de Implementation Order no SDD")
        return 1

    pending = []
    done = []
    for num, component, status, dep in rows:
        status = status.strip()
        component = component.strip()
        if "Done" in status or "✅" in status:
            done.append((num, component))
        elif "⏳" in status or "Pendente" in status:
            pending.append((num, component))
        else:
            pending.append((num, component))
            issues += 1

    print(f"  {ok} Concluídos:  {len(done)} itens")
    print(f"  {'⏳'} Pendentes:   {len(pending)} itens")

    if pending:
        print(f"\n  Pendentes:")
        for num, comp in pending:
            print(f"    #{num} {comp[:60]}")

    if len(done) == 0:
        print(f"  {err} Nenhum item marcado como Done — SDD pode estar desatualizado")
        issues += 1

    return issues


# ─── Check 4: docs/ vs INDEX.md ─────────────────────────────────────────────

def check_docs_index(verbose: bool) -> int:
    section("4. docs/ vs INDEX.md")
    issues = 0

    docs_dir = ROOT / "docs"
    if not docs_dir.exists():
        print(f"  {warn} docs/ dir não encontrado")
        return 1

    # All .md files (excluding INDEX itself, recursively)
    all_docs = sorted([
        f.relative_to(ROOT)
        for f in docs_dir.rglob("*.md")
        if f.name != "INDEX.md"
    ])

    index_text = read_file(INDEX_PATH)

    print(f"  {'Arquivo':<50} {'Em INDEX.md'}")
    print(f"  {'─'*50} {'─'*12}")

    for doc_path in all_docs:
        doc_name = doc_path.name
        in_index = doc_name in index_text or str(doc_path) in index_text
        symbol = ok if in_index else warn
        if not in_index:
            issues += 1
        if verbose or not in_index:
            print(f"  {str(doc_path):<52} {symbol}")

    if not verbose:
        print(f"\n  {ok} {len(all_docs) - issues}/{len(all_docs)} documentos registrados no INDEX.md")
        if issues:
            print(f"  {warn} {issues} doc(s) não encontrados no INDEX — rode com --verbose para ver quais")

    return issues


# ─── Check 5: BREAKDOWN-tasks.md vs Flyee ────────────────────────────────────

def check_breakdown_vs_flyee(verbose: bool) -> int:
    section("5. BREAKDOWN-tasks.md vs Flyee")
    issues = 0

    breakdown_path = ROOT / "docs/BREAKDOWN-tasks.md"
    if not breakdown_path.exists():
        print(f"  {warn} docs/BREAKDOWN-tasks.md não encontrado")
        return 1

    # ── Parse BREAKDOWN: extrair headers das tasks + sprint ────────────────
    breakdown_text = read_file(breakdown_path)

    sprint_pattern = re.compile(r"^## Sprint (\d+)[:\s]+(.+)$", re.MULTILINE)
    task_pattern   = re.compile(r"^### (T\d+\.\d+) — (.+)$", re.MULTILINE)

    sprints   = [(int(m.group(1)), m.start()) for m in sprint_pattern.finditer(breakdown_text)]
    tasks_raw = [(m.group(1), m.group(2).strip(), m.start()) for m in task_pattern.finditer(breakdown_text)]

    def find_sprint_for_pos(pos: int) -> int:
        sprint = 0
        for s_num, s_pos in sprints:
            if s_pos <= pos:
                sprint = s_num
        return sprint

    breakdown_tasks: dict = {}
    for t_id, t_name, t_pos in tasks_raw:
        sprint_num = find_sprint_for_pos(t_pos)
        breakdown_tasks[t_id] = {"name": t_name, "sprint": sprint_num}


    # ── Sprints concluídos: ler tabela Summary do próprio BREAKDOWN ─────────
    # Busca linhas da tabela com "✅ Done" — sprints sem esse marcador são pendentes
    pending_sprints: set = set()
    for line in breakdown_text.splitlines():
        # Linha da tabela: | **N** | T... | 🔲 Pendente | ... |
        m = re.match(r"\|\s*\*\*(\d+)\*\*\s*\|.+?🔲", line)
        if m:
            pending_sprints.add(int(m.group(1)))

    # Todos os sprints encontrados no breakdown
    all_sprints = {info["sprint"] for info in breakdown_tasks.values() if info["sprint"] > 0}
    completed_sprints = all_sprints - pending_sprints


    # ── Carregar tasks do Flyee via bridge CLI ─────────────────────────────
    import subprocess
    bridge = ROOT / ".agent/flyee-bridge/bridge.py"

    flyee_tasks: dict = {}  # "T1.1" -> "completed" | "running" | ...
    if bridge.exists():
        try:
            result = subprocess.run(
                ["python3", str(bridge), "--list-tasks"],
                capture_output=True, text=True, timeout=15, cwd=str(ROOT)
            )
            for line in result.stdout.splitlines():
                # Format: "N    T1.1 — Name    status    uuid"
                m = re.match(
                    r"\s*\d+\s+(T\d+\.\d+)[^\t]+?\s{2,}(completed|running|pending|failed|testing|cancelled)\s",
                    line
                )
                if m:
                    t_label, t_status = m.group(1), m.group(2)
                    flyee_tasks[t_label] = t_status  # last occurrence wins
        except Exception as e:
            print(f"  {warn} Não foi possível carregar tasks do Flyee: {e}")
    else:
        print(f"  {warn} Bridge não encontrado — pulando verificação Flyee")

    # ── Comparar ────────────────────────────────────────────────────────────
    ghost_running = []  # sprint Done no SDD mas task ainda 'running' no Flyee

    for t_id, info in sorted(breakdown_tasks.items()):
        sprint = info["sprint"]
        if sprint not in completed_sprints:
            continue  # sprint ainda em andamento — OK estar running
        flyee_status = flyee_tasks.get(t_id)
        if flyee_status is not None and flyee_status != "completed":
            ghost_running.append((t_id, info["name"], sprint, flyee_status))
            issues += 1

    # Tasks no Flyee como 'running' cujo sprint já é Done
    for t_label, t_status in flyee_tasks.items():
        if t_status == "running" and t_label in breakdown_tasks:
            sprint = breakdown_tasks[t_label]["sprint"]
            if sprint in completed_sprints and not any(g[0] == t_label for g in ghost_running):
                ghost_running.append((t_label, breakdown_tasks[t_label]["name"], sprint, "running"))
                issues += 1

    # ── Output ──────────────────────────────────────────────────────────────
    total_bd = len(breakdown_tasks)
    matched  = sum(1 for t in breakdown_tasks if t in flyee_tasks)

    print(f"  Tasks no BREAKDOWN:         {total_bd}")
    print(f"  Tasks encontradas no Flyee: {matched}/{total_bd}")
    print(f"  Sprints concluídos (SDD):   {sorted(completed_sprints)}")

    if not ghost_running:
        print(f"\n  {ok} Nenhuma divergência BREAKDOWN ↔ Flyee")
    else:
        print(f"\n  {err} {len(ghost_running)} task(s) com status desatualizado no Flyee:")
        print(f"  {'Task':<12} {'Sprint':<8} {'Status Flyee':<16} {'Nome'}")
        print(f"  {'─'*12} {'─'*8} {'─'*16} {'─'*40}")
        for t_id, name, sprint, status in sorted(ghost_running):
            print(f"  {t_id:<14} {str(sprint):<8} {status:<18} {name[:40]}")
        print(f"\n  Para corrigir (substitua <uuid> pelo ID real do Flyee):")
        print(f"    python3 .agent/flyee-bridge/bridge.py --update-task <uuid> --status completed --result success")

    # Tasks de sprints concluídos não encontradas no Flyee (verbose only)
    if verbose:
        not_in_flyee = [
            (t_id, info) for t_id, info in breakdown_tasks.items()
            if t_id not in flyee_tasks and info["sprint"] in completed_sprints
        ]
        if not_in_flyee:
            print(f"\n  {warn} Tasks de sprints concluídos não encontradas no Flyee:")
            for t_id, info in sorted(not_in_flyee):
                print(f"    Sprint {info['sprint']}: {t_id} — {info['name']}")

    return issues


# ─── Summary ─────────────────────────────────────────────────────────────────

def print_summary(total_issues: int):
    section("Resumo")
    if total_issues == 0:
        print(f"  {ok} {GREEN}{BOLD}Docs sincronizados — nenhuma divergência encontrada.{RESET}")
    else:
        print(f"  {err} {RED}{BOLD}{total_issues} divergência(s) encontrada(s).{RESET}")
        print(f"\n  Próximos passos:")
        print(f"    1. Corrija as divergências ANTES de marcar a task como concluída")
        print(f"    2. Features F-level: atualizar PRD Sec 6.1 + SDD Sec 13")
        print(f"    3. SDK changes: atualizar SDD Sec 3.2")
        print(f"    4. Novos docs: atualizar docs/INDEX.md")
        print(f"    5. Tasks desatualizadas: bridge.py --update-task <uuid> --status completed")
        print()
        print(f"  Docs relevantes:")
        print(f"    PRD:       docs/PRD-flyee.md")
        print(f"    SDD:       docs/design/SDD-flyee.md")
        print(f"    INDEX:     docs/INDEX.md")
        print(f"    BREAKDOWN: docs/BREAKDOWN-tasks.md")


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Detecta divergências entre codebase e documentação do projeto Flyee."
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Output detalhado")
    parser.add_argument(
        "--section", "-s",
        choices=["prd", "sdd", "index", "breakdown", "all"],
        default="all",
        help="Rodar apenas uma seção específica (default: all)"
    )
    args = parser.parse_args()

    print(f"\n{BOLD}🔍 doc-sync-check — Flyee Documentation Audit{RESET}")
    print(f"   Root: {ROOT}")

    total_issues = 0

    if args.section in ("prd", "all"):
        total_issues += check_features_vs_prd(args.verbose)

    if args.section in ("sdd", "all"):
        total_issues += check_sdk_vs_sdd(args.verbose)
        total_issues += check_impl_order(args.verbose)

    if args.section in ("index", "all"):
        total_issues += check_docs_index(args.verbose)

    if args.section in ("breakdown", "all"):
        total_issues += check_breakdown_vs_flyee(args.verbose)

    print_summary(total_issues)
    sys.exit(0 if total_issues == 0 else 1)


if __name__ == "__main__":
    main()
