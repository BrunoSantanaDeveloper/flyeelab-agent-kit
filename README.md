# 🤖 Flyeelab Agent Kit

> Um framework de agentes, skills e workflows para potencializar o desenvolvimento assistido por IA.

---

## 📦 Instalação

### Em um novo projeto (submodule)

```bash
git submodule add https://github.com/BrunoSantanaDeveloper/flyeelab-agent-kit.git .agent
```

### Clone de projeto existente

```bash
git clone --recurse-submodules <url-do-projeto>
```

### Se esqueceu o `--recurse-submodules`

```bash
git submodule update --init --recursive
```

---

## 🔄 Atualização

### Atualizar para última versão

```bash
cd .agent
git pull origin main
cd ..
git add .agent
git commit -m "chore: update .agent submodule"
```

### Atualizar em todos os projetos (script)

```bash
# Em cada projeto
git submodule update --remote .agent
git add .agent && git commit -m "chore: update .agent"
```

---

## 📂 Estrutura

```
.agent/
├── agents/           # 21 agentes especialistas
├── skills/           # 30+ skills modulares
├── workflows/        # 15 workflows automatizados
├── scripts/          # Scripts de automação
├── templates/        # Templates (TDD, etc.)
├── rules/            # Regras globais
└── ARCHITECTURE.md   # Mapa do sistema
```

---

## 🤖 Agentes Disponíveis

| Agente | Especialidade |
|--------|---------------|
| `orchestrator` | Coordenação multi-agente |
| `backend-specialist` | APIs, DB, Node.js |
| `frontend-specialist` | React, UI/UX, Web |
| `mobile-developer` | React Native, Flutter |
| `project-planner` | Planejamento de projetos |
| `debugger` | Debugging sistemático |
| `security-auditor` | Segurança e vulnerabilidades |
| `devops-engineer` | CI/CD, Deploy, Infra |
| `product-owner` | User Stories, Requisitos |
| `tdd-reviewer` | Validação de TDDs |

[Ver todos os agentes →](agents/)

---

## 🔧 Workflows Principais

| Comando | Descrição |
|---------|-----------|
| `/discovery` | **Discovery 2.0:** Reverse Engineering, Figma Import, TDD e Notion |
| `/demand` | **Comercial:** Levantamento de demanda, orçamento e proposta |
| `/execute` | **Notion Execution:** Executa task existente do Notion |
| `/enhance` | **Notion First:** Melhorias rápidas com rastreamento automático |
| `/task-commit` | **Git + Notion:** Commit com atualização automática de % |
| `/plan` | Planejamento estruturado de features |
| `/tdd` | Criar/validar Technical Design Documents |
| `/create` | Criar nova aplicação do zero |
| `/debug` | Debug sistemático de problemas |
| `/orchestrate` | Coordenar múltiplos agentes |
| `/test` | Gerar e rodar testes |

[Ver todos os workflows →](workflows/)

---

## 🏛️ Matriz de Governança

Para onde vai cada demanda?

### Criação de Tasks

| Tipo de Demanda | Comando | Rastreamento (Notion) |
|-----------------|---------|-----------------------|
| 💰 **Comercial / Orçamento** | `/demand` | Database "Propostas Comerciais" |
| 🏗️ **Projeto / Feature Grande** | `/discovery` | Database "Tasks" (via TDD Breakdown) |
| ⚡ **Ajuste Rápido / Melhoria** | `/enhance` | Database "Tasks" (Criação direta) |

### Execução de Tasks

| Cenário | Comando | O que faz |
|---------|---------|-----------|
| 📋 **Task existe no Notion** | `/execute 1.1` | Busca, executa e atualiza task existente |
| 🔄 **Commit incremental** | `/task-commit 1.1 feat "msg"` | Git commit + atualiza % progresso |
| ✅ **Finalizar task** | `/task-commit 1.1 done "msg"` | Git commit + marca como Feito (100%) |

---

## 🧠 Skills Populares

| Skill | Uso |
|-------|-----|
| `brainstorming` | Perguntas Socráticas |
| `frontend-design` | Design de interfaces e Design Tokens |
| `mobile-design` | Design mobile-first e Figma Import |
| `clean-code` | Padrões de código limpo |
| `database-design` | Modelagem de dados |
| `api-patterns` | REST, GraphQL, tRPC |
| `testing-patterns` | Pirâmide de testes |
| `tdd-validation` | Validação de TDDs |

[Ver todas as skills →](skills/)

---

## ⚙️ Configuração

### 1. GEMINI.md (Obrigatório)

Crie um arquivo `GEMINI.md` na raiz do projeto que referencie o kit:

```markdown
---
trigger: always_on
---

# GEMINI.md

> Veja o manual completo em [.agent/ARCHITECTURE.md](.agent/ARCHITECTURE.md)
```

### 2. Notion Integration (Opcional)

Para usar workflows que integram com Notion (`/discovery`, `/task-commit`):

1. Configure o MCP server `notion-mcp-server`
2. Crie um database com as propriedades documentadas em `/discovery`

---

## 🚀 Quick Start

```bash
# 1. Adicione ao projeto
git submodule add https://github.com/BrunoSantanaDeveloper/flyeelab-agent-kit.git .agent

# 2. Use um workflow
# (Na conversa com a IA)
/discovery meu novo projeto

# 3. Ou invoque um agente
# @backend-specialist ajude-me a criar uma API REST
```

---

## 📝 Contribuição

1. Faça edições dentro de `.agent/`
2. Commit dentro do submodule:
   ```bash
   cd .agent
   git add .
   git commit -m "feat: nova skill"
   git push
   ```
3. Atualize a referência no projeto pai:
   ```bash
   cd ..
   git add .agent
   git commit -m "chore: update .agent"
   ```

---

## 📄 Licença

MIT © Bruno Santana

---

> **Dica:** Leia `ARCHITECTURE.md` para entender o sistema completo de agentes, skills e regras.
