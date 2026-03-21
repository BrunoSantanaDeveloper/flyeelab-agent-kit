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

## 11. Anti-Mock Validation

> [!CAUTION]
> Tests that validate mock data in production pages/routes are INVALID.
> A test passing with `const mockProject = {...}` hardcoded in the page does NOT guarantee the page works with real database data.

**Rules for valid tests:**

| Test Type | MUST Validate | NOT Valid |
|-----------|--------------|-----------|
| **Page (server component)** | DB query returns data → renders | Manually passed mock props |
| **API route** | Request → INSERT/UPDATE in DB → real Response | `return NextResponse.json(mockData)` |
| **Client component** | onClick → calls function → side effect | `onSubmit={() => {}}` as handler |
| **Form** | Submit → API call → user feedback | Form renders but doesn't submit |

**Anti-Mock checklist (before GREEN):**

```markdown
⚠️ ANTI-MOCK CHECK — Task: {title}

[ ] Page/route queries REAL database (not hardcoded)?
[ ] API route persists data (INSERT/UPDATE), not returning mock?
[ ] Click/submit handlers execute REAL action, not noop?
[ ] Test validates END-TO-END behavior, not just rendering?

❌ Mock detected in production → Rewrite with real data
✅ All OK → Valid GREEN
```

**Grep patterns to detect mock violations:**

```bash
# Run in src/ (pages, routes, components):
grep -rn "mockData\|mock_data\|const mock\|// TODO\|// MVP:" src/
grep -rn "() => {}\|onSubmit={() =>" src/
grep -rn "hardcoded\|placeholder" src/
```

> **Historical Lesson:** Project created 140+ tests in ~2h. ALL passed because they tested mock props rendering,
> not real integration. Result: 7 pages marked as "implemented" were completely non-functional with real data.

---

## 12. E2E Core Loop Smoke Test

> [!CAUTION]
> Verification is NOT just test coverage. The agent MUST verify that the product's **CORE LOOP
> works end-to-end** with REAL data, not just that unit tests pass.

**What is the Core Loop?**

Consult PRD section "Core Flow" or "Main Journey" to identify the product's main flow:
```
[Action 1] → [Action 2] → [Action 3] → [Final Result]
```

**Mandatory verification for each Core Loop step:**

```markdown
⚠️ E2E CORE LOOP SMOKE TEST — {project name}

Core Loop from PRD: {describe flow}

| # | Step | Page/Route | Mock? | DB Query? | Functional? |
|---|------|-----------|-------|-----------|-------------|
| 1 | {action 1} | {file} | [ ] | [ ] | [ ] |
| 2 | {action 2} | {file} | [ ] | [ ] | [ ] |
| 3 | {action 3} | {file} | [ ] | [ ] | [ ] |

For EACH step:
[ ] No mock data in production?
[ ] Real DB queries (supabase.from() / prisma)?
[ ] Handlers connected to real actions (not noop)?
[ ] Previous step → current step flow works?

❌ ANY step fails → FIX before deploy
✅ Core Loop 100% functional → Ready for deploy
```

> [!TIP]
> Run the smoke test in the browser (dev server) when possible, not only via unit tests.
> This catches issues that isolated component tests miss.

> **Historical Lesson:** Project had 140+ passing tests and >80% coverage, but core loop
> (create project → create decision → portal → approve) was 100% broken because no test
> verified real integration.

**Decision table:**

| Verification | Action |
|-------------|--------|
| Coverage >= 80% | ✅ Proceed |
| Coverage < 80% | ❌ Add missing tests |
| **E2E Smoke Test FAILED** | ❌ **FIX — main flow is broken** |

---

## 13. Pós-TDD: Sync com Flyee (OBRIGATÓRIO)

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

