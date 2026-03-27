---
description: Debugging command. Activates DEBUG mode for systematic problem investigation.
---

# /debug - Systematic Problem Investigation

$ARGUMENTS

---

## Purpose

This command activates DEBUG mode for systematic investigation of issues, errors, or unexpected behavior.

---

## Agentes Envolvidos

- `debugger` - Investigação sistemática e análise de root cause
- `backend-specialist` / `frontend-specialist` / `mobile-developer` - Conforme domínio do erro
- `test-engineer` - Para criar testes de regressão após correção

---

## Etapa 0: Flyee Sync (OBRIGATÓRIO — ANTES de qualquer código)

> [!CAUTION]
> Toda investigação de bug DEVE ser registrada no Flyee antes de iniciar qualquer fix.
> Se `flyee.json` não existir ou `enabled: false`, informar o usuário.

```bash
python3 .agent/flyee-bridge/bridge.py --create-task \
  --name "Bug: <descrição curta do problema>" \
  --type generic \
  --description "<sintoma observado, arquivo afetado, passos para reproduzir>" \
  --priority high
```

> Salvar o `task_id` retornado — será usado nas etapas seguintes.

---

## Etapa 1: Gather Information

- Error message / sintoma visível
- Reproduction steps
- Expected vs actual behavior
- Recent changes that may have caused it

---

## Etapa 2: Form Hypotheses

- List possible causes
- Order by likelihood

---

## Etapa 3: Investigate Systematically

- Test each hypothesis
- Check logs, data flow
- Use elimination method

---

## Etapa 4: Fix and Prevent

- Apply fix
- Explain root cause
- Add prevention measures

---

## Etapa 5: QA Test Gate (BLOQUEANTE — ANTES de marcar concluído)

> [!CAUTION]
> O bug NÃO pode ser marcado como concluído sem gerar e executar testes.
> Seguir heurísticas de `@[skills/qa-test-generation]`.

1. **Transicionar status para `testing`:**
```bash
python3 .agent/flyee-bridge/bridge.py --update-task <task_id> --status testing
```

2. **Gerar checklist de testes:**
```bash
python3 .agent/flyee-bridge/bridge.py --generate-tests <task_id>
```

3. **Rodar testes automáticos** (TypeScript, Vitest, Playwright — conforme stack):
```bash
python3 .agent/flyee-bridge/bridge.py --report-test <task_id> <step_id> passed|failed ["comment"]
```

4. **Verificar gate:**
```bash
python3 .agent/flyee-bridge/bridge.py --test-summary <task_id>
```

- `all_passed == true` → ✅ prosseguir para Etapa 6
- `all_passed == false` → ❌ BLOQUEAR — corrigir testes antes de concluir

> Se o usuário solicitar skip (ex: hotfix urgente), registrar como `skipped` com aviso de quality debt.

> [!IMPORTANT]
> **Para bugs de UI:** orientar o usuário a reproduzir o bug pelo caminho real da aplicação.
> Exemplo: abrir a tela de tasks de um projeto → clicar nos 3 pontos de uma task → selecionar uma opção que abre modal → fechar o modal → verificar se a tela continua responsiva.

---

## Etapa 6: Conclusão — /task-complete

> Após testes aprovados, executar obrigatoriamente:

```
/task-complete <task_id> "<tempo_gasto>"
```

Isso sincroniza o status, adiciona nota de conclusão e comentário rico no Flyee.

---

## Output Format

```markdown
## 🔍 Debug: [Issue]

### 1. Symptom
[What's happening]

### 2. Information Gathered
- Error: `[error message]`
- File: `[filepath]`
- Line: [line number]

### 3. Hypotheses
1. ❓ [Most likely cause]
2. ❓ [Second possibility]
3. ❓ [Less likely cause]

### 4. Investigation

**Testing hypothesis 1:**
[What I checked] → [Result]

**Testing hypothesis 2:**
[What I checked] → [Result]

### 5. Root Cause
🎯 **[Explanation of why this happened]**

### 6. Fix
```[language]
// Before
[broken code]

// After
[fixed code]
```

### 7. Prevention
🛡️ [How to prevent this in the future]
```

---

## Examples

```
/debug login not working
/debug API returns 500
/debug form doesn't submit
/debug modal freezes the screen
```

---

## Key Principles

- **Register first** - create Flyee task before touching code
- **Ask before assuming** - get full error context
- **Test hypotheses** - don't guess randomly
- **Explain why** - not just what to fix
- **Prevent recurrence** - add tests, validation
- **No completion without tests** - QA gate is mandatory
