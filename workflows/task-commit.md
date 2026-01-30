---
description: Commit changes with automatic Notion task update. Updates Status.
---

# /task-commit Workflow

Commits code changes and updates Notion task status automatically.

**Agente Envolvido:** `project-planner` (para tracking de progresso)

## Usage

```
/task-commit <task-id> <type> "<message>"
```

### Parameters:
- `task-id`: Task identifier or keyword (e.g., cfop, login)
- `type`: Commit type (feat, fix, test, docs, refactor, done)
- `message`: Commit message description

---

## Type → Status Mapping

| Type | Status Action |
|------|---------------|
| `start` | Set to **Em andamento** |
| `feat` | Set to **Em andamento** (if not already) |
| `fix` | Set to **Em andamento** (if not already) |
| `done` | Set to **Concluído** |

---

## Steps

### 1. Parse Parameters
Extract task-id, type, and message.

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
- `feat`/`fix`: Status="Em andamento", % Progresso=Current+Progress

Execute `API-patch-page`:
```json
{
  "properties": {
    "Status": {"status": {"name": "<New Status>"}},
    "% Progresso": {"number": <New Progress>}
  }
}
```

### 4. Report Result
Confirm update with link to task.
