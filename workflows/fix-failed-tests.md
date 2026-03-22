---
description: Workflow para corrigir testes falhados. O agente lê falhas, analisa código, aplica fixes e re-testa em loop (máx 3 tentativas automáticas).
---

# /fix-tests

> Corrigir testes falhados de uma task. Loop automático com limite de tentativas.

## Uso

```bash
/fix-tests <task_id>
```

**Exemplo:**
```bash
/fix-tests abc-123-uuid
```

---

## Pré-requisitos

1. A task DEVE ter `meta.test_checklist` preenchido
2. Pelo menos 1 teste com `status: failed` ou `status: pending`
3. Bridge configurado (fallback: usar API diretamente)

---

## Fluxo de Execução

### Step 1: Ler Testes Pendentes/Falhados

```bash
python3 .agent/flyee-bridge/bridge.py --pending-tests <task_id>
```

Separar em dois grupos:
- **Auto tests** (`type: auto`) → agente corrige e re-roda
- **Manual tests** (`type: manual`) → listar para o dev

> Se nenhum teste failing/pending → informar "✅ All tests passed" e encerrar.

### Step 2: Loop de Auto-Fix (máx 3 iterações)

Para cada teste `auto` com status `failed`:

```
2.1: Ler result_comment → entender o que falhou
2.2: Identificar arquivo(s) relacionado(s) ao teste
2.3: Analisar código e aplicar correção
2.4: Re-rodar teste:
     - tsc --noEmit (para testes unit/sdk)
     - vitest run (se configurado)
     - Playwright (se configurado)
2.5: Reportar resultado:
     python3 .agent/flyee-bridge/bridge.py --report-test <task_id> <step_id> passed|failed ["novo comentário"]
```

**Controle de loop:**
```
iteration = 0
MAX_ITERATIONS = 3

while iteration < MAX_ITERATIONS:
    pending = get_pending_auto_tests()
    if len(pending) == 0: break
    
    for test in pending:
        analyze_and_fix(test)
        report_result(test)
    
    iteration += 1

if iteration >= MAX_ITERATIONS:
    ESCALATE → informar dev
```

### Step 3: Regression Detection

Antes de aplicar fix, verificar se mesmo cenário falhou antes:

```bash
python3 .agent/flyee-bridge/bridge.py --search-context "<description do teste falhado>"
```

Se encontrar task anterior com mesmo padrão de falha → consultar solução aplicada anteriormente.

### Step 4: Listar Testes Manuais

Para testes com `type: manual`:

```markdown
## 🔍 Testes Manuais Pendentes

Os seguintes testes requerem validação manual:

| # | Teste | Categoria |
|---|-------|-----------|
| ts-3 | Responsivo no mobile (≤640px) | visual |
| ts-7 | Hover states match DS | visual |

Por favor, teste e marque como passed/failed na UI (TaskDetail → tab "tests").
```

### Step 5: Verificar Resultado Final

```bash
python3 .agent/flyee-bridge/bridge.py --test-summary <task_id>
```

| Resultado | Ação |
|-----------|------|
| `all_passed: true` | ✅ "Todos os testes passando. Task pode ser concluída." |
| `all_passed: false` (só manual) | ⏳ "Testes auto OK. Aguardando validação manual do dev." |
| `all_passed: false` (auto failed after 3 loops) | ❌ Escalar ao dev com detalhes |

### Step 6: Emitir Eventos (se bridge configurado)

```bash
# Para cada teste que passou:
python3 .agent/flyee-bridge/bridge.py emit "qa.test_passed" '{"task_id": "<id>", "step_id": "<step>", "tested_by": "agent"}'

# Para cada teste que falhou (após 3 tentativas):
python3 .agent/flyee-bridge/bridge.py emit "qa.test_failed" '{"task_id": "<id>", "step_id": "<step>", "attempts": 3, "last_error": "<comment>"}'
```

---

## Mensagem Final

```markdown
## 🧪 Fix-Tests Summary — Task {id}

| Métrica | Valor |
|---------|-------|
| Total de testes | {total} |
| ✅ Passed | {passed} |
| ❌ Failed | {failed} |
| ⏭️ Skipped | {skipped} |
| ⏳ Pending (manual) | {pending} |
| 🔄 Auto-fix loops | {iterations}/3 |
| All passed | {yes/no} |

{Se all_passed: "✅ Task pronta para /task-complete"}
{Se não: "❌ Testes ainda falhando. Intervenção manual necessária."}
```

---

## Gatilhos

Este workflow é acionado quando:

- O usuário invoca `/fix-tests <task_id>`
- O usuário solicita "corrigir testes" ou "fix failing tests"
- Etapa 1.7 do `/task-complete` sugere e o dev aceita
- Agent detecta `all_passed == false` durante verificação

> 🔴 **REGRA:** O agente NÃO pode marcar `all_passed` manualmente. Somente o endpoint `PUT /tasks/{id}/test-results` pode alterar o status.
