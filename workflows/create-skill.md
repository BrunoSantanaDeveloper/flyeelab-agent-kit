---
description: Create new skill with guided dialogue
---

# /create-skill

> Interactively create a new specialized skill in global or local scope.

## 1. Scope & Domain (Socratic)
First, determine where the skill belongs and its purpose:
1.  **Scope**: "Global (`.agent/skills/`) or Local (`project/`, git-ignored)?"
2.  **Domain**: "What is the specific domain or technology?" (e.g., "GraphQL Patterns", "Vitrine Rules")
3.  **Name**: "What should be the folder name?" (kebab-case, e.g., `graphql-patterns`)

## 2. Structure
Ask about the skill's components:
- "Does this skill need auxiliary scripts?"
- "Does it need templates or examples?"

## 3. Content Generation
Ask for core content to populate the template:
- "What are the top 3 core principles?"
- "What are the critical anti-patterns?"
- "Are there specific decision frameworks?"

## 4. Execution
1.  **Target Directory**:
    - Global: `.agent/skills/{name}`
    - Local: `.agent/skills/project/{name}`
2.  **Read Template**: `.agent/templates/skill-template.md`
3.  **Generate File**: Write `SKILL.md` in the target directory with populated content.
4.  **Optional**: 
    - If scripts requested: Create `scripts/` folder and copy `.agent/templates/script-template.py` to `scripts/verify.py`.
    - If examples requested: Create `examples/` folder.

## Example
```bash
/create-skill
# Follow the dialogue
```
