---
description: Create new specialist agent
---

# /create-agent

> Interactively create a new specialist agent. Can invoke /create-skill if needed.

## 1. Scope & Identity
1.  **Scope**: "Global (`.agent/agents/`) or Local (`project/`, git-ignored)?"
2.  **Identity**: "What is the agent's name?" (e.g., `aws-specialist`, `tanavitrine-expert`)
3.  **Trigger**: "What keywords should trigger this agent?"

## 2. Skills Analysis
1.  **Existing**: "Which existing skills should this agent possess?" (List common ones like `clean-code`)
2.  **New**: "Do you need a new specific skill?"
    - If YES: Invoke `/create-skill` first.

## 3. Behavior Definition
1.  **Philosophy**: "What is this agent's core philosophy?"
2.  **Do/Don'ts**: "What are the critical Do's and Don'ts?"
3.  **Questions**: "What must the agent ask before acting?"

## 4. Execution
1.  **Target Directory**:
    - Global: `.agent/agents/`
    - Local: `.agent/agents/project/`
2.  **Read Template**: `.agent/templates/agent-template.md`
3.  **Generate File**: Write `{name}.md` in the target directory.

## Example
```bash
/create-agent --local
```
