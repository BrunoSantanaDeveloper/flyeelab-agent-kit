---
description: Execute existing Notion task. Searches task by ID or name, updates status to "Em Progresso", executes, then marks as "Feito".
---

# /execute - Executar Task Existente do Notion

$ARGUMENTS

**Arguments:**

| Flag | Descrição | Exemplo |
|------|-----------|---------|
| `<task-id>` | ID da task (ex: 1.1, 2.3) | `/execute 3.3` |
| `<task-name>` | Nome parcial da task | `/execute "Testes de Regressão"` |

---

## 🎯 PROPÓSITO

Executa uma task **já existente** no Notion (criada via `/discovery` ou manualmente).

> [!IMPORTANT]
> Este workflow **NÃO CRIA** nova task. Ele busca e atualiza uma task existente.

---

## 🔴 FLUXO: Search → Update → Execute → Complete

### Fase 1: SEARCH TASK (Obrigatório)

**Trigger:** Comando `/execute <task-id ou nome>`

**Agente:** `orchestrator`

**Ações:**
1. Buscar task no Notion usando `API-post-search`:
   ```
   query: "{task-id ou nome}"
   filter: { "property": "object", "value": "page" }
   ```
2. Validar que encontrou exatamente 1 task
3. Se encontrar múltiplas:
   ```
   ⚠️ MÚLTIPLAS TASKS ENCONTRADAS
   
   1. [Nome Task 1] - Status: X
   2. [Nome Task 2] - Status: Y
   
   Qual você quer executar? (digite o número)
   ```
4. Se não encontrar:
   ```
   ❌ TASK NÃO ENCONTRADA
   
   Nenhuma task com "{busca}" foi encontrada no Notion.
   
   Dica: Use `/discovery` para criar novas tasks ou verifique o ID.
   ```

---

### Fase 2: LOAD CONTEXT (Carregar Conteúdo)

**Trigger:** Task encontrada

**Ações:**
1. Usar `API-get-block-children` para ler o corpo da página:
   - User Story
   - Critérios de Aceite
   - Verificação
2. Extrair metadados da task:
   - Agente recomendado
   - Ref. TDD
   - Dependências
3. Mostrar resumo ao usuário:
   ```
   ✅ TASK ENCONTRADA
   
   📋 Nome: {nome}
   📄 User Story: {user story}
   🎯 Agente: {agente}
   📊 Status atual: {status}
   
   Iniciando execução...
   ```

---

### Fase 3: UPDATE STATUS → EM PROGRESSO

**Trigger:** Contexto carregado

**Ações:**
1. Atualizar task via `API-patch-page`:
   ```json
   {
     "properties": {
       "Status": { "status": { "name": "Em Progresso" } },
       "% Progresso": { "number": 10 }
     }
   }
   ```

---

### Fase 4: EXECUTE (Implementação)

**Agentes:** Conforme especificado na task (backend-specialist, frontend-specialist, etc.)

**Ações:**
1. Carregar TDD Ref se disponível
2. Executar implementação seguindo:
   - User Story como objetivo
   - Critérios de Aceite como checklist
   - Agente recomendado como especialista
3. Durante a execução, usar `/task-commit` para commits incrementais

---

### Fase 5: VERIFY

**Trigger:** Implementação concluída

**Ações:**
1. Verificar cada item de "Verificação" do corpo da task
2. Rodar testes se aplicável
3. Se tudo OK: prosseguir para Fase 6
4. Se falhar: corrigir e re-verificar

---

### Fase 6: UPDATE STATUS → FEITO

**Trigger:** Verificação passou

**Ações:**
1. Atualizar task via `API-patch-page`:
   ```json
   {
     "properties": {
       "Status": { "status": { "name": "Feito" } },
       "% Progresso": { "number": 100 }
     }
   }
   ```
2. Adicionar comentário com resumo:
   ```
   API-create-a-comment:
   - page_id: {task_id}
   - rich_text: "✅ Implementado em {data}. Arquivos: {lista}"
   ```
3. Notificar usuário:
   ```
   🚀 TASK CONCLUÍDA
   
   📋 Task: {nome}
   ✅ Status: Feito
   📂 Arquivos alterados: X, Y, Z
   
   Próxima task recomendada: {próxima P0}
   ```

---

## Usage Examples

```bash
# Por ID
/execute 1.1
/execute 3.3

# Por nome parcial
/execute "Testes de Regressão"
/execute "Dashboard KPIs"

# Por nome completo
/execute "Testes de Regressão - Emissão Fiscal (Invoicy)"
```

---

## Diferença entre /enhance e /execute

| Comando | Quando usar | O que faz |
|---------|-------------|-----------|
| `/enhance` | Demandas ad-hoc, bugfixes rápidos | **CRIA** nova task no Notion |
| `/execute` | Executar task do TDD/Discovery | **ATUALIZA** task existente |
| `/task-commit` | Durante execução | Commit + atualiza % progresso |

---

## ⚠️ REGRAS

1. **NUNCA criar nova task** - se a task não existir, informar ao usuário
2. **SEMPRE carregar contexto** - ler User Story e ACs do corpo da página
3. **SEMPRE atualizar status** - Em Progresso → Feito
4. **Sugerir próxima task** - ao concluir, sugerir próxima task P0/MUST
