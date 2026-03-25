# Antigravity Kit Architecture

> Comprehensive AI Agent Capability Expansion Toolkit

---

## 📋 Overview

Antigravity Kit is a modular system consisting of:

- **21 Specialist Agents** - Role-based AI personas
- **37 Skills** - Domain-specific knowledge modules
- **15 Workflows** - Slash command procedures (3 Creation Workflows)
- **4 Templates** - Document templates (Skill, Agent, Workflow, TDD)

---

## 🏗️ Directory Structure

```plaintext
.agent/                      # Kit (cloned from shared repo) - IMMUTABLE
├── ARCHITECTURE.md          
├── agents/
│   └── *.md                 # Global agents (shared)
├── skills/
│   └── */                   # Global skills (shared)
├── workflows/
│   └── *.md                 # Global workflows (shared)
├── templates/               
├── rules/                   
└── scripts/                 
```

## 📁 Project-Specific Customizations

The `.agent/` directory is **IMMUTABLE** and should not be modified by projects.

For project-specific customizations, use the `docs/` directory in the project root:

| Location | Use Case | Example |
|----------|----------|---------|
| `docs/flows/` | Process documentation | `cadastro-produtos.md` |
| `docs/architecture/` | Architecture decisions | `auth-system.md` |
| `docs/INDEX.md` | Central documentation catalog | - |

> **ℹ️ Note:** Use the `/document` workflow to create project-specific documentation.

### Documentation Discovery

The `/new-task` and `/document` workflows automatically:
1. Check `docs/INDEX.md` for existing documentation
2. Load context from `docs/flows/` for the affected module
3. Prompt to create documentation if missing
4. **Backlog Support:** Use `/new-task --backlog` to only register the task without immediate implementation.

## Agent Loading Priority

1. **`docs/`** (Project Documentation) - Context for implementation
2. **Global** (Kit) - Agent behavior and skills


---

## 🤖 Agents (21)

Specialist AI personas for different domains.

| Agent | Focus | Skills Used |
| ----- | ----- | ----------- |
| `orchestrator` | Multi-agent coordination | parallel-agents, behavioral-modes |
| `project-planner` | Discovery, task planning | brainstorming, plan-writing, architecture |
| `frontend-specialist` | Web UI/UX | frontend-design, nextjs-react-expert, tailwind-patterns |
| `backend-specialist` | API, business logic | api-patterns, nodejs-best-practices, database-design |
| `database-architect` | Schema, SQL | database-design, prisma-expert |
| `mobile-developer` | iOS, Android, RN | mobile-design |
| `game-developer` | Game logic, mechanics | game-development |
| `devops-engineer` | CI/CD, Docker | deployment-procedures, docker-expert |
| `security-auditor` | Security compliance | vulnerability-scanner, red-team-tactics |
| `penetration-tester` | Offensive security | red-team-tactics |
| `test-engineer` | Testing strategies | testing-patterns, tdd-workflow, webapp-testing |
| `debugger` | Root cause analysis | systematic-debugging |
| `performance-optimizer` | Speed, Web Vitals | performance-profiling |
| `seo-specialist` | Ranking, visibility | seo-fundamentals, geo-fundamentals |
| `documentation-writer` | Manuals, docs | documentation-templates |
| `product-manager` | Requirements, user stories | plan-writing, brainstorming |
| `product-owner` | Strategy, backlog, MVP | plan-writing, brainstorming |
| `qa-automation-engineer` | E2E testing, CI pipelines | webapp-testing, testing-patterns |
| `code-archaeologist` | Legacy code, refactoring | clean-code, code-review-checklist |
| `explorer-agent` | Codebase analysis | - |
| `tdd-reviewer` | TDD review, validation | tdd-validation, brainstorming, architecture |

---

## 🧩 Skills (38)

Modular knowledge domains that agents can load on-demand. based on task context.

### Frontend & UI

| Skill | Description |
| ----- | ----------- |
| `nextjs-react-expert` | React & Next.js performance optimization (Vercel - 57 rules) |
| `web-design-guidelines` | Web UI audit - 100+ rules for accessibility, UX, performance (Vercel) |
| `tailwind-patterns` | Tailwind CSS v4 utilities |
| `frontend-design` | UI/UX patterns, design systems |
| `ui-ux-pro-max` | 50 styles, 21 palettes, 50 fonts |
| `atomic-design` | Stack-agnostic Atomic Design component generation (Atoms, Molecules, Organisms) |

### Backend & API

| Skill | Description |
| ----- | ----------- |
| `api-patterns` | REST, GraphQL, tRPC |
| `nestjs-expert` | NestJS modules, DI, decorators |
| `nodejs-best-practices` | Node.js async, modules |
| `python-patterns` | Python standards, FastAPI |

### Database

| Skill | Description |
| ----- | ----------- |
| `database-design` | Schema design, optimization |
| `prisma-expert` | Prisma ORM, migrations |

### TypeScript/JavaScript

| Skill | Description |
| ----- | ----------- |
| `typescript-expert` | Type-level programming, performance |

### Cloud & Infrastructure

| Skill | Description |
| ----- | ----------- |
| `docker-expert` | Containerization, Compose |
| `deployment-procedures` | CI/CD, deploy workflows |
| `server-management` | Infrastructure management |

### Testing & Quality

| Skill | Description |
| ----- | ----------- |
| `testing-patterns` | Jest, Vitest, strategies |
| `webapp-testing` | E2E, Playwright |
| `tdd-workflow` | Test-driven development |
| `code-review-checklist` | Code review standards |
| `lint-and-validate` | Linting, validation |

### Security

| Skill | Description |
| ----- | ----------- |
| `vulnerability-scanner` | Security auditing, OWASP |
| `red-team-tactics` | Offensive security |

### Architecture & Planning

| Skill | Description |
| ----- | ----------- |
| `app-builder` | Full-stack app scaffolding |
| `architecture` | System design patterns |
| `plan-writing` | Task planning, breakdown |
| `brainstorming` | Socratic questioning |

### Mobile

| Skill | Description |
| ----- | ----------- |
| `mobile-design` | Mobile UI/UX patterns |

### Game Development

| Skill | Description |
| ----- | ----------- |
| `game-development` | Game logic, mechanics |

### SEO & Growth

| Skill | Description |
| ----- | ----------- |
| `seo-fundamentals` | SEO, E-E-A-T, Core Web Vitals |
| `geo-fundamentals` | GenAI optimization |

### Shell/CLI

| Skill | Description |
| ----- | ----------- |
| `bash-linux` | Linux commands, scripting |
| `powershell-windows` | Windows PowerShell |

### Other

| Skill | Description |
| ----- | ----------- |
| `clean-code` | Coding standards (Global) |
| `behavioral-modes` | Agent personas |
| `parallel-agents` | Multi-agent patterns |
| `mcp-builder` | Model Context Protocol |
| `documentation-templates` | Doc formats |
| `i18n-localization` | Internationalization |
| `performance-profiling` | Web Vitals, optimization |
| `tdd-validation` | TDD completeness validation |
| `systematic-debugging` | Troubleshooting |

---

## 🔄 Workflows (22)

Slash command procedures. Invoke with `/command`.

### Project Lifecycle

| Command | Description |
| ------- | ----------- |
| `/new-project` | New project orchestrator (PRD → TDD → Implementation) |
| `/legacy-project` | Legacy project analysis (Documentation → TDD reverso → Tasks) |
| `/discovery` | Full automated flow: brainstorm → TDD → Notion |
| `/demand` | Commercial proposal generation |

### Feature Development

| Command | Description |
| ------- | ----------- |
| `/new-task` | Add or improve features with Notion/Flyee tracking (`--backlog` for registration only) |
| `/execute` | Execute existing Notion task |
| `/tdd` | TDD workflow (create, validate, breakdown) |
| `/prd` | Create Product Requirements Document |
| `/atomic` | Create Atomic Design components (stack-agnostic) |

### Task Management (Notion)

| Command | Description |
| ------- | ----------- |
| `/check-task` | Query task status without execution |
| `/task-update` | Update task progress in Notion |
| `/log` | Record completed work retroactively |

### Utilities

| Command | Description |
| ------- | ----------- |
| `/brainstorm` | Socratic discovery |
| `/create` | Create new features |
| `/debug` | Debug issues |
| `/deploy` | Deploy application |
| `/document` | Document existing flows |
| `/orchestrate` | Multi-agent coordination |
| `/plan` | Task breakdown |
| `/preview` | Preview changes |
| `/status` | Check project status |
| `/test` | Run tests |

### Meta (Creation)

| Command | Description |
| ------- | ----------- |
| `/create-skill` | Create new skill |
| `/create-agent` | Create new specialist |
| `/create-workflow` | Create new workflow |

---

## 🎯 Skill Loading Protocol

```plaintext
User Request → Skill Description Match → Load SKILL.md
                                            ↓
                                    Read references/
                                            ↓
                                    Read scripts/
```

### Skill Structure

```plaintext
skill-name/
├── SKILL.md           # (Required) Metadata & instructions
├── scripts/           # (Optional) Python/Bash scripts
├── references/        # (Optional) Templates, docs
└── assets/            # (Optional) Images, logos
```

### Enhanced Skills (with scripts/references)

| Skill | Files | Coverage |
| ----- | ----- | -------- |
| `typescript-expert` | 5 | Utility types, tsconfig, cheatsheet |
| `ui-ux-pro-max` | 27 | 50 styles, 21 palettes, 50 fonts |
| `app-builder` | 20 | Full-stack scaffolding |

---

## � Scripts (2)

Master validation scripts that orchestrate skill-level scripts.

### Master Scripts

| Script | Purpose | When to Use |
| ------ | ------- | ----------- |
| `checklist.py` | Priority-based validation (Core checks) | Development, pre-commit |
| `verify_all.py` | Comprehensive verification (All checks) | Pre-deployment, releases |

### Usage

```bash
# Quick validation during development
python .agent/scripts/checklist.py .

# Full verification before deployment
python .agent/scripts/verify_all.py . --url http://localhost:3000
```

### What They Check

**checklist.py** (Core checks):

- Security (vulnerabilities, secrets)
- Code Quality (lint, types)
- Schema Validation
- Test Suite
- UX Audit
- SEO Check

**verify_all.py** (Full suite):

- Everything in checklist.py PLUS:
- Lighthouse (Core Web Vitals)
- Playwright E2E
- Bundle Analysis
- Mobile Audit
- i18n Check

For details, see [scripts/README.md](scripts/README.md)

---

## 📊 Statistics

| Metric | Value |
| ------ | ----- |
| **Total Agents** | 21 |
| **Total Skills** | 38 |
| **Total Workflows** | 23 |
| **Total Templates** | 5 |
| **Total Scripts** | 2 (master) + 19 (skill-level) |
| **Coverage** | ~95% web/mobile development |

---

## 📝 Notion Integration

Workflows that integrate with Notion for task management.

### Required Database Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| Título | Title | ✅ | Task name |
| ID | Text | ✅ | Unique identifier (e.g., `1.1`, `M.2`) |
| Épico | Select | ✅ | Logical grouping (e.g., Autenticação, Listagem) |
| Status | Status | ✅ | `A Fazer` → `Em Progresso` → `Concluído` |
| % Progresso | Number | ✅ | 0-100% |
| Categoria | Multi-select | ✅ | Feature, Melhoria, Refatoração, Log, Bug |
| Prioridade | Select | ❌ | P0, P1, P2, P3 |
| Estimativa | Text | ❌ | Time estimate (e.g., "4h") |
| Tempo Gasto | Text | ❌ | Time spent |

### ID Convention

| Source | Format | Example |
|--------|--------|----------|
| `/discovery` | `{Epic}.{Seq}` | `1.1`, `2.3` |
| `/new-task` | `M.{Seq}` | `M.1`, `M.2` |
| `/legacy-project` | `R.{Seq}` or `{module}.{Seq}` | `R.1`, `auth.2` |

### Recommended Views

- **Visão Cliente**: Name, Status, % Progresso only (for client transparency)
- **Por Épico**: Grouped by Épico property
- **Por Prioridade**: Sorted by Prioridade

---

## 🔗 Quick Reference

| Need | Agent | Skills |
| ---- | ----- | ------ |
| Web App | `frontend-specialist` | nextjs-react-expert, frontend-design |
| API | `backend-specialist` | api-patterns, nodejs-best-practices |
| Mobile | `mobile-developer` | mobile-design |
| Database | `database-architect` | database-design, prisma-expert |
| Security | `security-auditor` | vulnerability-scanner |
| Testing | `test-engineer` | testing-patterns, webapp-testing |
| Debug | `debugger` | systematic-debugging |
| Plan | `project-planner` | brainstorming, plan-writing |
