---
description: Update task status (Notion or Local). NO git commits - commits are manual only.
skills: notion-task-patterns
---

# /task-update Workflow

Updates task status in the configured tracker. **Does NOT perform git commits.**

**Agente Envolvido:** `project-planner` (para tracking de progresso)

> [!IMPORTANT]
> **Git commits são exclusivamente manuais pelo usuário.**
> Este workflow atualiza o tracker configurado em `PROJECT-PROGRESS.md` → `Tracker de Tasks`.
> Se `Tracker = Notion`: usa API do Notion. Se `Tracker = Local`: edita `docs/TASKS.md`.

## Usage

```
/task-update <task-id> <type> "<description>"
```

### Parameters:
- `task-id`: Task identifier or keyword (e.g., 1.1, login)
- `type`: Update type (start, progress, done)
- `description`: Description of what was done

---

## Type → Status Mapping

| Type | Status | Ação |
|------|--------|------|
| `start` | Em andamento | Marca início da task |
| `progress` | Em andamento | Registra progresso intermediário |
| `done` | Concluído | Marca task como finalizada |

> [!NOTE]
> `Última edição` é atualizada **automaticamente** pelo Notion a cada modificação.

---

## Steps

### 1. Parse Parameters
Extract task-id, type, and description.

### 1.5. Identificar Modo de Tracking
Ler `PROJECT-PROGRESS.md` → `Tracker de Tasks`.

### 2. Search & Validate Task

**Se Tracker = Notion:**
Use `API-post-search` to find the task.
- Query: `<task-id>`
- Filter: object = page

**Se Tracker = Local:**
Buscar a task em `docs/TASKS.md` pelo nome ou ID.

**VALIDATION STEP:**
Check the `properties` of the found page.
1. **Status**: Must exist. (Type: status)
2. **Última edição**: Must exist. (Type: last_edited_time - automático)

> [!WARNING] Missing Properties?
> If `Status` is missing in the JSON response:
> 1. **STOP** execution.
> 2. Inform the user:
>    ```
>    🛑 Propriedade ausente no Notion!
>    
>    Sua tarefa Notion não tem a coluna: `Status`
>    Por favor, adicione esta coluna no database e tente novamente.
>    ```

### 3. Update Notion Task
**Only proceed if validation passed.**

Determine new status based on type:
- `done`: Status="Concluído" + **Tempo Gasto (OBRIGATÓRIO)**
- `start`: Status="Em andamento" + **Pre-Start Check**
- `progress`: Status="Em andamento"

**Para type=`start`:**
> [!CAUTION]
> Seguir skill `notion-task-patterns` → Seção "GATE DE FINALIZAÇÃO".
> Verificar se há tasks "Em andamento" antes de iniciar nova.

**Para type=`done`:**
> [!CAUTION]
> **OBRIGATÓRIO:** Perguntar `Tempo Gasto` antes de marcar como "Concluído".

```
⏱️ Quanto tempo foi gasto nesta task?
(Ex: "2h30m", "4h", "30m")
```

Execute `API-patch-page`:
```json
{
  "properties": {
    "Status": {"status": {"name": "<New Status>"}},
    // Se type=done, incluir:
    "Tempo Gasto": {"rich_text": [{"text": {"content": "{tempo_informado}"}}]},
    "% Progresso": {"number": 100}
  }
}
```

> [!NOTE]
> `Última edição` será atualizada automaticamente pelo Notion.

### 3.5. Adicionar Nota de Conclusão no Corpo (se type=done — INLINE — NÃO PULAR)

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

### 4. Add Progress Comment
Add a comment documenting what was done:
```
Use: API-create-a-comment
rich_text: [{ "text": { "content": "📝 {description}" } }]
```

### 4.5. 🔔 FLYEE BRIDGE EMIT (Condicional)

> Se `.agent/flyee-bridge/config.json` existe E `enabled: true`:

**Se type=`start`:**
```bash
python .agent/flyee-bridge/bridge.py emit "dev.workflow_started" '{"workflow": "task-update", "task_name": "{task_name}"}'
```

**Se type=`done`:**
```bash
python .agent/flyee-bridge/bridge.py emit "dev.task_completed" '{"workflow": "task-update", "task_name": "{task_name}", "time_spent": "{tempo}"}'
```

> Se bridge não configurado → Pular silenciosamente.

### 5. Report Result
Confirm update with link to task.

---

## Notes

- **No git commits**: All git operations are manual by the user
- **Use during /enhance**: Call this workflow when completing subitems
- **Tracker-aware**: Reads `PROJECT-PROGRESS.md` → `Tracker de Tasks` to determine Notion vs Local mode
- **If Local**: Steps 3, 3.5, 4 are replaced by editing `docs/TASKS.md` checkboxes
