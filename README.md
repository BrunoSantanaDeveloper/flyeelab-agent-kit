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
| `/discovery` | Da ideia à execução: Brainstorm → TDD → Design → Notion |
| `/plan` | Planejamento estruturado de features |
| `/create` | Criar nova aplicação do zero |
| `/debug` | Debug sistemático de problemas |
| `/orchestrate` | Coordenar múltiplos agentes |
| `/tdd` | Criar/validar Technical Design Documents |
| `/deploy` | Deploy com verificações |
| `/test` | Gerar e rodar testes |

[Ver todos os workflows →](workflows/)

---

## 🧠 Skills Populares

| Skill | Uso |
|-------|-----|
| `brainstorming` | Perguntas Socráticas |
| `clean-code` | Padrões de código limpo |
| `frontend-design` | Design de interfaces web |
| `mobile-design` | Design mobile-first |
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
