---
description: Commit changes with automatic Notion task update. Updates Status and % Progresso.
---

# /task-commit Workflow

Commits code changes and updates Notion task progress automatically.

## Usage

```
/task-commit <task-id> <type> "<message>"
```

### Parameters:
- `task-id`: Task identifier (e.g., 1.1, 2.3, 4.1)
- `type`: Commit type (feat, fix, test, docs, refactor, done)
- `message`: Commit message description

### Examples:
```
/task-commit 1.1 feat "Add initial project structure"
/task-commit 2.3 fix "Resolve OAuth callback issue"
/task-commit 3.2 done "Complete public vitrine page"
```

---

## Type → Progress Mapping

| Type | Status | Δ Progress |
|------|--------|------------|
| `start` | Em Progresso | 0% → 10% |
| `feat` | Em Progresso | +25% |
| `fix` | Em Progresso | +10% |
| `test` | Em Progresso | +15% |
| `docs` | Em Progresso | +5% |
| `refactor` | Em Progresso | +10% |
| `done` | Feito | → 100% |

---

## Steps

### 1. Parse Parameters
Extract task-id, type, and message from the command.

### 2. Search Task in Notion
Use `mcp_notion-mcp-server_API-post-search` to find the task by name containing the task-id.

### 3. Get Current Progress
Use `mcp_notion-mcp-server_API-retrieve-a-page` to get current % Progresso.

### 4. Calculate New Progress
Apply the delta based on type:
- If type is `done` or `complete`, set to 100%
- Otherwise, add delta to current progress (max 100%)

### 5. Update Notion Task
Use `mcp_notion-mcp-server_API-patch-page` with:
```json
{
  "properties": {
    "Status": {"status": {"name": "<status>"}},
    "% Progresso": {"number": <new_progress>}
  }
}
```

// turbo
### 6. Git Commit
Run git commands:
```bash
git add -A
git commit -m "<type>(<task-id>): <message>"
```

### 7. Report Result
Confirm the task update and commit were successful.

---

## Example Execution

User: `/task-commit 1.1 feat "Add Next.js project structure"`

1. Search Notion for task containing "1.1"
2. Get current progress: 0%
3. Type = feat → +25% → new progress = 25%
4. Update Notion: Status = "Em Progresso", % Progresso = 25
5. Run: `git add -A && git commit -m "feat(1.1): Add Next.js project structure"`
6. Report: "✅ Task 1.1 updated (25%) and committed"

---

## Notes for Agents

When completing work on a task, ALWAYS use this workflow to commit:
```
/task-commit <task-id> <type> "<description of what was done>"
```

Use `done` type when the task is 100% complete.
Use `feat`, `fix`, etc. for incremental progress.
