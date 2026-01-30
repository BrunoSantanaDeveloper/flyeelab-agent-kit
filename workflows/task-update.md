---
description: Update Notion task status and progress. NO git commits - commits are manual only.
---

# /task-update Workflow

Updates Notion task status and progress. **Does NOT perform git commits.**

**Agente Envolvido:** `project-planner` (para tracking de progresso)

> [!IMPORTANT]
> **Git commits são exclusivamente manuais pelo usuário.**
> Este workflow apenas atualiza o Notion.

## Usage

```
/task-update <task-id> <type> "<description>"
```

### Parameters:
- `task-id`: Task identifier or keyword (e.g., cfop, login)
- `type`: Update type (start, progress, done)
- `description`: Description of what was done

---

## Type → Status Mapping

| Type | Status | % Progresso |
|------|--------|-------------|
| `start` | Em andamento | 10% |
| `progress` | Em andamento | +15% (incremental) |
| `done` | Concluído | 100% |

---

## Steps

### 1. Parse Parameters
Extract task-id, type, and description.

### 2. Search & Validate Task
Use `API-post-search` to find the task.
- Query: `<task-id>`
- Filter: object = page

**VALIDATION STEP:**
Check the `properties` of the found page.
1. **Status**: Must exist. (Type: status)
2. **% Progresso**: Must exist. (Type: number)

> [!WARNING] Missing Properties?
> If `Status` or `% Progresso` are missing in the JSON response:
> 1. **STOP** execution.
> 2. Inform the user:
>    ```
>    🛑 Propriedade ausente no Notion!
>    
>    Sua tarefa Notion não tem a coluna: `% Progresso` (Número)
>    Por favor, adicione esta coluna no database e tente novamente.
>    ```

### 3. Update Notion Task
**Only proceed if validation passed.**

Calculate new values based on type:
- `done`: Status="Concluído", % Progresso=100
- `start`: Status="Em andamento", % Progresso=10
- `progress`: Status="Em andamento", % Progresso=Current+15 (max 95)

Execute `API-patch-page`:
```json
{
  "properties": {
    "Status": {"status": {"name": "<New Status>"}},
    "% Progresso": {"number": <New Progress>}
  }
}
```

### 4. Add Progress Comment
Add a comment documenting what was done:
```
Use: API-create-a-comment
rich_text: [{ "text": { "content": "📝 {description}" } }]
```

### 5. Report Result
Confirm update with link to task.

---

## Notes

- **No git commits**: All git operations are manual by the user
- **Use during /enhance**: Call this workflow when completing subitems
- **Progress tracking**: Each `progress` call adds 15% up to 95% (done = 100%)
