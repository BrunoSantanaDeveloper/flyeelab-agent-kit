---
description: Structured brainstorming for projects and features. Explores multiple options before implementation.
---

# /brainstorm - Structured Idea Exploration

$ARGUMENTS

---

## Purpose

This command activates BRAINSTORM mode for structured idea exploration. Use when you need to explore options before committing to an implementation.

---

## 🔗 Integração com `/new-project`

> [!TIP]
> **Se você quer explorar ideias E depois implementar**, use:
> ```bash
> /new-project --brainstorm [nome]
> ```
> Isso executa o brainstorm como Phase 0 e continua automaticamente para PRD → TDD → Código.

**Use `/brainstorm` standalone quando:**
- Quer apenas explorar ideias sem compromisso de implementar
- Precisa comparar abordagens técnicas para uma decisão
- Está avaliando tecnologias ou arquiteturas

---

## Behavior

When `/brainstorm` is triggered:

**Agentes Envolvidos:**
- `project-planner` - Estruturação e decomposição de opções
- `backend-specialist` / `frontend-specialist` / `mobile-developer` - Conforme domínio técnico
- `security-auditor` - Para avaliar riscos de cada opção

1. **Understand the goal**
   - What problem are we solving?
   - Who is the user?
   - What constraints exist?

2. **Generate options**
   - Provide at least 3 different approaches
   - Each with pros and cons
   - Consider unconventional solutions

3. **Compare and recommend**
   - Summarize tradeoffs
   - Give a recommendation with reasoning

---

## Output Format

```markdown
## 🧠 Brainstorm: [Topic]

### Context
[Brief problem statement]

---

### Option A: [Name]
[Description]

✅ **Pros:**
- [benefit 1]
- [benefit 2]

❌ **Cons:**
- [drawback 1]

📊 **Effort:** Low | Medium | High

---

### Option B: [Name]
[Description]

✅ **Pros:**
- [benefit 1]

❌ **Cons:**
- [drawback 1]
- [drawback 2]

📊 **Effort:** Low | Medium | High

---

### Option C: [Name]
[Description]

✅ **Pros:**
- [benefit 1]

❌ **Cons:**
- [drawback 1]

📊 **Effort:** Low | Medium | High

---

## 💡 Recommendation

**Option [X]** because [reasoning].

What direction would you like to explore?
```

---

## Examples

```
/brainstorm authentication system
/brainstorm state management for complex form
/brainstorm database schema for social app
/brainstorm caching strategy
```

---

## Key Principles

- **No code** - this is about ideas, not implementation
- **Visual when helpful** - use diagrams for architecture
- **Honest tradeoffs** - don't hide complexity
- **Defer to user** - present options, let them decide
