---
name: tdd-workflow
description: Test-Driven Development workflow principles. RED-GREEN-REFACTOR cycle.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# TDD Workflow

> Write tests first, code second.

---

## 1. The TDD Cycle

```
🔴 RED → Write failing test
    ↓
🟢 GREEN → Write minimal code to pass
    ↓
🔵 REFACTOR → Improve code quality
    ↓
   Repeat...
```

---

## 2. The Three Laws of TDD

1. Write production code only to make a failing test pass
2. Write only enough test to demonstrate failure
3. Write only enough code to make the test pass

---

## 3. RED Phase Principles

### What to Write

| Focus | Example |
|-------|---------|
| Behavior | "should add two numbers" |
| Edge cases | "should handle empty input" |
| Error states | "should throw for invalid data" |

### RED Phase Rules

- Test must fail first
- Test name describes expected behavior
- One assertion per test (ideally)

---

## 4. GREEN Phase Principles

### Minimum Code

| Principle | Meaning |
|-----------|---------|
| **YAGNI** | You Aren't Gonna Need It |
| **Simplest thing** | Write the minimum to pass |
| **No optimization** | Just make it work |

### GREEN Phase Rules

- Don't write unneeded code
- Don't optimize yet
- Pass the test, nothing more

### UI Components in GREEN Phase

> For components with UI, use Design System during GREEN phase:

| Step | Action |
|------|--------|
| 1 | Load `design-system/{project}/MASTER.md` |
| 2 | Use CSS variables (e.g., `var(--bg-card)`) |
| 3 | Follow skill `design-system-enforcement` |
| 4 | No hardcoded colors or values |
| 5 | Use Lucide/Heroicons, not emojis |

---


## 5. REFACTOR Phase Principles

### What to Improve

| Area | Action |
|------|--------|
| Duplication | Extract common code |
| Naming | Make intent clear |
| Structure | Improve organization |
| Complexity | Simplify logic |

### REFACTOR Rules

- All tests must stay green
- Small incremental changes
- Commit after each refactor

---

## 6. AAA Pattern

Every test follows:

| Step | Purpose |
|------|---------|
| **Arrange** | Set up test data |
| **Act** | Execute code under test |
| **Assert** | Verify expected outcome |

---

## 7. When to Use TDD

| Scenario | TDD Value |
|----------|-----------|
| New feature | High |
| Bug fix | High (write test first) |
| Complex logic | High |
| Exploratory | Low (spike, then TDD) |
| UI layout | Low |

---

## 8. Test Prioritization

| Priority | Test Type |
|----------|-----------|
| 1 | Happy path |
| 2 | Error cases |
| 3 | Edge cases |
| 4 | Performance |

---

## 9. Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Skip the RED phase | Watch test fail first |
| Write tests after | Write tests before |
| Over-engineer initial | Keep it simple |
| Multiple asserts | One behavior per test |
| Test implementation | Test behavior |

---

## 10. AI-Augmented TDD

### Multi-Agent Pattern

| Agent | Role |
|-------|------|
| Agent A | Write failing tests (RED) |
| Agent B | Implement to pass (GREEN) |
| Agent C | Optimize (REFACTOR) |

---

> **Remember:** The test is the specification. If you can't write a test, you don't understand the requirement.

---

## 11. Pós-TDD: Sync com Flyee (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Após GREEN passar, ANTES de notificar usuário, DEVE:
> 1. Atualizar task no Flyee (Status → "Concluído", Tempo Gasto, % Progresso → 100)
> 2. Adicionar nota de conclusão no corpo da task
> 3. Seguir skill `Flyee API` seção "Gate de Sync Flyee" (linhas 167-263)

### Checklist Pós-GREEN

| Ação | API |
|------|-----|
| Status → Concluído | `Flyee API: update_task()` |
| Preencher Tempo Gasto | `Flyee API: update_task()` |
| Nota de Conclusão | `Flyee API: update_task() (output)` |

> [!WARNING]
> **📜 HISTÓRICO DE FALHA (2026-02-08):**
> - **Gap detectado:** Agente completou TDD para Task #1 mas não syncou com Flyee
> - **Causa raiz:** Esta skill não referenciava `Flyee API`
> - **Correção aplicada:** Adicionada seção 11 com regra bloqueante

