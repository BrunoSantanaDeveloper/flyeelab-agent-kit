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

| Request Type      | Trigger Keywords                                        | Active Tiers                   | Result                                       |
| ----------------- | ------------------------------------------------------- | ------------------------------ | -------------------------------------------- |
| **QUESTION**      | "what is", "how does", "explain"                        | TIER 0 only                    | Text Response                                |
| **SURVEY/INTEL**  | "analyze", "list files", "overview"                     | TIER 0 + Explorer              | Session Intel (No File)                      |
| **SIMPLE CODE**   | "fix", "add", "change" (single file)                    | TIER 0 + TIER 1 (lite)         | **Flyee Sync Gate**                          |
| **COMPLEX CODE**  | "build", "create", "implement", "refactor"              | TIER 0 + TIER 1 (full) + Agent | **Pre-Implementation Gate + {task-slug}.md** |
| **DESIGN/UI**     | "design", "UI", "page", "dashboard"                     | TIER 0 + TIER 1 + Agent        | **Pre-Implementation Gate + {task-slug}.md** |
| **DESIGN AUDIT**  | "verifique", "está de acordo", "compare", "confira ref" | TIER 0 + frontend-specialist   | **Visual Reference Audit Protocol**          |
| **SLASH CMD**     | /create, /orchestrate, /debug, /new-task                | Command-specific flow          | Variable                                     |

> [!CAUTION]
> **TODAS AS ALTERAÇÕES DE CÓDIGO** ativam a sincronização com o Flyee OBRIGATORIAMENTE.
> **COMPLEX CODE e DESIGN/UI** exigem o *Pre-Implementation Gate* completo (Context + History + Flyee Sync).
> **SIMPLE CODE** exige **pelo menos o Flyee Sync (Bridge CLI)** antes de alterar os arquivos.
> **NENHUM CÓDIGO** deve ser alterado sem registro (se `flyee.json` existir).

> [!CAUTION]
> **REGRA ESPECÍFICA `/new-task`:**
> Ao receber `/new-task`, o agente DEVE:
> 1. **LER** o arquivo `.agent/workflows/new-task.md` **INTEIRO** antes de qualquer ação
> 2. **EXECUTAR** o MANDATORY EXECUTION PROTOCOL (seção no topo do workflow)
> 3. **CRIAR** a task no Flyee via `bridge.py --create-task` **ANTES** de escrever código
> 4. **MOSTRAR** o checklist de governança preenchido ao usuário
> 🚫 Pular QUALQUER destes passos = **VIOLAÇÃO**. Mesmo que pareça simples.

> [!CAUTION]  
> **Resource-Aware Context Gathering é OBRIGATÓRIO (Passo 1.5):**  
> Verifique explicitamente `project-resources.json` e execute `--search-context` no Flyee.  
> 🚫 Nunca vá direto para pesquisa de código ou planejamento sem essa validação prévia.

**Comandos OBRIGATÓRIOS (executar e mostrar output):**
```bash
# 1. Resources locais
cat .agent/project-resources.json 2>/dev/null || echo "⚠️ project-resources.json não encontrado"

# 2. Busca semântica no Flyee (substituir keywords)
python3 .agent/flyee-bridge/bridge.py --search-context "<keywords da task>"
```
> 🚫 Se NENHUM dos comandos acima foi executado → **GATE NÃO PASSOU**. Voltar e executar.

---

## 🤖 INTELLIGENT AGENT ROUTING (STEP 2 - AUTO)

> 🔴 **MANDATORY:** Follow `@[skills/intelligent-routing]` for full protocol.

**Quick rules:**

1. **Analyze (Silent)** → Detect domains → **Select Agent(s)** → **Announce** → Apply.
2. Announce: `🤖 **Applying knowledge of @[agent-name]...**`
3. If user mentions `@agent`, use it. Complex tasks → `orchestrator` + Socratic questions.

**Agent Routing Checklist (BEFORE code/design work):**

| Step | Check | If Unchecked |
| ---- | ----- | ------------ |
| 1 | Correct agent identified? | → STOP. Analyze domain. |
| 2 | Agent `.md` file read? | → STOP. Read `.agent/agents/{agent}.md` |
| 3 | Announced `🤖 Applying knowledge...`? | → STOP. Add announcement. |
| 4 | Skills from frontmatter loaded? | → STOP. Check `skills:` field. |

**Project Type Routing:**

| Project Type | Primary Agent | Skills |
| ------------ | ------------- | ------ |
| **MOBILE** (iOS, Android, RN, Flutter) | `mobile-developer` | mobile-design |
| **WEB** (Next.js, React) | `frontend-specialist` | frontend-design |
| **BACKEND** (API, server, DB) | `backend-specialist` | api-patterns, database-design |

> 🔴 **Mobile + frontend-specialist = WRONG.** Mobile = mobile-developer ONLY.

---

## TIER 0: UNIVERSAL RULES (Always Active)

### 🌐 Language Handling

1. **Internally translate** for better comprehension
2. **Respond in user's language**
3. **Code comments/variables** remain in English

### 🧹 Clean Code → `@[skills/clean-code]`

### 📁 File Dependency Awareness

Before modifying ANY file: Check `CODEBASE.md` → Identify dependents → Update ALL together.

### 🧩 Component Classification → `@[skills/design-system-enforcement]` § Component Classification

### 🗺️ System Map → Read `ARCHITECTURE.md` at session start

### 🧠 Read → Understand → Apply

Before coding: (1) What is the GOAL? (2) What PRINCIPLES? (3) How does this DIFFER from generic output?

### 📖 PRE-IMPLEMENTATION GATE 🔴

> [!CAUTION]
> **Antes de PLANEJAR ou IMPLEMENTAR qualquer mudança**, completar gates aplicáveis.
> Isto inclui criação de planos, análise de escopo, e qualquer pesquisa de código para features novas.

| # | Gate | Skill | Quando |
| - | ---- | ----- | ------ |
| 1 | Context Gathering | `@[skills/context-gathering-patterns]` | COMPLEX CODE / DESIGN/UI / NEW FEATURES |
| 2 | History Check | `@[skills/history-check-patterns]` | COMPLEX CODE |
| 3 | Flyee Auto-Sync | `bridge.py --create-task` | SEMPRE (`flyee.json` existe → sync / não existe → informar) |

> [!CAUTION]  
> **Resource-Aware Context Gathering é OBRIGATÓRIO (Passo 1.5):**  
> Verifique explicitamente `project-resources.json` e execute `--search-context` no Flyee.  
> 🚫 Nunca vá direto para pesquisa de código ou planejamento sem essa validação prévia.

**Comandos OBRIGATÓRIOS (executar e mostrar output):**
```bash
# 1. Resources locais
cat .agent/project-resources.json 2>/dev/null || echo "⚠️ project-resources.json não encontrado"

# 2. Busca semântica no Flyee (substituir keywords)
python3 .agent/flyee-bridge/bridge.py --search-context "<keywords da task>"
```
> 🚫 Se NENHUM dos comandos acima foi executado → **GATE NÃO PASSOU**. Voltar e executar.

```markdown
⚠️ PRE-IMPLEMENTATION GATE

[ ] Flyee Sync: Task criada via bridge.py? (OBRIGATÓRIO — se flyee.json não existe, informar usuário)
[ ] Context Gathering: Li task/PRD/TDD? (COMPLEX CODE / DESIGN/UI)
[ ] Resource Discovery LOCAL: Executei cat project-resources.json? (mostrar output)
[ ] Resource Discovery FLYEE: Executei --search-context? (mostrar output)
[ ] History Check: Consultei bugs anteriores? (COMPLEX CODE)

❌ Item obrigatório desmarcado → NÃO PLANEJAR NEM IMPLEMENTAR
```

**Exceções:** QUESTION / SURVEY → Gate não se aplica.
**`flyee.json` ausente:** NÃO é exceção — informar usuário que Flyee não está configurado.

---

## TIER 1: CODE RULES (When Writing Code)

### 🛑 Socratic Gate → `@[skills/brainstorming]`

**MANDATORY** for every request. Quick reference:

| Request Type | Strategy | Action |
| ------------ | -------- | ------ |
| New Feature / Build | Deep Discovery | ASK min. 3 questions |
| Code Edit / Bug Fix | Context Check | Confirm + impact questions |
| Vague / Simple | Clarification | Purpose, Users, Scope |
| Full Orchestration | Gatekeeper | STOP until user confirms |

### 🏁 Final Checklist

**Trigger:** "final checks", "son kontrolleri yap", etc.

```bash
python .agent/scripts/checklist.py .              # Manual Audit
python .agent/scripts/checklist.py . --url <URL>  # Pre-Deploy (Full Suite)
```

Priority: Security → Lint → Schema → Tests → UX → SEO → Lighthouse/E2E

### 🌐 Web Task Protocol

For web tasks: Ask "Deseja executar testes E2E com Playwright agora?"

> Scripts available via `python .agent/skills/<skill>/scripts/<script>.py`
> Full list in `ARCHITECTURE.md` → Scripts section.

### 🎭 Gemini Mode Mapping

| Mode | Agent | Behavior |
| ---- | ----- | -------- |
| **plan** | `project-planner` | 4-phase (ANALYSIS → PLANNING → SOLUTIONING → IMPLEMENTATION) |
| **ask** | — | Focus on understanding. Ask questions. |
| **edit** | `orchestrator` | Execute. Check `{task-slug}.md` first. |

> 🔴 **Edit mode:** Multi-file/structural → Offer `{task-slug}.md`. Single-file → Proceed directly.

### 📝 Flyee Task Tracking → `@[skills/project-tracking-patterns]`

> [!CAUTION]
> **Git commits são exclusivamente manuais pelo usuário.** O agente NÃO faz commits.

**Bridge CLI (quick ref):**
```bash
python3 .agent/flyee-bridge/bridge.py --create-task --name "Nome" --type implement_feature --description "Desc" --priority normal
python3 .agent/flyee-bridge/bridge.py --update-task <id> --status completed --result success
python3 .agent/flyee-bridge/bridge.py --persist-plan "implementation_plan.md" --task-id <id>
```

> **Auto-Save Plan Hook:** Sempre que um plano de implementação (`implementation_plan.md`) for aprovado pelo usuário (fase PLANNING concluída), você **DEVE OBRIGATORIAMENTE** executar o comando `--persist-plan` no bridge CLI. Isso salva o snapshot do documento no Flyee e veda a perda de contexto em sessões futuras.

> **Flyee Detection:**
> - `flyee.json` exists → projeto conectado ao Flyee. Sync OBRIGATÓRIO.
> - `flyee.json` NÃO existe → projeto **não configurado**. Informar e perguntar:
>   `"⚠️ flyee.json não encontrado. Deseja conectar ao Flyee? (Sim/Não)"`
>   - **Se Sim:** Solicitar `api-key` para configurar.
>   - **Se Não:** Gerar automaticamente `flyee.json` com `{"enabled": false, "opted_out": true}`.
> - 🚫 **PROIBIDO** tratar ausência de `flyee.json` como "não aplicável" e pular silenciosamente.

> **Flyee API Error Handling:**
> - Erro 500/502/503 → **RETRY 1x após 5s**
> - Se retry falhar → **INFORMAR USUÁRIO**, não pular silenciosamente
> - 🚫 **PROIBIDO** tratar erro de API como "não bloqueante" e continuar sem sync

### ✅ Task Completion → `@[skills/project-tracking-patterns]` § Seção 7

> [!CAUTION]
> **O ÚNICO caminho para concluir task = `/task-complete`.** Chamadas avulsas a `API-patch-page` são PROIBIDAS.
> Gate POR TASK, não em batch. Gatilhos: "concluído", `[x]`, avançar, `notify_user` com conclusão.

### 🔒 Sub-Phase Verification

> [!CAUTION]
> Fases com sub-fases NÃO podem ser marcadas concluídas sem verificar TODAS.

```
Phase 5: 5.1 Lógica → 5.2 UI → 5.3 Styling (/ui-ux-pro-max) → 5.4 Flyee Sync
→ TODOS obrigatórios antes de Phase 6
```

### 📝 Flyee Task Body Gate (Atomic) 🔴

> Toda criação de task: `API-post-page` → `API-patch-block-children` (corpo com template). Operação atômica.
> Templates por categoria: Bug (Problema+Causa+Fix), Feature (Story+AC), Doc (Escopo+Entregáveis), Test (Escopo+Suites).



### 🚫 Anti-Mock Data → `@[skills/integration-completeness]` § Production Mock Detection

> [!CAUTION]
> Mock data em pages/routes de produção = **PROTÓTIPO**, não implementação.
> Verificar ANTES de marcar task concluída. Detalhes no skill.

---

## TIER 2: DESIGN RULES (Reference)

> Design rules are in the specialist agents, NOT here.

| Task | Read |
| ---- | ---- |
| Web UI/UX | `.agent/agents/frontend-specialist.md` |
| Mobile UI/UX | `.agent/agents/mobile-developer.md` |
| Design Audit | `frontend-specialist.md` → §Visual Reference Audit Protocol |

> 🔴 **Visual Fidelity:** Verify VALUES not EXISTENCE. 9 dimensions. Output tabelado. Evidence in CSS.

---

## 📁 QUICK REFERENCE

- **Agents**: `orchestrator`, `project-planner`, `security-auditor`, `backend-specialist`, `frontend-specialist`, `mobile-developer`, `debugger`, `game-developer`
- **Key Skills**: `clean-code`, `brainstorming`, `intelligent-routing`, `project-tracking-patterns`, `context-gathering-patterns`
- **Verify**: `.agent/scripts/checklist.py`
- **Bridge**: `.agent/flyee-bridge/bridge.py`
