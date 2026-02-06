---
description: Create new application command. Triggers App Builder skill and starts interactive dialogue with user.
---

# /create - Create Application

$ARGUMENTS

---

## Task

This command starts a new application creation process.

### Steps:

1. **Request Analysis**
   - Understand what the user wants
   - If information is missing, use `conversation-manager` skill to ask

2. **Project Planning**
   - Use `project-planner` agent for task breakdown
   - Determine tech stack
   - Plan file structure
   - Create plan file and proceed to building

3. **TDD Metodologia (OBRIGATÓRIO)**
   > [!IMPORTANT]
   > **Antes de implementar, escrever testes.**
   
   - Use `tdd-workflow` skill para cada feature
   - Ciclo: 🔴 RED → 🟢 GREEN → 🔵 REFACTOR
   - Gerar testes com `/test [feature]`

4. **Design System (OBRIGATÓRIO para UI)**
   > [!IMPORTANT]
   > **SKILL OBRIGATÓRIA:** Seguir `ui-ux-discovery` para perguntas granulares.
   > **WORKFLOW:** Executar `/ui-ux-pro-max` para obter recomendações.
   
   **Processo:**
   1. Executar script para obter recomendações
   2. **Fazer perguntas granulares** (cores, tipografia, layout, efeitos, logo)
   3. **AGUARDAR respostas** antes de finalizar
   4. Consolidar decisões e persistir em `design-system/MASTER.md`
   5. AGUARDAR aprovação antes de implementar

5. **Application Building (After Tests + Design System + Approval)**
   - Orchestrate with `app-builder` skill
   - Coordinate expert agents:
     - `database-architect` → Schema
     - `backend-specialist` → API
     - `frontend-specialist` → UI (seguindo Design System)

6. **Verificação de Cobertura (GATE)**
   > [!CAUTION]
   > **Cobertura mínima: 80%** antes de preview.
   
   ```bash
   /test coverage
   ```
   
   Se cobertura < 80%:
   - Identificar áreas não cobertas
   - Adicionar testes faltantes
   - Repetir verificação

7. **Preview**
   - Start with `auto_preview.py` when complete
   - Present URL to user

---

## Usage Examples

```
/create blog site
/create e-commerce app with product listing and cart
/create todo app
/create Instagram clone
/create crm system with customer management
```

---

## Before Starting

If request is unclear, ask these questions:
- What type of application?
- What are the basic features?
- Who will use it?

Use defaults, add details later.
