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

| Propriedade | Tipo | Obrigatório | Notas |
|-------------|------|-------------|-------|
| `Nome da tarefa` | title | ✅ Sim | Título da task |
| `Status` | status | ✅ Sim | Options: Não iniciado, Em andamento, Concluído |
| `ID` | rich_text | ✅ Sim | Formato: X.Y (Épico.Task) |
| `Categoria` | multi_select | ✅ Sim | Feature, Bug, Melhoria, Refatoração, Log |
| `Prioridade` | select | ✅ Sim | Alta, Média, Baixa |
| `Épico` | select | ✅ Sim | Módulo/Feature principal (1. Setup, 2. Auth, etc.) |
| `Criado em` | created_time | ✅ Sim | **Automático** - Preenchido pelo Notion |
| `Última edição` | last_edited_time | ✅ Sim | **Automático** - Atualizado a cada modificação |
| `Estimativa` | number | ⚠️ Opcional | Horas estimadas |
| `Nível de esforço` | select | ⚠️ Opcional | XS, S, M, L, XL |
| `Agente` | select | ⚠️ Opcional | backend-specialist, frontend-specialist, etc. |
| `Projeto` | select | ⚠️ Opcional | Nome do projeto |
| `Prazo` | date | ⚠️ Opcional | Data limite |
| `Responsável` | people | ⚠️ Opcional | Quem é responsável |

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

```
Use: mcp_notion-mcp-server_API-patch-block-children
block_id: {page_id}
children: [
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

### 📋 Validar Schema

```json
// Tool: mcp_notion-mcp-server_API-retrieve-a-database
{ "database_id": "{DATABASE_ID}" }
```

### ➕ Criar Task

```json
// Tool: mcp_notion-mcp-server_API-post-page
{
  "parent": { "database_id": "{DATABASE_ID}" },
  "properties": {
    "Nome da tarefa": { "title": [{ "text": { "content": "{nome}" } }] },
    "ID": { "rich_text": [{ "text": { "content": "{X.Y}" } }] },
    "Status": { "status": { "name": "Não iniciado" } },
    "Épico": { "select": { "name": "{N. Nome}" } },
    "Categoria": { "multi_select": [{ "name": "{categoria}" }] },
    "Prioridade": { "select": { "name": "Alta" } },
    "Projeto": { "select": { "name": "{projeto}" } }
  }
}
```

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
    "Status": { "status": { "name": "Concluído" } }
  }
}
```

### 💬 Adicionar Comentário

```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{page_id}" },
  "rich_text": [{ "text": { "content": "✅ {descrição}" } }]
}
```

### 📝 Adicionar Corpo

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [ /* Usar template por categoria */ ]
}
```

---

## 📋 CHECKLIST DE USO

Antes de criar/atualizar task:

- [ ] Database descoberto dinamicamente (não hardcoded)
- [ ] Schema validado com propriedades obrigatórias
- [ ] Categoria detectada corretamente
- [ ] Template de corpo apropriado selecionado
- [ ] Corpo adicionado via `API-patch-block-children` (não propriedade)

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
