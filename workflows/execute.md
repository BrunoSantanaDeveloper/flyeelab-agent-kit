---
description: Execute existing task (Notion or Local). Searches task by ID or name, updates status, executes, then marks complete.
skills: notion-task-patterns, context-gathering-patterns, project-tracking-patterns, local-verification
---

# /execute - Executar Task Existente

> **Tracker-aware:** Lê `PROJECT-PROGRESS.md` → `Tracker de Tasks` para determinar se busca no Notion ou em `docs/TASKS.md`.

$ARGUMENTS

**Arguments:**

| Flag | Descrição | Exemplo |
|------|-----------|---------|
| `<task-id>` | ID da task (ex: 1.1, 2.3) | `/execute 3.3` |
| `<task-name>` | Nome parcial da task | `/execute "Testes de Regressão"` |
| `--add-tests` | Complementar task com requisitos de testes | `/execute "Emissão Fiscal" --add-tests` |
| `--analyze-tests` | Analisar cobertura de testes existente | `/execute 2.1 --analyze-tests` |

---

## 🎯 PROPÓSITO

Executa uma task **já existente** no Notion (criada via `/discovery` ou manualmente).

> [!IMPORTANT]
> Este workflow **NÃO CRIA** nova task. Ele busca e atualiza uma task existente.

---

## 🔴 FLUXO: Pre-Check → Search → Update → Execute → Complete

### Fase 0: PRE-START CHECK (🚨 OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Seguir skill `notion-task-patterns` → Seção "GATE DE FINALIZAÇÃO".
> Verificar se há tasks "Em andamento" antes de iniciar nova.

**Ações:**
1. Buscar tasks com Status="Em andamento":
   ```json
   // Tool: mcp_notion-mcp-server_API-query-data-source
   {
     "data_source_id": "{DATABASE_ID}",
     "filter": {
       "property": "Status",
       "status": { "equals": "Em andamento" }
     }
   }
   ```

2. **Se encontrar tasks abertas:**
   ```
   ⚠️ TASK EM ANDAMENTO DETECTADA
   
   📋 {nome da task}
   📊 Status: Em andamento
   ⏱️ Tempo Gasto: (não preenchido)
   
   Deseja:
   1. Finalizar esta task primeiro (preencher Tempo Gasto)
   2. Iniciar nova task mesmo assim
   ```

3. **Se usuário escolher finalizar:** Executar Fase 6 (UPDATE STATUS → CONCLUÍDO) na task aberta.
4. **Se usuário escolher continuar:** Prosseguir para Fase 1.

---

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
       "Status": { "status": { "name": "Em andamento" } }
     }
   }
   ```

> [!NOTE]
> `Última edição` é atualizada automaticamente pelo Notion.

#### 🔔 FLYEE BRIDGE EMIT (Condicional)

> Se `.agent/flyee-bridge/config.json` existe E `enabled: true`:

```bash
python .agent/flyee-bridge/bridge.py emit "dev.workflow_started" '{"workflow": "execute", "task_id": "{task_id}", "task_name": "{nome}"}'
```

> Se bridge não configurado → Pular silenciosamente.

---

### Fase 4: EXECUTE (Implementação)

**Agentes:** Conforme especificado na task (backend-specialist, frontend-specialist, etc.)

> [!CAUTION]
> **GATE OBRIGATÓRIO:** Seguir skill `context-gathering-patterns` → seção "PROCESSO DE CONTEXT GATHERING"
> ANTES de implementar. Preencher checklist de evidência e persistir como comentário na task Notion.

**Ações:**
1. **Context Gathering** (skill `context-gathering-patterns`) — ler task + docs + TDD
2. Executar implementação seguindo:
   - User Story como objetivo
   - Critérios de Aceite como checklist
   - Agente recomendado como especialista
3. Durante a execução, usar `/task-update` para atualizações de progresso

---

### Fase 5: VERIFY

**Trigger:** Implementação concluída

**Ações:**
1. Verificar cada item de "Verificação" do corpo da task
2. Rodar testes se aplicável
3. Se tudo OK: prosseguir para Fase 6
4. Se falhar: corrigir e re-verificar

---

### Fase 6: UPDATE STATUS → CONCLUÍDO

**Trigger:** Verificação passou

**Ações:**
1. **PERGUNTAR Tempo Gasto ao usuário:**
   ```
   ⏱️ Quanto tempo foi gasto nesta task?
   (Ex: "2h30m", "4h", "30m")
   ```

2. Atualizar task via `API-patch-page`:
   ```json
   {
     "properties": {
       "Status": { "status": { "name": "Concluído" } },
       "Tempo Gasto": { "rich_text": [{ "text": { "content": "{tempo_informado}" } }] },
       "% Progresso": { "number": 100 }
     }
   }
   ```

> [!CAUTION]
> **OBRIGATÓRIO:** `Tempo Gasto` DEVE ser preenchido. Não marcar "Concluído" sem este campo.

3. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

   ```json
   // Tool: mcp_notion-mcp-server_API-patch-block-children
   {
     "block_id": "{page_id}",
     "children": [
       { "type": "divider", "divider": {} },
       { "type": "callout", "callout": { "icon": { "type": "emoji", "emoji": "✅" }, "rich_text": [{ "type": "text", "text": { "content": "Concluído em {data}" } }] } },
       { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📋 {resumo da implementação}" } }] } },
       { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }] } },
       { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📁 Arquivos: {lista de arquivos modificados}" } }] } }
     ]
   }
   ```

3.5. **🔔 FLYEE BRIDGE EMIT (Condicional):**

    > Se `.agent/flyee-bridge/config.json` existe E `enabled: true`:

    ```bash
    python .agent/flyee-bridge/bridge.py emit "dev.task_completed" '{"workflow": "execute", "task_id": "{task_id}", "task_name": "{nome}", "time_spent": "{tempo_informado}", "files_changed": ["{lista de arquivos}"]}'
    ```

    > Se bridge não configurado → Pular silenciosamente.

4. Adicionar comentário com resumo:
   ```
   API-create-a-comment:
   - page_id: {task_id}
   - rich_text: "✅ Implementado em {data}. Arquivos: {lista}"
   ```
3. Notificar usuário:
   ```
   🚀 TASK CONCLUÍDA
   
   📋 Task: {nome}
   ✅ Status: Concluído
   📂 Arquivos alterados: X, Y, Z
   
   Próxima task recomendada: {próxima P0}
   ```

### Fase 5.5: DOC REFRESH CHECK (Obrigatório)

> [!CAUTION]
> **Após concluir a task**, verificar se os arquivos modificados são referenciados
> em documentação existente. Docs desatualizados = informação errada para devs.

**Ações:**

1. Listar arquivos modificados durante a execução da task
2. Buscar referências em `docs/flows/` e `docs/design/TDD-*.md`:
   ```bash
   grep -rl "{nome_do_arquivo}" docs/flows/ docs/design/ 2>/dev/null
   ```
3. Se **referências encontradas**:
   a. Abrir cada doc e verificar se a descrição corresponde ao estado real pós-mudança
   b. Se divergência → Atualizar o doc localmente
   c. Verificar se a doc existe no Notion (database "Documentação Técnica") e atualizar lá também
4. Se **nenhuma referência** → Registrar "📄 Nenhum doc afetado" no comentário de conclusão

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
| `/execute --add-tests` | Complementar task com testes | **ADICIONA** requisitos de teste |
| `/task-update` | Durante execução | Atualiza status no Notion |

---

## 🧪 MODO --add-tests (Complementar Testes)

> [!IMPORTANT]
> Use este modo para adicionar requisitos de testes a tasks de **features já implementadas**.

### Trigger

```bash
/execute "Testes de Regressão - Emissão Fiscal (Invoicy)" --add-tests
/execute 2.5 --add-tests
```

### Fluxo: Search → Analyze → Generate → Update

---

### Fase A1: SEARCH & LOAD (Igual ao fluxo normal)

1. Buscar task no Notion
2. Carregar corpo da página
3. Verificar se já existe seção "🧪 Testes Necessários"

---

### Fase A2: ANALYZE CODE (Se --add-tests)

**Agente:** `test-engineer`

**Skills:** `testing-patterns`, `webapp-testing`

**Ações:**
1. Identificar arquivos relacionados à task:
   - Ler TDD Ref se disponível
   - Buscar no codebase por arquivos mencionados
2. Analisar código existente:
   - Backend: Services, Controllers, Repositories
   - Frontend: Components, Hooks, Pages
3. Detectar testes existentes:
   - Buscar `*.spec.ts`, `*.test.ts`, `*.test.tsx`
   - Verificar coverage atual

**Output:**
```
📊 ANÁLISE DE CÓDIGO

Arquivos encontrados:
├── Backend (5 arquivos)
│   ├── invoicy.service.ts (567 linhas, 23 métodos)
│   ├── nfe.service.ts (1117 linhas, 14 métodos)
│   └── ...
├── Frontend (0 arquivos)
│   └── N/A (feature sem UI)

Testes existentes:
├── fiscal.e2e-spec.ts (18 testes)
└── Cobertura: 65%

Gaps identificados:
├── ❌ Falta: Unit tests para InvoicyHttpService
├── ❌ Falta: Error handling tests
└── ❌ Falta: Timeout/retry tests
```

---

### Fase A3: GENERATE TEST REQUIREMENTS

**Agente:** `test-engineer`

**Ações:**
1. Para cada arquivo sem cobertura, gerar requisitos:

```markdown
## 🧪 Testes Necessários (Complemento)

### Backend Tests

| Arquivo | Tipo | Testes a Criar |
|---------|------|----------------|
| `invoicy-http.service.ts` | Unit | Timeout handling, retry logic |
| `nfe.service.ts` | Integration | Payload validation, error responses |
| `nfse.service.ts` | Unit | Cancel flow, certificate errors |

### Frontend Tests

| Arquivo | Tipo | Testes a Criar |
|---------|------|----------------|
| N/A | - | Feature sem componentes UI |

> **Justificativa N/A:** Esta feature é backend-only (emissão fiscal via API Invoicy).

### Comandos para Executar

```bash
# Backend
npm run test:e2e -- --grep "Fiscal"
npm run test -- invoicy.service.spec.ts

# Verificação
npm run test:coverage
```
```

---

### Fase A4: UPDATE NOTION (Adicionar ao corpo)

**Ações:**
1. Usar `API-patch-block-children` para **ADICIONAR** (não substituir) ao corpo da task:
   - Seção "🧪 Testes Necessários (Complemento)"
   - Tabelas de Backend e Frontend
   - Comandos de execução
2. Adicionar comentário:
   ```
   📋 Requisitos de testes adicionados em {data}.
   - Backend: X testes identificados
   - Frontend: Y testes identificados (ou N/A com justificativa)
   - Cobertura atual: XX%
   ```

**Output Final:**
```
✅ TESTES COMPLEMENTADOS

📋 Task: "Testes de Regressão - Emissão Fiscal (Invoicy)"

Adicionado ao corpo da task:
- ✓ Seção "🧪 Testes Necessários"
- ✓ 8 testes de backend identificados
- ✓ Frontend: N/A (justificado)
- ✓ Comandos de execução

Para executar a task agora:
> /execute "Testes de Regressão - Emissão Fiscal"
```

---

## 📊 MODO --analyze-tests (Apenas Análise)

> Use para ver status de testes sem modificar a task.

```bash
/execute 2.5 --analyze-tests
```

**Output:** Relatório de cobertura sem atualizar Notion.

---

## ⚠️ REGRAS CRÍTICAS

> [!CAUTION]
> **REGRA BLOQUEANTE:** Este workflow **NÃO PODE TERMINAR** sem atualizar o tracker (Notion ou Local).
> A Fase 6 (UPDATE STATUS → FEITO) é **OBRIGATÓRIA**.

1. **NUNCA criar nova task** - se a task não existir, informar ao usuário
2. **SEMPRE carregar contexto** - ler User Story e ACs (Notion body ou docs/TASKS.md)
3. **SEMPRE atualizar status no INÍCIO** - Em andamento (Notion) ou anotar (Local)
4. **SEMPRE atualizar status no FIM** - Concluído (Notion) ou `[x]` (Local)
5. **Sugerir próxima task** - ao concluir, sugerir próxima task pendente
6. **Com --add-tests:** SEMPRE incluir tanto Backend quanto Frontend (ou justificar N/A)

### Checklist de Finalização (Obrigatório)

Antes de encerrar este workflow, verifique:

- [ ] `API-patch-page` foi chamado com Status = "Concluído" e `% Progresso: 100`?
- [ ] `API-patch-block-children` foi chamado com nota de conclusão no corpo?
- [ ] `API-create-a-comment` foi chamado com resumo da implementação?
- [ ] Usuário foi notificado sobre próxima task recomendada?
- [ ] **(Se --add-tests)** Seção de testes foi adicionada ao corpo?
- [ ] **(Se --add-tests)** Backend E Frontend foram analisados?
- [ ] **Fase 5.5 executada?** Docs impactados verificados e atualizados (local + Notion)?

> [!IMPORTANT]
> Se algum item acima não foi feito, **EXECUTE AGORA** antes de finalizar.
