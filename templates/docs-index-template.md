---
type: INDEX
project: {slug}
last_updated: YYYY-MM-DD
generated_by: new-project workflow Phase 2.05
---

# Document Registry — {project-name}

> Central registry for all project documents. Updated automatically by the agent whenever a document is created or its status changes.
> **Agent instruction:** Before reading any document, consult this INDEX to find the correct path and verify status.

---

## Document Map

| doc_id | Type | File | Status | Version | Approved at |
|--------|------|------|--------|---------|-------------|
| PRD-{slug} | PRD | [docs/PRD-{slug}.md](PRD-{slug}.md) | draft | 1.0 | — |
| SDD-{slug} | SDD | [docs/design/SDD-{slug}.md](design/SDD-{slug}.md) | draft | 1.0 | — |
| DS-{slug} | Design System | [docs/design/DESIGN-SYSTEM.md](design/DESIGN-SYSTEM.md) | draft | 1.0 | — |
| API-{slug} | OpenAPI Spec | [docs/api/openapi.yaml](api/openapi.yaml) | draft | 1.0 | — |
| SECURITY | Security Policy | [SECURITY.md](../SECURITY.md) | approved | 1.0 | YYYY-MM-DD |

### Architecture Decision Records (ADRs)

| doc_id | Title | Status | Date |
|--------|-------|--------|------|
| ADR-000-{slug} | Initial Setup | accepted | YYYY-MM-DD |

### Page Specifications

| doc_id | Page | File | Status |
|--------|------|------|--------|
| PAGESPEC-{page} | {Page Name} | [docs/design/PAGE-SPEC-{page}.md](design/PAGE-SPEC-{page}.md) | draft |

### Content Strategy

| doc_id | Scope | File | Status |
|--------|-------|------|--------|
| CONTENT-{page} | {Page Name} | [docs/design/CONTENT-{page}.md](design/CONTENT-{page}.md) | draft |

### Retrospectives

| doc_id | Version | File | Date |
|--------|---------|------|------|
| RETRO-{slug}-v1 | v1.0 | [docs/RETRO-{slug}-v1.md](RETRO-{slug}-v1.md) | — |

---

## Status Reference

| Status | Meaning | Agent Action |
|--------|---------|--------------|
| `draft` | Work in progress | Do not treat as authoritative |
| `review` | Awaiting human approval | Flag for review before implementing |
| `approved` | Human approved — source of truth | Implement without questioning |
| `superseded` | Replaced by newer version | Do not use; see replacement |

---

## Agent Instructions

1. **Always check this INDEX first** before searching for documents
2. **Update this INDEX** whenever you create or approve a document — change `status`, `version`, and `approved_at` accordingly
3. **Do not implement from `draft` documents** without explicit user approval
4. **Cross-reference**: every SDD section references PRD requirements by ID (e.g., `REQ-F1`)

---

*Auto-maintained. Do not add prose sections — keep this file purely tabular.*
