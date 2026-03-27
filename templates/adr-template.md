---
type: ADR
doc_id: ADR-{NNN}-{slug}
status: proposed     # proposed | accepted | deprecated | superseded
date: YYYY-MM-DD
deciders:
  - [Nome]
superseded_by: null
related_docs:
  - docs/design/SDD-{project-slug}.md
  - docs/INDEX.md
---

# ADR-{NNN}: {Título da Decisão}

> **Architecture Decision Record** — Registra o contexto, a decisão e as consequências de uma escolha arquitetural significativa.

---

## 0. Agent Context

| Campo | Valor |
|-------|-------|
| **Status** | proposed |
| **Decisão em uma linha** | [Ex: Usar PostgreSQL em vez de MongoDB] |
| **Força a mudança em** | [Ex: SDD-{slug}.md §4, new-project.md Phase 3.5] |

---

## 1. Contexto

> Descreva a situação que levou a esta decisão. Qual problema está sendo resolvido? Quais forças estão em jogo (técnicas, organizacionais, de prazo)?

[Descreva o contexto aqui]

---

## 2. Decisão

> Declare a decisão de forma imperativa e inequívoca.

**Decidimos** [ação concreta, ex: "adotar PostgreSQL como banco de dados principal"].

---

## 3. Consequências

### Positivas
- [Benefício 1]
- [Benefício 2]

### Negativas / Trade-offs
- [Custo ou limitação 1]
- [Custo ou limitação 2]

### Neutras
- [Mudança de processo necessária, sem julgamento de valor]

---

## 4. Alternativas Consideradas

| Alternativa | Por que rejeitada |
|-------------|------------------|
| [Opção A] | [Motivo] |
| [Opção B] | [Motivo] |

---

## 5. Validação

> Como saberemos que esta decisão foi correta?

- [ ] [Critério de sucesso 1]
- [ ] [Critério de sucesso 2]

---

## Histórico

| Data | Status | Autor | Nota |
|------|--------|-------|------|
| YYYY-MM-DD | proposed | [Nome] | Criação |
