---
description: Create new workflow (can invoke create-agent)
---

# /create-workflow

> Interactively create a new workflow. Can invoke /create-agent if a new specialist is needed.

## 1. Purpose
1.  **Trigger**: "What is the slash command?" (e.g., `/deploy-aws`)
2.  **Goal**: "What problem does this workflow solve?"

> **Note:** All workflows are created in `.agent/workflows/` (global scope). The `.agent/` directory is immutable per project.

## 2. Agent Check
1.  **Required expertise**: "Which agents are needed to execute this?"
2.  **Gap Analysis**: "Do these agents exist?"
    - If NO: Invoke `/create-agent` to create the missing specialist.

## 3. Flow Design
1.  **Phases**: "What are the main phases?"
2.  **Steps**: "List the key steps for each phase."
3.  **Inputs/Outputs**: "What inputs are needed? What artifacts are produced?"

## 4. Execution
1.  **Target Directory**: `.agent/workflows/`
2.  **Read Template**: `.agent/templates/workflow-template.md`
3.  **Generate File**: Write `{command}.md` in the target directory.

## Example
```bash
/create-workflow
```
