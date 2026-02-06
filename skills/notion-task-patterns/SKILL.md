---
name: notion-task-patterns
description: Padrões centralizados para criação e atualização de tasks no Notion. Validação de schema, formato de corpo por categoria, propriedades obrigatórias.
---

# Notion Task Patterns

> **Single Source of Truth** para todos os workflows que manipulam tasks no Notion.

---

## 🎯 PROPÓSITO

Garantir consistência em:
1. **Database Padrão** - Sempre usar "Tarefas"
2. **Validação de Schema** - Propriedades obrigatórias
3. **Formato de Corpo** - Template por categoria
4. **API Calls** - Exemplos padronizados
5. **Idioma** - Templates localizados para transparência com cliente

---

## 🌐 IDIOMA DAS TASKS (GATE PRÉ-CRIAÇÃO)

> [!IMPORTANT]
> **REGRA:** Antes de criar tasks, perguntar ao usuário o idioma preferido.
> O objetivo é **transparência com o cliente** - tasks devem ser compreensíveis.

### Pergunta Obrigatória (1x por Projeto)

```markdown
🌐 **Idioma das Tasks no Notion**

Para garantir transparência com o cliente, em qual idioma você prefere que as tasks sejam escritas?

- [ ] 🇧🇷 **Português** (recomendado para clientes brasileiros)
- [ ] 🇺🇸 **English** (recommended for international teams)

Essa escolha afeta:
- Títulos das seções (User Story, Acceptance Criteria, etc.)
- Descrições e critérios de aceite
- Comentários de progresso e conclusão
```

### Quando Perguntar

| Situação | Ação |
|----------|------|
| Novo projeto (`/new-project`, `/discovery`) | ⭐ Perguntar na Phase 3 (antes do Breakdown) |
| Projeto existente sem preferência salva | ⭐ Perguntar antes de criar primeira task |
| Preferência já definida em PROJECT-PROGRESS.md | ✅ Usar idioma salvo |

### Salvar Preferência

Adicionar em `docs/PROJECT-PROGRESS.md`:

```markdown
## Configurações
| Configuração | Valor |
|--------------|-------|
| Idioma Tasks | 🇧🇷 Português |
```

---

## 🔴 DATABASE PADRÃO (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** TODOS os workflows DEVEM buscar o database com nome exato **"Tarefas"**.
> NÃO usar outros databases como "Daily", "Sprint", etc.

### Busca Obrigatória

```
Use: mcp_notion-mcp-server_API-post-search
query: "Tarefas"
filter: { "property": "object", "value": "data_source" }
```

### Validação do Nome

| Resultado da Busca | Ação |
|-------------------|------|
| Encontrou "Tarefas" | ✅ Usar este database |
| Encontrou outro nome | ❌ PARAR e perguntar ao usuário |
| Não encontrou nada | ❌ PARAR e notificar usuário |

### Mensagem se Database Incorreto

```markdown
⚠️ **DATABASE INCORRETO**

Esperado: "Tarefas"
Encontrado: "{nome_encontrado}"

O padrão do projeto exige que tasks sejam criadas no database "Tarefas".

**Opções:**
1. Criar database "Tarefas" no Notion
2. Confirmar que deseja usar "{nome_encontrado}" (não recomendado)
```

---

## 📋 PROPRIEDADES OBRIGATÓRIAS

> [!IMPORTANT]
> Antes de criar qualquer task, valide se o database possui estas propriedades.
> Se QUALQUER propriedade obrigatória estiver ausente, **PARE e notifique o usuário**.

### Na Criação da Task

| Propriedade | Tipo | Obrigatório | Notas |
|-------------|------|-------------|-------|
| `Nome da tarefa` | title | ✅ Sim | Título da task (usado na busca via MCP) |
| `Status` | status | ✅ Sim | Options: Não iniciado, Em andamento, Concluído |
| `ID` | unique_id | ✅ Automático | Autoincremento do Notion (NÃO preencher na criação) |
| `Categoria` | multi_select | ✅ Sim | Feature, Bug, Melhoria, Refatoração, Log |
| `Prioridade` | select | ✅ Sim | Alta, Média, Baixa |
| `Épico` | select | ✅ Sim | Módulo/Feature principal (1. Setup, 2. Auth, etc.) |
| `Estimativa` | number | ✅ Sim | **Horas estimadas** (obrigatório na criação) |
| `% Progresso` | number | ✅ Sim | Percentual de conclusão (0-100) |

### Na Conclusão da Task

| Propriedade | Tipo | Obrigatório | Notas |
|-------------|------|-------------|-------|
| `Tempo Gasto` | rich_text | ✅ Sim | **Tempo real gasto** (ex: "2h30m") - obrigatório ao concluir |

> [!CAUTION]
> **REGRA:** Ao marcar task como "Concluído", **DEVE** preencher `Tempo Gasto`.

### Propriedades Opcionais

| Propriedade | Tipo | Notas |
|-------------|------|-------|
| `Nível de esforço` | select | XS, S, M, L, XL |
| `Agente` | select | backend-specialist, frontend-specialist, etc. |
| `Projeto` | select | Nome do projeto |
| `Prazo` | date | Data limite |
| `Responsável` | people | Quem é responsável |

### Propriedades Automáticas (Read-Only)

> [!NOTE]
> Estas propriedades são **gerenciadas automaticamente** pelo Notion.
> **NÃO** inclua em chamadas de API - elas são read-only.

| Propriedade | Tipo | Comportamento |
|-------------|------|---------------|
| `Criado em` | created_time | Preenchido ao criar página |
| `Última edição` | last_edited_time | Atualizado a cada modificação |

---

## 🔄 CICLO DE VIDA DA TASK

### Fases e Propriedades Obrigatórias

| Fase | Trigger | Propriedades Obrigatórias |
|------|---------|---------------------------|
| **Criação** | `/discovery`, `/new-project`, `/enhance`, `/legacy-project` | `Estimativa` ✅ |
| **Início** | `/execute`, `/task-update start` | `Status` → "Em andamento" |
| **Progresso** | `/task-update progress` | Comentário de progresso |
| **Conclusão** | `/execute`, `/task-update done` | `Status` → "Concluído", `Tempo Gasto` ✅ |

### 🚨 GATE DE SYNC NOTION (OBRIGATÓRIO) ⭐

> [!CAUTION]
> **REGRA BLOQUEANTE:** Quando uma task ou épico é concluído localmente (testes passando, código funcionando),
> o agente **DEVE** atualizar o Notion **ANTES** de prosseguir para próxima task/épico.
> **NUNCA** deixar sync para depois - isso causa inconsistência e falta de transparência.

**Trigger:**
- Testes passando para uma task
- Épico completo (todas tasks do épico concluídas)
- Trabalho manual executado (refatoração, fix, etc.)

**Ação Obrigatória (sequencial):**

1. **Atualizar Status** → "Concluído"
2. **Preencher Tempo Gasto** → Ex: "2h30m"
3. **Adicionar % Progresso** → 100
4. **Adicionar Nota de Conclusão no Corpo** → Append block com resumo

```json
// Tool: mcp_notion-mcp-server_API-patch-page
{
  "page_id": "{page_id}",
  "properties": {
    "Status": { "status": { "name": "Concluído" } },
    "Tempo Gasto": { "rich_text": [{ "text": { "content": "{tempo}" } }] },
    "% Progresso": { "number": 100 }
  }
}
```

**Nota de Conclusão (append ao corpo da task):**

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    {
      "type": "divider",
      "divider": {}
    },
    {
      "type": "callout",
      "callout": {
        "icon": { "type": "emoji", "emoji": "✅" },
        "rich_text": [{ "type": "text", "text": { "content": "Concluído em {data}" } }]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{ "type": "text", "text": { "content": "📋 {resumo da implementação}" } }]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{ "type": "text", "text": { "content": "🧪 Testes: {X} novos ({arquivo}.test.tsx)" } }]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [{ "type": "text", "text": { "content": "📁 Arquivos: {lista de arquivos modificados}" } }]
      }
    }
  ]
}
```

**Mensagem Obrigatória ao Concluir Épico:**

```markdown
✅ **Épico X Completo**

📋 **Tasks concluídas:**
| ID | Task | Tempo |
|----|------|-------|
| #1 | {nome} | {tempo} |
| #2 | {nome} | {tempo} |

🔄 **Synced com Notion:** ✅
📍 **Próximo:** Épico Y - {nome}
```

> [!WARNING]
> **FALHA DETECTADA:** Épicos sendo marcados como "completos" sem atualizar Notion.
> Esta regra existe para EVITAR essa inconsistência.

### 🚨 GATE DE FINALIZAÇÃO (Pre-Start Check)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de iniciar qualquer nova task, o agente DEVE verificar
> se há tasks com Status="Em andamento". Se houver, PERGUNTAR ao usuário.

**Verificação obrigatória:**

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

**Se encontrar tasks abertas:**

```
⚠️ TASK EM ANDAMENTO DETECTADA

📋 {nome da task}
📊 Status: Em andamento
⏱️ Tempo Gasto: (não preenchido)

Deseja:
1. Finalizar esta task primeiro (preencher Tempo Gasto)
2. Iniciar nova task mesmo assim
```

### Regras do Ciclo

1. **CRIAÇÃO:** `Estimativa` é **OBRIGATÓRIO** - não criar task sem este campo
2. **CONCLUSÃO:** `Tempo Gasto` é **OBRIGATÓRIO** - não marcar "Concluído" sem preencher
3. **GATE:** Verificar tasks abertas antes de iniciar nova

---

## 🛑 VALIDAÇÃO DE SCHEMA (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Este processo DEVE ser executado ANTES de criar qualquer task.
> NÃO pule esta validação em nenhuma circunstância.

### Processo de Validação (3 Passos)

**Passo 1 - Buscar Database:**
```
Use: mcp_notion-mcp-server_API-post-search
query: "Tarefas"
filter: { "property": "object", "value": "data_source" }
```

**Passo 2 - Recuperar Schema:**
```
Use: mcp_notion-mcp-server_API-retrieve-a-database
database_id: {DATABASE_ID}
```

**Passo 3 - Validar Propriedades:**
- Verificar se TODAS as propriedades obrigatórias existem
- Se QUALQUER uma estiver ausente → **PARAR**

### Mensagem de Erro OBRIGATÓRIA

Se propriedades estiverem ausentes, exibir:

```markdown
⚠️ **PROPRIEDADES AUSENTES** no database 'Tarefas':

| Propriedade | Tipo Esperado |
|-------------|---------------|
| {nome} | {tipo} |
| {nome} | {tipo} |

**Por favor, crie estas propriedades no Notion antes de continuar.**

🔗 [Abrir database no Notion]({notion_url})

---

**Instruções para criar propriedades:**
1. Abra o database "Tarefas" no Notion
2. Clique em "+" ao lado do último cabeçalho de coluna
3. Adicione cada propriedade com o tipo correto

**AGUARDANDO** confirmação após criar as propriedades...
```

> [!CAUTION]
> **NÃO prossiga** com criação de tasks até que TODAS as propriedades obrigatórias existam.
> O usuário DEVE confirmar que criou as propriedades antes de continuar.

---

## 📝 FORMATO DO CORPO POR CATEGORIA

### Detectar Categoria

| Categoria | Trigger Keywords | Formato |
|-----------|------------------|---------|
| `Feature` | "nova", "criar", "implementar", "adicionar" | User Story |
| `Bug` | "fix", "corrigir", "erro", "bug", "problema" | Bug Report |
| `Melhoria` | "refactor", "melhorar", "otimizar", "limpar" | Plano Técnico |
| `Refatoração` | "débito", "legacy", "modernizar" | Plano Técnico |
| `Log` | trabalho retroativo | Resumo Técnico |

---

### 🎯 Template: FEATURE (User Story)

> **Usar o idioma definido pelo usuário em PROJECT-PROGRESS.md**

#### 🇧🇷 Português (PT-BR)

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    { "heading_2": { "rich_text": [{ "text": { "content": "📖 História do Usuário" } }] } },
    { "paragraph": { "rich_text": [{ "text": { "content": "Como **{persona}**, eu quero **{ação}**, para que **{benefício}**." } }] } },
    
    { "heading_2": { "rich_text": [{ "text": { "content": "✅ Critérios de Aceite" } }] } },
    { "to_do": { "rich_text": [{ "text": { "content": "Dado {contexto}, Quando {ação}, Então {resultado}" } }], "checked": false } },
    { "to_do": { "rich_text": [{ "text": { "content": "Dado {contexto}, Quando {ação}, Então {resultado}" } }], "checked": false } },
    
    { "heading_2": { "rich_text": [{ "text": { "content": "⚠️ Casos Especiais" } }] } },
    { "bulleted_list_item": { "rich_text": [{ "text": { "content": "{caso especial 1}" } }] } },
    { "bulleted_list_item": { "rich_text": [{ "text": { "content": "{caso especial 2}" } }] } },
    
    { "heading_2": { "rich_text": [{ "text": { "content": "🔗 Referências" } }] } },
    { "paragraph": { "rich_text": [{ "text": { "content": "PRD: {link}\nTDD: {link}" } }] } }
  ]
}
```

#### 🇺🇸 English (EN)

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    { "heading_2": { "rich_text": [{ "text": { "content": "📖 User Story" } }] } },
    { "paragraph": { "rich_text": [{ "text": { "content": "As a **{persona}**, I want to **{action}**, so that **{benefit}**." } }] } },
    
    { "heading_2": { "rich_text": [{ "text": { "content": "✅ Acceptance Criteria" } }] } },
    { "to_do": { "rich_text": [{ "text": { "content": "Given {context}, When {action}, Then {outcome}" } }], "checked": false } },
    { "to_do": { "rich_text": [{ "text": { "content": "Given {context}, When {action}, Then {outcome}" } }], "checked": false } },
    
    { "heading_2": { "rich_text": [{ "text": { "content": "⚠️ Edge Cases" } }] } },
    { "bulleted_list_item": { "rich_text": [{ "text": { "content": "{edge case 1}" } }] } },
    { "bulleted_list_item": { "rich_text": [{ "text": { "content": "{edge case 2}" } }] } },
    
    { "heading_2": { "rich_text": [{ "text": { "content": "🔗 References" } }] } },
    { "paragraph": { "rich_text": [{ "text": { "content": "PRD: {link}\nTDD: {link}" } }] } }
  ]
}
```


---

### 🐛 Template: BUG

```
Use: mcp_notion-mcp-server_API-patch-block-children
block_id: {page_id}
children: [
  { "heading_2": { "rich_text": [{ "text": { "content": "🐛 Problema" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "{descrição do bug}" } }] } },
  
  { "heading_2": { "rich_text": [{ "text": { "content": "📋 Passos para Reproduzir" } }] } },
  { "numbered_list_item": { "rich_text": [{ "text": { "content": "{passo 1}" } }] } },
  { "numbered_list_item": { "rich_text": [{ "text": { "content": "{passo 2}" } }] } },
  
  { "heading_2": { "rich_text": [{ "text": { "content": "✅ Critérios de Resolução" } }] } },
  { "to_do": { "rich_text": [{ "text": { "content": "{critério 1}" } }], "checked": false } },
  { "to_do": { "rich_text": [{ "text": { "content": "{critério 2}" } }], "checked": false } },
  
  { "heading_2": { "rich_text": [{ "text": { "content": "🔗 References" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "Related: #{task_id}" } }] } }
]
```

---

### 🔧 Template: MELHORIA / REFATORAÇÃO

```
Use: mcp_notion-mcp-server_API-patch-block-children
block_id: {page_id}
children: [
  { "heading_2": { "rich_text": [{ "text": { "content": "📋 Plano Técnico" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "{descrição técnica}" } }] } },
  
  { "heading_2": { "rich_text": [{ "text": { "content": "✅ Checklist" } }] } },
  { "to_do": { "rich_text": [{ "text": { "content": "{item 1}" } }], "checked": false } },
  { "to_do": { "rich_text": [{ "text": { "content": "{item 2}" } }], "checked": false } },
  
  { "heading_2": { "rich_text": [{ "text": { "content": "📁 Arquivos Afetados" } }] } },
  { "bulleted_list_item": { "rich_text": [{ "text": { "content": "{arquivo 1}" } }] } },
  { "bulleted_list_item": { "rich_text": [{ "text": { "content": "{arquivo 2}" } }] } }
]
```

---

### 📝 Template: LOG (Retroativo)

```
Use: mcp_notion-mcp-server_API-patch-block-children
block_id: {page_id}
children: [
  { "heading_2": { "rich_text": [{ "text": { "content": "📋 Resumo" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "{descrição do trabalho realizado}" } }] } },
  
  { "heading_2": { "rich_text": [{ "text": { "content": "📁 Arquivos Alterados" } }] } },
  { "bulleted_list_item": { "rich_text": [{ "text": { "content": "{arquivo 1}" } }] } }
]
```

---

## 🔌 API TEMPLATES CENTRALIZADOS

> [!IMPORTANT]
> **SINGLE SOURCE OF TRUTH:** Todos os workflows DEVEM usar estes templates.
> Não duplique exemplos de API nos workflows - referencie esta skill.

---

### Status Values (CANÔNICOS)

| Status | Quando Usar | Valor API |
|--------|-------------|-----------|
| **Não iniciado** | Task criada, não começada | `"Não iniciado"` |
| **Em andamento** | Task em execução | `"Em andamento"` |
| **Concluído** | Task finalizada | `"Concluído"` |

> [!NOTE]
> - `Última edição` → Atualizada **automaticamente** a cada modificação
> - `Criado em` → Preenchido **automaticamente** ao criar a página

---

### 🔍 Buscar Database

```json
// Tool: mcp_notion-mcp-server_API-post-search
{
  "query": "Tarefas",
  "filter": { "property": "object", "value": "data_source" }
}
```

### 🔎 Buscar Task por ID (PREFERIDO)

> [!TIP]
> **Método mais preciso:** Use busca por `unique_id` quando souber o ID da task.

```json
// Tool: mcp_notion-mcp-server_API-query-data-source
{
  "data_source_id": "{DATABASE_ID}",
  "filter": {
    "property": "ID",
    "unique_id": {
      "equals": 42
    }
  }
}
```

> [!CAUTION]
> **IMPORTANTE:** Use `"unique_id"` como tipo do filtro, **NÃO** `"number"`.

**Operadores disponíveis:**

| Operador | Uso |
|----------|-----|
| `equals` | Buscar task específica por ID exato |
| `does_not_equal` | Excluir task específica |
| `greater_than` | Tasks após ID X |
| `less_than` | Tasks antes de ID X |
| `greater_than_or_equal_to` | Tasks a partir de ID X |
| `less_than_or_equal_to` | Tasks até ID X |

### 🔎 Buscar Task por Nome (Alternativa)

```json
// Tool: mcp_notion-mcp-server_API-post-search
{
  "query": "{Nome da Task}",
  "filter": { "property": "object", "value": "page" }
}
```

> [!NOTE]
> Busca por nome é menos precisa (pode retornar múltiplos resultados).
> Prefira busca por ID quando disponível.

### 📋 Validar Schema

```json
// Tool: mcp_notion-mcp-server_API-retrieve-a-database
{ "database_id": "{DATABASE_ID}" }
```

### ➕ CRIAR TASK (2 ETAPAS OBRIGATÓRIAS) ⭐

> [!CAUTION]
> **REGRA BLOQUEANTE:** Criação de tasks é um processo de **2 ETAPAS SEQUENCIAIS**.
> Uma task SÓ está completa após AMBAS as etapas. Pular ETAPA 2 = task incompleta.

---

#### ETAPA 1: Criar Página (Propriedades)

```json
// Tool: mcp_notion-mcp-server_API-post-page
{
  "parent": { "database_id": "{DATABASE_ID}" },
  "properties": {
    "Nome da tarefa": { "title": [{ "text": { "content": "{nome}" } }] },
    "Status": { "status": { "name": "Não iniciado" } },
    "Épico": { "select": { "name": "{N. Nome}" } },
    "Categoria": { "multi_select": [{ "name": "{categoria}" }] },
    "Prioridade": { "select": { "name": "Alta" } },
    "Estimativa": { "number": {horas} },
    "% Progresso": { "number": 0 }
  }
}
```

**⚠️ IMPORTANTE:** Salvar o `page_id` retornado (campo `id` na resposta) para ETAPA 2.

---

#### ETAPA 2: Adicionar Corpo (OBRIGATÓRIO)

> [!CAUTION]
> **IMEDIATAMENTE** após ETAPA 1, executar ETAPA 2. NÃO prosseguir para próxima task sem completar esta etapa.

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}", // ID retornado da ETAPA 1
  "children": [ /* Template por categoria - ver seção TEMPLATES */ ]
}
```

---

#### TEMPLATES POR CATEGORIA

**Feature (User Story):**
```json
[
  { "heading_2": { "rich_text": [{ "text": { "content": "📖 User Story" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "As a **{persona}**, I want to **{action}**, so that **{benefit}**." } }] } },
  { "heading_2": { "rich_text": [{ "text": { "content": "✅ Acceptance Criteria" } }] } },
  { "to_do": { "rich_text": [{ "text": { "content": "Given {context}, When {action}, Then {outcome}" } }], "checked": false } },
  { "heading_2": { "rich_text": [{ "text": { "content": "🔗 References" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "TDD: docs/design/TDD-{nome}.md" } }] } }
]
```

**Bug:**
```json
[
  { "heading_2": { "rich_text": [{ "text": { "content": "🐛 Problema" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "{descrição do bug}" } }] } },
  { "heading_2": { "rich_text": [{ "text": { "content": "📋 Passos para Reproduzir" } }] } },
  { "numbered_list_item": { "rich_text": [{ "text": { "content": "{passo 1}" } }] } },
  { "heading_2": { "rich_text": [{ "text": { "content": "✅ Critérios de Resolução" } }] } },
  { "to_do": { "rich_text": [{ "text": { "content": "{critério}" } }], "checked": false } }
]
```

**Log (Trabalho Retroativo):**
```json
[
  { "heading_2": { "rich_text": [{ "text": { "content": "📝 Resumo Técnico" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "{descrição técnica}" } }] } },
  { "heading_2": { "rich_text": [{ "text": { "content": "📁 Arquivos Afetados" } }] } },
  { "bulleted_list_item": { "rich_text": [{ "text": { "content": "{arquivo}" } }] } }
]
```

---

> [!WARNING]
> **FALHA COMUM:** Criar múltiplas tasks com `API-post-page` e só depois adicionar corpos.
> **CORRETO:** Para CADA task: ETAPA 1 → ETAPA 2 → próxima task.

---

#### VERIFICAÇÃO DE CONCLUSÃO

Após criar todas as tasks, verificar:

```
[ ] Todas as tasks criadas com API-post-page
[ ] TODAS as tasks com corpo via API-patch-block-children
[ ] Template correto usado para cada categoria
```

---

## 🚨 GATE DE CONCLUSÃO DE FASE (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Uma fase que cria tasks no Notion SÓ pode ser marcada como "Concluída"
> após verificar que **100% das tasks** têm propriedades E corpo preenchidos.
> **NUNCA** avançar de fase sem completar esta verificação.

### Processo de Verificação (OBRIGATÓRIO)

**Antes de marcar qualquer fase como "Concluída":**

1. **Listar todas as tasks criadas na fase**
2. **Para CADA task, verificar:**
   - [ ] Propriedades obrigatórias preenchidas (Nome, Status, Épico, Categoria, Estimativa)
   - [ ] Corpo adicionado via `API-patch-block-children`
   - [ ] Corpo contém seções obrigatórias (User Story, Acceptance Criteria, References)

3. **Se QUALQUER task estiver incompleta → PARAR e completar antes de avançar**

### Query de Verificação

```json
// Tool: mcp_notion-mcp-server_API-query-data-source
{
  "data_source_id": "{DATABASE_ID}",
  "filter": {
    "property": "ID",
    "unique_id": {
      "greater_than_or_equal_to": {ID_INICIAL},
      "less_than_or_equal_to": {ID_FINAL}
    }
  }
}
```

Para cada task retornada, verificar se tem children/blocks:

```json
// Tool: mcp_notion-mcp-server_API-get-block-children
{
  "block_id": "{page_id}"
}
```

**Se `results` estiver vazio → task SEM corpo → INCOMPLETA**

### Mensagem de Erro OBRIGATÓRIA

Se encontrar tasks incompletas:

```markdown
⚠️ **FASE NÃO PODE SER CONCLUÍDA**

Encontrei {N} task(s) sem corpo preenchido:

| ID | Nome | Status |
|----|------|--------|
| #{id} | {nome} | ❌ Sem corpo |

**Ação obrigatória:** Adicionar corpo a todas as tasks antes de avançar.
```

### Regras do Gate

1. **OBRIGATÓRIO** verificar TODAS as tasks antes de marcar fase como concluída
2. **NUNCA** atualizar PROJECT-PROGRESS.md para próxima fase sem completar verificação
3. **Se falhar**, completar tasks faltantes ANTES de prosseguir
4. **Log obrigatório** em PROJECT-PROGRESS.md: "Phase X: Verificação completa - N tasks"

---

### 🔄 Atualizar Status → Em Andamento

```json
// Tool: mcp_notion-mcp-server_API-patch-page
{
  "page_id": "{page_id}",
  "properties": {
    "Status": { "status": { "name": "Em andamento" } }
  }
}
```

### ✅ Atualizar Status → Concluído

```json
// Tool: mcp_notion-mcp-server_API-patch-page
{
  "page_id": "{page_id}",
  "properties": {
    "Status": { "status": { "name": "Concluído" } },
    "Tempo Gasto": { "rich_text": [{ "text": { "content": "{Xh}m" } }] }
  }
}
```

> [!CAUTION]
> **OBRIGATÓRIO:** `Tempo Gasto` deve ser preenchido ao concluir.

### 💬 Adicionar Comentário de Progresso

```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{page_id}" },
  "rich_text": [{ "text": { "content": "🔄 **Progresso:** {descrição do avanço}" } }]
}
```

### ✅ Comentário de Conclusão (RICO - OBRIGATÓRIO)

> [!IMPORTANT]
> **REGRA:** Ao concluir task, adicionar comentário rico para transparência com cliente.
> Use o idioma definido em PROJECT-PROGRESS.md.

#### 🇧🇷 Português (PT-BR)

```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{page_id}" },
  "rich_text": [{
    "text": {
      "content": "✅ **Task Concluída**\n\n📋 **O que foi feito:**\n• {descrição simples do que foi implementado}\n• {outra funcionalidade se aplicável}\n\n📁 **Arquivos modificados:**\n• {arquivo 1}\n• {arquivo 2}\n\n🔗 **Próximos passos:**\n• {task relacionada ou \"Nenhum - task independente\"}"
    }
  }]
}
```

#### 🇺🇸 English (EN)

```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{page_id}" },
  "rich_text": [{
    "text": {
      "content": "✅ **Task Completed**\n\n📋 **What was done:**\n• {simple description of what was implemented}\n• {another feature if applicable}\n\n📁 **Files modified:**\n• {file 1}\n• {file 2}\n\n🔗 **Next steps:**\n• {related task or \"None - standalone task\"}"
    }
  }]
}
```

> [!TIP]
> **Para transparência:** Use linguagem simples que o cliente entenda.
> Evite jargões técnicos quando possível.


## 📋 CHECKLIST DE USO

Antes de criar/atualizar task:

- [ ] **Idioma definido** em PROJECT-PROGRESS.md (PT-BR ou EN)
- [ ] Database descoberto dinamicamente (não hardcoded)
- [ ] Schema validado com propriedades obrigatórias
- [ ] Categoria detectada corretamente
- [ ] **ETAPA 1:** Task criada via `API-post-page`
- [ ] **ETAPA 2:** Corpo adicionado via `API-patch-block-children` (OBRIGATÓRIO)
- [ ] Template correto usado para categoria (no idioma do projeto)

Ao concluir task:
- [ ] `Status` → "Concluído"
- [ ] `Tempo Gasto` preenchido
- [ ] **Comentário rico** adicionado (no idioma do projeto)

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Operação |
|----------|----------|
| `/discovery` | Criar tasks do TDD |
| `/enhance` | Criar task de melhoria/bug |
| `/tdd breakdown` | Criar tasks do breakdown |
| `/legacy-project` | Criar tasks de refatoração |
| `/log` | Criar task retroativa |
| `/execute` | Atualizar task existente |
| `/new-project` | Criar tasks via breakdown |
| `/task-update` | Atualizar progresso |
