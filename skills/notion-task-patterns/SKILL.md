---
name: notion-task-patterns
description: Padrões centralizados para criação e atualização de tasks no Notion. Validação de schema, formato de corpo por categoria, propriedades obrigatórias.
---

# Notion Task Patterns

> **Single Source of Truth** para todos os workflows que manipulam tasks no Notion.

---

## 🎯 PROPÓSITO

Garantir consistência em:
1. **Validação de Schema** - Propriedades obrigatórias
2. **Formato de Corpo** - Template por categoria
3. **API Calls** - Exemplos padronizados

---

## 📋 PROPRIEDADES OBRIGATÓRIAS

> [!IMPORTANT]
> Antes de criar qualquer task, valide se o database possui estas propriedades.

| Propriedade | Tipo | Obrigatório | Notas |
|-------------|------|-------------|-------|
| `Título` | title | ✅ Sim | - |
| `Status` | status | ✅ Sim | Options: A Fazer, Em Progresso, Concluído |
| `% Progresso` | number | ✅ Sim | 0-100 |
| `ID` | rich_text | ✅ Sim | Formato: X.Y ou R.X |
| `Categoria` | multi_select | ✅ Sim | Feature, Bug, Melhoria, Refatoração, Log |
| `Prioridade` | select | ✅ Sim | P0, P1, P2, P3 ou Alta, Média, Baixa |
| `Estimativa` | select | ⚠️ Opcional | XS, S, M, L, XL |
| `Tempo Gasto` | rich_text | ⚠️ Opcional | - |
| `Épico` | select | ⚠️ Opcional | Módulo/Feature principal |
| `Agente` | select | ⚠️ Opcional | backend-specialist, frontend-specialist, etc. |
| `Projeto` | select | ⚠️ Opcional | Nome do projeto |

---

## 🛑 VALIDAÇÃO DE SCHEMA

### Processo Obrigatório

```
1. Buscar database (API-post-search)
2. Recuperar schema (API-retrieve-a-database)
3. Validar propriedades obrigatórias
4. Se faltar → PARAR e notificar usuário
```

### Mensagem de Erro Padrão

```markdown
⚠️ **PROPRIEDADES AUSENTES** no database '{Nome}':

| Propriedade | Tipo Esperado |
|-------------|---------------|
| {nome} | {tipo} |
| {nome} | {tipo} |

**Por favor, crie estas propriedades no Notion antes de continuar.**

[Link para o database]({notion_url})
```

> [!CAUTION]
> **NÃO prossiga** com criação de tasks até que TODAS as propriedades obrigatórias existam.

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

## 🔧 API CALLS PADRÃO

### Buscar Database

```
Use: mcp_notion-mcp-server_API-post-search
query: "Tarefas"
filter: { "property": "object", "value": "data_source" }
```

### Validar Schema

```
Use: mcp_notion-mcp-server_API-retrieve-a-database
database_id: {DATABASE_ID}
```

### Criar Task

```
Use: mcp_notion-mcp-server_API-post-page
parent: { "database_id": "{DATABASE_ID}" }
properties: {
  "{Título}": { "title": [{ "text": { "content": "{nome}" } }] },
  "ID": { "rich_text": [{ "text": { "content": "{X.Y}" } }] },
  "Status": { "status": { "name": "A Fazer" } },
  "% Progresso": { "number": 0 },
  "Categoria": { "multi_select": [{ "name": "{categoria}" }] },
  "Prioridade": { "select": { "name": "{P0-P3}" } }
}
```

### Atualizar Task

```
Use: mcp_notion-mcp-server_API-patch-page
page_id: {page_id}
properties: {
  "Status": { "status": { "name": "Em Progresso" } },
  "% Progresso": { "number": {valor} }
}
```

### Adicionar Corpo

```
Use: mcp_notion-mcp-server_API-patch-block-children
block_id: {page_id}
children: [ ... ] // Usar template por categoria
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
