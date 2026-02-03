---
description: Execute existing Notion task. Searches task by ID or name, updates status to "Em Progresso", executes, then marks as "Feito".
skills: notion-task-patterns, project-tracking-patterns
---

# /execute - Executar Task Existente do Notion

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

---

### Fase 4: EXECUTE (Implementação)

**Agentes:** Conforme especificado na task (backend-specialist, frontend-specialist, etc.)

**Ações:**
1. Carregar TDD Ref se disponível
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
       "Tempo Gasto": { "rich_text": [{ "text": { "content": "{tempo_informado}" } }] }
     }
   }
   ```

> [!CAUTION]
> **OBRIGATÓRIO:** `Tempo Gasto` DEVE ser preenchido. Não marcar "Concluído" sem este campo.

3. Adicionar comentário com resumo:
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
> **REGRA BLOQUEANTE:** Este workflow **NÃO PODE TERMINAR** sem atualizar o Notion.
> A Fase 6 (UPDATE STATUS → FEITO) é **OBRIGATÓRIA** e deve ser executada mesmo que o usuário encerre a conversa.

1. **NUNCA criar nova task** - se a task não existir, informar ao usuário
2. **SEMPRE carregar contexto** - ler User Story e ACs do corpo da página
3. **SEMPRE atualizar status no INÍCIO** - Em andamento
4. **SEMPRE atualizar status no FIM** - Concluído
5. **Sugerir próxima task** - ao concluir, sugerir próxima task P0/MUST
6. **Com --add-tests:** SEMPRE incluir tanto Backend quanto Frontend (ou justificar N/A)

### Checklist de Finalização (Obrigatório)

Antes de encerrar este workflow, verifique:

- [ ] `API-patch-page` foi chamado com Status = "Concluído"?
- [ ] `API-create-a-comment` foi chamado com resumo da implementação?
- [ ] Usuário foi notificado sobre próxima task recomendada?
- [ ] **(Se --add-tests)** Seção de testes foi adicionada ao corpo?
- [ ] **(Se --add-tests)** Backend E Frontend foram analisados?

> [!IMPORTANT]
> Se algum item acima não foi feito, **EXECUTE AGORA** antes de finalizar.
