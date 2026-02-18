---
trigger: always_on
---

# GEMINI.md - Antigravity Kit

> This file defines how the AI behaves in this workspace.

---

## CRITICAL: AGENT & SKILL PROTOCOL (START HERE)

> **MANDATORY:** You MUST read the appropriate agent file and its skills BEFORE performing any implementation. This is the highest priority rule.

### 1. Modular Skill Loading Protocol

Agent activated → Check frontmatter "skills:" → Read SKILL.md (INDEX) → Read specific sections.

- **Selective Reading:** DO NOT read ALL files in a skill folder. Read `SKILL.md` first, then only read sections matching the user's request.
- **Rule Priority:** P0 (GEMINI.md) > P1 (Agent .md) > P2 (SKILL.md). All rules are binding.

### 2. Enforcement Protocol

1. **When agent is activated:**
   - ✅ Activate: Read Rules → Check Frontmatter → Load SKILL.md → Apply All.
2. **Forbidden:** Never skip reading agent rules or skill instructions. "Read → Understand → Apply" is mandatory.

---

## 📥 REQUEST CLASSIFIER (STEP 1)

**Before ANY action, classify the request:**

| Request Type     | Trigger Keywords                           | Active Tiers                   | Result                                       |
| ---------------- | ------------------------------------------ | ------------------------------ | -------------------------------------------- |
| **QUESTION**     | "what is", "how does", "explain"           | TIER 0 only                    | Text Response                                |
| **SURVEY/INTEL** | "analyze", "list files", "overview"        | TIER 0 + Explorer              | Session Intel (No File)                      |
| **SIMPLE CODE**  | "fix", "add", "change" (single file)       | TIER 0 + TIER 1 (lite)         | Inline Edit                                  |
| **COMPLEX CODE** | "build", "create", "implement", "refactor" | TIER 0 + TIER 1 (full) + Agent | **Pre-Implementation Gate + {task-slug}.md** |
| **DESIGN/UI**    | "design", "UI", "page", "dashboard"        | TIER 0 + TIER 1 + Agent        | **Pre-Implementation Gate + {task-slug}.md** |
| **SLASH CMD**    | /create, /orchestrate, /debug              | Command-specific flow          | Variable                                     |

> [!CAUTION]
> **COMPLEX CODE e DESIGN/UI** ativam o **Pre-Implementation Gate** (TIER 1) OBRIGATORIAMENTE,
> mesmo quando o usuário NÃO usa um slash command (`/execute`, `/enhance`, etc.).
> Isso inclui: Context Gathering + History Check + Notion Sync.

---

## 🤖 INTELLIGENT AGENT ROUTING (STEP 2 - AUTO)

**ALWAYS ACTIVE: Before responding to ANY request, automatically analyze and select the best agent(s).**

> 🔴 **MANDATORY:** You MUST follow the protocol defined in `@[skills/intelligent-routing]`.

### Auto-Selection Protocol

1. **Analyze (Silent)**: Detect domains (Frontend, Backend, Security, etc.) from user request.
2. **Select Agent(s)**: Choose the most appropriate specialist(s).
3. **Inform User**: Concisely state which expertise is being applied.
4. **Apply**: Generate response using the selected agent's persona and rules.

### Response Format (MANDATORY)

When auto-applying an agent, inform the user:

```markdown
🤖 **Applying knowledge of `@[agent-name]`...**

[Continue with specialized response]
```

**Rules:**

1. **Silent Analysis**: No verbose meta-commentary ("I am analyzing...").
2. **Respect Overrides**: If user mentions `@agent`, use it.
3. **Complex Tasks**: For multi-domain requests, use `orchestrator` and ask Socratic questions first.

### ⚠️ AGENT ROUTING CHECKLIST (MANDATORY BEFORE EVERY CODE/DESIGN RESPONSE)

**Before ANY code or design work, you MUST complete this mental checklist:**

| Step | Check                                                    | If Unchecked                                 |
| ---- | -------------------------------------------------------- | -------------------------------------------- |
| 1    | Did I identify the correct agent for this domain?        | → STOP. Analyze request domain first.        |
| 2    | Did I READ the agent's `.md` file (or recall its rules)? | → STOP. Open `.agent/agents/{agent}.md`      |
| 3    | Did I announce `🤖 Applying knowledge of @[agent]...`?   | → STOP. Add announcement before response.    |
| 4    | Did I load required skills from agent's frontmatter?     | → STOP. Check `skills:` field and read them. |

**Failure Conditions:**

- ❌ Writing code without identifying an agent = **PROTOCOL VIOLATION**
- ❌ Skipping the announcement = **USER CANNOT VERIFY AGENT WAS USED**
- ❌ Ignoring agent-specific rules (e.g., Purple Ban) = **QUALITY FAILURE**

> 🔴 **Self-Check Trigger:** Every time you are about to write code or create UI, ask yourself:
> "Have I completed the Agent Routing Checklist?" If NO → Complete it first.

---

## TIER 0: UNIVERSAL RULES (Always Active)

### 🌐 Language Handling

When user's prompt is NOT in English:

1. **Internally translate** for better comprehension
2. **Respond in user's language** - match their communication
3. **Code comments/variables** remain in English

### 🧹 Clean Code (Global Mandatory)

**ALL code MUST follow `@[skills/clean-code]` rules. No exceptions.**

- **Code**: Concise, direct, no over-engineering. Self-documenting.
- **Testing**: Mandatory. Pyramid (Unit > Int > E2E) + AAA Pattern.
- **Performance**: Measure first. Adhere to 2025 standards (Core Web Vitals).
- **Infra/Safety**: 5-Phase Deployment. Verify secrets security.

### 📁 File Dependency Awareness

**Before modifying ANY file:**

1. Check `CODEBASE.md` → File Dependencies
2. Identify dependent files
3. Update ALL affected files together

### 🗺️ System Map Read

> 🔴 **MANDATORY:** Read `ARCHITECTURE.md` at session start to understand Agents, Skills, and Scripts.

**Path Awareness:**

- Agents: `.agent/` (Project)
- Skills: `.agent/skills/` (Project)
- Runtime Scripts: `.agent/skills/<skill>/scripts/`

### 🧠 Read → Understand → Apply

```
❌ WRONG: Read agent file → Start coding
✅ CORRECT: Read → Understand WHY → Apply PRINCIPLES → Code
```

**Before coding, answer:**

1. What is the GOAL of this agent/skill?
2. What PRINCIPLES must I apply?
3. How does this DIFFER from generic output?

---

## TIER 1: CODE RULES (When Writing Code)

### 📱 Project Type Routing

| Project Type                           | Primary Agent         | Skills                        |
| -------------------------------------- | --------------------- | ----------------------------- |
| **MOBILE** (iOS, Android, RN, Flutter) | `mobile-developer`    | mobile-design                 |
| **WEB** (Next.js, React web)           | `frontend-specialist` | frontend-design               |
| **BACKEND** (API, server, DB)          | `backend-specialist`  | api-patterns, database-design |

> 🔴 **Mobile + frontend-specialist = WRONG.** Mobile = mobile-developer ONLY.

### 🛑 Socratic Gate

**For complex requests, STOP and ASK first:**

### 🛑 GLOBAL SOCRATIC GATE (TIER 0)

**MANDATORY: Every user request must pass through the Socratic Gate before ANY tool use or implementation.**

| Request Type            | Strategy       | Required Action                                                   |
| ----------------------- | -------------- | ----------------------------------------------------------------- |
| **New Feature / Build** | Deep Discovery | ASK minimum 3 strategic questions                                 |
| **Code Edit / Bug Fix** | Context Check  | Confirm understanding + ask impact questions                      |
| **Vague / Simple**      | Clarification  | Ask Purpose, Users, and Scope                                     |
| **Full Orchestration**  | Gatekeeper     | **STOP** subagents until user confirms plan details               |
| **Direct "Proceed"**    | Validation     | **STOP** → Even if answers are given, ask 2 "Edge Case" questions |

**Protocol:**

1. **Never Assume:** If even 1% is unclear, ASK.
2. **Handle Spec-heavy Requests:** When user gives a list (Answers 1, 2, 3...), do NOT skip the gate. Instead, ask about **Trade-offs** or **Edge Cases** (e.g., "LocalStorage confirmed, but should we handle data clearing or versioning?") before starting.
3. **Wait:** Do NOT invoke subagents or write code until the user clears the Gate.
4. **Reference:** Full protocol in `@[skills/brainstorming]`.

### 🏁 Final Checklist Protocol

**Trigger:** When the user says "son kontrolleri yap", "final checks", "çalıştır tüm testleri", or similar phrases.

| Task Stage       | Command                                            | Purpose                        |
| ---------------- | -------------------------------------------------- | ------------------------------ |
| **Manual Audit** | `python .agent/scripts/checklist.py .`             | Priority-based project audit   |
| **Pre-Deploy**   | `python .agent/scripts/checklist.py . --url <URL>` | Full Suite + Performance + E2E |

**Priority Execution Order:**

1. **Security** → 2. **Lint** → 3. **Schema** → 4. **Tests** → 5. **UX** → 6. **Seo** → 7. **Lighthouse/E2E**

**Rules:**

- **Completion:** A task is NOT finished until `checklist.py` returns success.
- **Reporting:** If it fails, fix the **Critical** blockers first (Security/Lint).

### 🌐 Web Task Protocol (Mandatory)

**For ANY web-related task (Frontend, API, Fullstack), regardless of size:**

1. You **MUST** ask the user: "Deseja executar testes E2E com Playwright agora?".
2. If YES: Run `python .agent/scripts/checklist.py . --url <URL>`.
3. If NO: Proceed with standard checklist.

**Available Scripts (12 total):**

| Script                     | Skill                 | When to Use         |
| -------------------------- | --------------------- | ------------------- |
| `security_scan.py`         | vulnerability-scanner | Always on deploy    |
| `dependency_analyzer.py`   | vulnerability-scanner | Weekly / Deploy     |
| `lint_runner.py`           | lint-and-validate     | Every code change   |
| `test_runner.py`           | testing-patterns      | After logic change  |
| `schema_validator.py`      | database-design       | After DB change     |
| `ux_audit.py`              | frontend-design       | After UI change     |
| `accessibility_checker.py` | frontend-design       | After UI change     |
| `seo_checker.py`           | seo-fundamentals      | After page change   |
| `bundle_analyzer.py`       | performance-profiling | Before deploy       |
| `mobile_audit.py`          | mobile-design         | After mobile change |
| `lighthouse_audit.py`      | performance-profiling | Before deploy       |
| `playwright_runner.py`     | webapp-testing        | Before deploy       |

> 🔴 **Agents & Skills can invoke ANY script** via `python .agent/skills/<skill>/scripts/<script>.py`

### 🎭 Gemini Mode Mapping

| Mode     | Agent             | Behavior                                     |
| -------- | ----------------- | -------------------------------------------- |
| **plan** | `project-planner` | 4-phase methodology. NO CODE before Phase 4. |
| **ask**  | -                 | Focus on understanding. Ask questions.       |
| **edit** | `orchestrator`    | Execute. Check `{task-slug}.md` first.       |

**Plan Mode (4-Phase):**

1. ANALYSIS → Research, questions
2. PLANNING → `{task-slug}.md`, task breakdown
3. SOLUTIONING → Architecture, design (NO CODE!)
4. IMPLEMENTATION → Code + tests

> 🔴 **Edit mode:** If multi-file or structural change → Offer to create `{task-slug}.md`. For single-file fixes → Proceed directly.

### 📝 Task Update Protocol (Notion Integration)

**Updates Notion task status and progress. Does NOT perform git commits.**

> [!CAUTION]
> **Git commits são exclusivamente manuais pelo usuário.**
> O agente NÃO faz commits automáticos em nenhum workflow.

```
/task-update <task-id> <type> "<description>"
```

**Type Mapping:**

| Type       | Status       | % Progresso |
| ---------- | ------------ | ----------- |
| `start`    | Em Progresso | 10%         |
| `progress` | Em Progresso | +15%        |
| `done`     | Concluído    | 100%        |

**Examples:**

```bash
/task-update 1.1 progress "Implementado validação de campos"
/task-update 2.3 done "Fluxo OAuth completo"
```

**Rules:**

1. **No Git Commits:** This workflow only updates Notion, not git.
2. **Increment Progress:** Use `progress` for partial updates.
3. **Mark Complete:** Use `done` when task is 100% finished.
4. **Agent Responsibility:** ALL agents use this workflow for task tracking.

### ✅ TASK COMPLETION GATE (MANDATORY) 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de marcar QUALQUER task como "concluída" ou avançar para próxima task,
> o agente DEVE completar TODOS os itens abaixo. NÃO prosseguir sem cumprir.

**Checklist Obrigatório:**

| Check                               | Ação                                       | Workflow               |
| ----------------------------------- | ------------------------------------------ | ---------------------- |
| [ ] Log de Execução exibido?        | Mostrar template com arquivos + critérios  | `/task-complete`       |
| [ ] Notion atualizado?              | Status → Concluído, Tempo Gasto preenchido | `API-patch-page`       |
| [ ] Comentário adicionado?          | Resumo do que foi feito                    | `API-create-a-comment` |
| [ ] PROJECT-PROGRESS.md atualizado? | Tabela de tasks atualizada                 | Editar arquivo         |

**Gatilhos que DEVEM invocar este gate:**

- Dizer "task completa", "concluído", "feito"
- Marcar `[x]` em checklist
- Avançar para próxima task
- Finalizar um épico
- **Chamar `notify_user` com mensagem de conclusão** (ex: "terminei", "implementado", walkthrough gerado)
- **Encerrar sessão de COMPLEX CODE** sem ter passado pelo gate
- **Chamar `API-patch-page` com Status → Concluído** (ex: marcar task como concluída no Notion)

> 🔴 **REGRA DE BATCH:** Ao completar múltiplas tasks em sequência/paralelo,
> o gate DEVE ser executado **POR TASK** (via `/task-complete`), NÃO em batch.
> Cada task = 1 execução de `/task-complete` com seus próprios arquivos, tempo e comentário.

> 🔴 **FALHA QUE GEROU ESTA REGRA (v1):** Sessão de 5 fixes no sistema de assinaturas executada
> sem invocar `/task-complete` porque nenhum gatilho textual foi acionado.
>
> 🔴 **FALHA QUE GEROU REGRA DE BATCH (v2):** Phase 4 do api/ — 6 tasks de documentação
> (#27-#32) marcadas Concluído via `API-patch-page` direto, sem comentário, sem Tempo Gasto,
> sem nota de conclusão. O agente usou `patch-page` em batch, bypassing o gate porque
> o gatilho `API-patch-page` não existia na lista.

**Como executar:**

```bash
/task-complete <task_id> "<tempo_gasto>"
```

**Exemplo:**

```bash
/task-complete 1.1 "30min"
```

> 🔴 **FALHA COMUM:** Concluir código/testes e pular para próxima task sem sync.
> **CORRETO:** Código → Testes → `/task-complete` → Próxima task.

### 🔒 SUB-PHASE VERIFICATION PROTOCOL (MANDATORY)

> [!CAUTION]
> **REGRA CRÍTICA:** Fases com sub-fases (ex: Phase 5) NÃO podem ser marcadas como concluídas sem verificar TODAS as sub-fases.

**Fases com Sub-Fases Obrigatórias:**

| Fase                       | Sub-Fases                                                | Gate               |
| -------------------------- | -------------------------------------------------------- | ------------------ |
| **Phase 5: Implementação** | 5.1 Lógica, 5.2 UI, **5.3 Styling**, **5.4 Notion Sync** | Todas obrigatórias |

**Checklist ANTES de Avançar de Phase 5 para Phase 6:**

```markdown
⚠️ VERIFICAÇÃO OBRIGATÓRIA - Phase 5 Completa?

[ ] 5.1 Backend/Lógica implementado
[ ] 5.2 UI Components criados
[ ] 5.3 UI STYLING aplicado (via /ui-ux-pro-max)
[ ] Design System carregado
[ ] Pre-Delivery Checklist verificado
[ ] Verificação visual feita
[ ] 5.4 Notion SYNC executado
[ ] Tasks atualizadas no Notion

❌ Se QUALQUER item acima estiver desmarcado → NÃO PROSSEGUIR
✅ Se TODOS marcados → Prosseguir para Phase 6
```

**Enforcement:**

1. **Antes de mudar de fase:** Verificar PROJECT-PROGRESS.md
2. **Se sub-fase pendente:** Executar sub-fase antes de prosseguir
3. **Log obrigatório:** Registrar conclusão de cada sub-fase no histórico

### 📋 NOTION TASK VERIFICATION GATE (MANDATORY)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Fases que criam tasks no Notion (ex: Phase 3 Breakdown) NÃO podem
> ser marcadas como concluídas sem verificar que **100% das tasks** têm corpo preenchido.

**Quando aplicar:**

| Fase               | Verificação Obrigatória                           |
| ------------------ | ------------------------------------------------- |
| Phase 3: Breakdown | Todas tasks com body (User Story, AC, References) |
| `/discovery`       | Todas tasks criadas têm corpo                     |
| `/enhance`         | Task criada tem corpo completo                    |

**Processo:**

1. Após criar última task → **NÃO** atualizar PROJECT-PROGRESS.md ainda
2. Executar verificação conforme `@[skills/notion-task-patterns]` → "GATE DE CONCLUSÃO DE FASE"
3. Se tasks incompletas → Completar ANTES de avançar
4. Só então marcar fase como concluída

> 🔴 **FALHA QUE GEROU ESTA REGRA:** Phase 3 foi marcada como concluída com 4 tasks sem corpo.
> Esta verificação é obrigatória para evitar repetição.

### 📝 NOTION TASK BODY GATE (MANDATORY — Atomic) 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE ATÔMICA:** Toda chamada a `API-post-page` que cria uma task
> DEVE ser seguida IMEDIATAMENTE por `API-patch-block-children` com corpo completo.
> **NÃO existe task válida sem corpo.** Isso aplica-se a QUALQUER contexto de criação:
> fases, workflows, fixes avulsos, `/enhance`, `/execute`, ou criação manual.

**Operação atômica obrigatória (2 chamadas em sequência):**

```
1. API-post-page → cria task com propriedades (título, status, categoria...)
2. API-patch-block-children → adiciona corpo com template adequado
```

**Template mínimo do corpo (por categoria):**

| Categoria          | Corpo Obrigatório                                      |
| ------------------ | ------------------------------------------------------ |
| Bug / Segurança    | Problema, Causa Raiz, Fix Aplicado, Arquivos Alterados |
| Feature / Melhoria | User Story, Acceptance Criteria, Referências           |
| Documentação       | Escopo, Entregáveis, Referências                       |
| Testes             | Escopo, Critérios de Cobertura, Suites                 |

**Enforcement:**

1. **Proibido:** Chamar `API-post-page` sem `API-patch-block-children` na sequência
2. **Proibido:** Usar apenas callout/inline notes como substituto do corpo
3. **Se esquecer:** Corrigir ANTES de prosseguir para próximo passo

> 🔴 **FALHA QUE GEROU ESTA REGRA (v3):** Tasks #11 e #12 (P0 Fixes) criadas via
> `API-post-page` + `API-patch-block-children` com apenas callout de conclusão,
> sem corpo estruturado (Problema, Causa, Fix, Arquivos). O agente tratou inline notes
> como corpo, mas não são — corpo é o conteúdo estruturado com template por categoria.

### 📖 PRE-IMPLEMENTATION GATE (MANDATORY for COMPLEX CODE) 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de implementar código classificado como **COMPLEX CODE** ou **DESIGN/UI**,
> o agente DEVE completar os 3 gates abaixo. **Aplica-se MESMO SEM slash command.**

**Gates Obrigatórios:**

| #   | Gate                  | Skill/Workflow                         | Ação                                                |
| --- | --------------------- | -------------------------------------- | --------------------------------------------------- |
| 1   | **Context Gathering** | `@[skills/context-gathering-patterns]` | Ler task Notion + docs relevantes + TDD             |
| 2   | **History Check**     | `@[skills/history-check-patterns]`     | Buscar tasks anteriores, aprender com bugs passados |
| 3   | **Notion Sync**       | `@[skills/notion-task-patterns]`       | Criar ou vincular task existente no Notion          |

**Checklist Mental (ANTES de tocar em código):**

```markdown
⚠️ PRE-IMPLEMENTATION GATE - Passou?

[ ] Context Gathering: Li a task/docs relevantes?
[ ] History Check: Consultei bugs/features anteriores?
[ ] Notion Sync: Task existe/foi criada no Notion?

❌ Se QUALQUER item desmarcado → NÃO IMPLEMENTAR
✅ TODOS marcados → Prosseguir com implementação
```

**Exceções (ÚNICO caso onde o gate pode ser pulado):**

- **SIMPLE CODE** (single file fix) → Gate NÃO obrigatório
- **QUESTION / SURVEY** → Gate NÃO se aplica

> 🔴 **FALHA QUE GEROU ESTA REGRA:** Sessão de 5 fixes no sistema de assinaturas
> executada sem ler Notion, sem consultar docs, e sem sync final — porque as skills
> `context-gathering` e `history-check` só eram referenciadas dentro de workflows formais.

---

## TIER 2: DESIGN RULES (Reference)

> **Design rules are in the specialist agents, NOT here.**

| Task         | Read                            |
| ------------ | ------------------------------- |
| Web UI/UX    | `.agent/frontend-specialist.md` |
| Mobile UI/UX | `.agent/mobile-developer.md`    |

**These agents contain:**

- Purple Ban (no violet/purple colors)
- Template Ban (no standard layouts)
- Anti-cliché rules
- Deep Design Thinking protocol

> 🔴 **For design work:** Open and READ the agent file. Rules are there.

---

## 📁 QUICK REFERENCE

### Agents & Skills

- **Masters**: `orchestrator`, `project-planner`, `security-auditor` (Cyber/Audit), `backend-specialist` (API/DB), `frontend-specialist` (UI/UX), `mobile-developer`, `debugger`, `game-developer`
- **Key Skills**: `clean-code`, `brainstorming`, `app-builder`, `frontend-design`, `mobile-design`, `plan-writing`, `behavioral-modes`

### Key Scripts

- **Verify**: `.agent/scripts/verify_all.py`, `.agent/scripts/checklist.py`
- **Scanners**: `security_scan.py`, `dependency_analyzer.py`
- **Audits**: `ux_audit.py`, `mobile_audit.py`, `lighthouse_audit.py`, `seo_checker.py`
- **Test**: `playwright_runner.py`, `test_runner.py`

---
