---
type: PROJECT_PROGRESS
project: {slug}
doc_registry: docs/INDEX.md
last_updated: YYYY-MM-DD
current_phase: PHASE-000
current_mode: complete   # complete | quick | brainstorm
---

# Project Progress — {project-name}

> Checkpoint file for the `/new-project` workflow. Maintained automatically.
> **Resume:** Run `/new-project --resume` to continue from the last incomplete phase.

---

## Status Geral

| Campo | Valor |
|-------|-------|
| **Projeto** | {project-name} |
| **Iniciado em** | YYYY-MM-DD |
| **Última atualização** | YYYY-MM-DD |
| **Fase atual** | PHASE-205 (Project Foundation) |
| **Modo** | complete \| quick \| brainstorm |

---

## Project Profile

| Campo | Valor |
|-------|-------|
| **Tipo** | web \| mobile \| backend \| fullstack |
| **Stack** | {stack} |
| **Agent principal** | frontend-specialist \| backend-specialist \| mobile-developer |
| **Design approach** | custom \| from-reference \| stitch-generated |
| **Flyee habilitado** | true \| false |

---

## Phases Checklist

> IDs de fase são parseáveis por agente. Formato: `PHASE-{NNN}` onde NNN = número da fase × 100.

| ID | Phase | Status | Artefato gerado | Completado em |
|----|-------|--------|-----------------|---------------|
| PHASE-000 | Gate 0: Project Type Discovery | ⬜ pending | PROJECT-PROGRESS.md | — |
| PHASE-000B | Phase 0: Brainstorm (opcional) | ⬜ skipped | — | — |
| PHASE-100 | Phase 1: PRD | ⬜ pending | docs/PRD-{slug}.md | — |
| PHASE-200 | Phase 2: SDD | ⬜ pending | docs/design/SDD-{slug}.md | — |
| PHASE-205 | Phase 2.05: Project Foundation | ⬜ pending | README.md, .env.example, SECURITY.md, docs/INDEX.md, docs/adr/ADR-000.md | — |
| PHASE-210 | Phase 2.1: Task Setup | ⬜ pending | Tasks no tracker | — |
| PHASE-245 | Phase 2.45: Visual Reference | ⬜ pending | Referências coletadas | — |
| PHASE-250 | Phase 2.5: Design System | ⬜ pending | docs/design/DESIGN-SYSTEM.md | — |
| PHASE-265 | Phase 2.65: Content Strategy | ⬜ pending | docs/design/CONTENT-*.md | — |
| PHASE-270 | Phase 2.7: Stitch (opcional) | ⬜ skipped | Protótipos | — |
| PHASE-280 | Phase 2.8: Page Specifications | ⬜ pending | docs/design/PAGE-SPEC-*.md | — |
| PHASE-290 | Phase 2.9: Analytics Strategy | ⬜ pending | Eventos mapeados | — |
| PHASE-300 | Phase 3: Breakdown (Tasks) | ⬜ pending | {nome}.md | — |
| PHASE-310 | Phase 3.1: OKR Creation | ⬜ pending | OKRs no Flyee | — |
| PHASE-350 | Phase 3.5: Project Setup | ⬜ pending | Infra inicializada | — |
| PHASE-400 | Phase 4: TDD Metodologia | ⬜ pending | tests/ | — |
| PHASE-500 | Phase 5: Implementação | ⬜ pending | src/ | — |
| PHASE-550 | Phase 5.5: Security Review | ⬜ pending | Relatório de security | — |
| PHASE-560 | Phase 5.6: Code Review Gate | ⬜ pending | Checklist assinado | — |
| PHASE-600 | Phase 6: Verificação (6.0+6.1+6.2) | ⬜ pending | Cobertura ≥ 80% + a11y + perf | — |
| PHASE-650 | Phase 6.5: Staging Validation | ⬜ pending | Aprovação stakeholder | — |
| PHASE-700 | Phase 7: Deploy | ⬜ pending | App em produção | — |
| PHASE-770 | Phase 7.7: Retrospective | ⬜ pending | docs/RETRO-{slug}-v1.md | — |

**Legenda:** ✅ done | 🔄 in_progress | ⬜ pending | ⏭️ skipped

---

## Tasks

| ID (Tracker) | Nome | Status | Phase |
|--------------|------|--------|-------|
| — | — | — | — |

---

## Desync Detector (para --resume)

> Preenchido automaticamente ao executar `--resume`.

| Phase | Status Local | Status Tracker | Ação necessária |
|-------|-------------|----------------|-----------------|
| — | — | — | — |

---

## Log de Ações

| Data | Fase | Ação | Agente |
|------|------|------|--------|
| YYYY-MM-DD | PHASE-000 | Arquivo criado | new-project workflow |
