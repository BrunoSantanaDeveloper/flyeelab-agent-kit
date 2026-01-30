# 🤖 Flyeelab Agent Kit

> Um framework de agentes, skills e workflows para potencializar o desenvolvimento assistido por IA.

---

## 📦 Instalação

### Em um novo projeto

```bash
git clone https://github.com/BrunoSantanaDeveloper/flyeelab-agent-kit.git .agent
```

---

## 🔄 Atualização

### Atualizar para última versão

```bash
cd .agent
git pull origin main
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
| `/task-update` | **Notion:** Atualização de % e status (sem git) |
| `/plan` | Planejamento estruturado de features |
| `/tdd` | Criar/validar Technical Design Documents |
| `/create` | Criar nova aplicação do zero |
| `/create-workflow` | Criar novo workflow (com opção de criar agentes) |
| `/create-agent` | Criar novo agente especialista |
| `/create-skill` | Criar nova skill (com opção de scripts) |
| `/ui-ux-pro-max` | **Design System:** Criar/atualizar Design Systems e UI |
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
| 🔄 **Atualizar progresso** | `/task-update 1.1 progress "msg"` | Atualiza % progresso no Notion |
| ✅ **Finalizar task** | `/task-update 1.1 done "msg"` | Marca como Feito (100%) no Notion |

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

### 1. Notion Integration (Opcional)

Para usar workflows que integram com Notion (`/discovery`, `/task-update`):

1. Configure o MCP server `notion-mcp-server`
2. Crie um database com as propriedades documentadas em `/discovery`

---

## 📄 Licença

MIT © Bruno Santana

---

> **Dica:** Leia `ARCHITECTURE.md` para entender o sistema completo de agentes, skills e regras.
