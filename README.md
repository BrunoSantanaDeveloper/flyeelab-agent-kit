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

### 🆕 Novo Projeto

| Comando | Descrição |
|---------|-----------|
| `/new-project [nome]` | **Fluxo completo:** PRD → TDD → Testes → Código → Deploy |
| `/new-project --brainstorm [nome]` | Inclui fase de **exploração de ideias** antes do PRD |
| `/new-project --quick [nome]` | Modo **ágil** (sem PRD, direto para TDD) |
| `/new-project --resume` | **Retomar** de onde parou (`PROJECT-PROGRESS.md`) |
| `/discovery` | **Discovery ágil:** TDD + Tasks no Notion (sem PRD formal) |

### 📦 Projeto Legado

| Comando | Descrição |
|---------|-----------|
| `/legacy-project [path]` | **Fluxo completo:** Análise → Docs → TDD Reverso → Melhorias |
| `/legacy-project --scope [módulo]` | Analisar apenas **um módulo** (monorepos) |
| `/legacy-project --resume` | **Retomar** de onde parou (`LEGACY-PROGRESS.md`) |
| `/legacy-project --critical-first` | Priorizar fluxos **críticos** (auth, payment) |
| `/document [fluxo]` | Documentar UM fluxo específico |

### 📝 Documentação e Planejamento

| Comando | Descrição |
|---------|-----------|
| `/prd` | **PRD:** Product Requirements Document (O QUE construir) |
| `/tdd` | **TDD:** Technical Design Document (COMO construir) |
| `/plan` | Planejamento estruturado de features |
| `/brainstorm` | Explorar opções técnicas sem compromisso |

### ✨ Nova Feature (Projeto Existente)

| Comando | Descrição |
|---------|-----------|
| `/enhance [descrição]` | **Melhoria rápida** com tracking no Notion |
| `/enhance --tdd [descrição]` | Modo **TDD obrigatório** (testes antes do código) |
| `/enhance --resume` | **Retomar** de onde parou |
| `/tdd new [feature]` | Criar TDD para nova feature |

### 📈 Notion Integration

| Comando | Descrição |
|---------|-----------|
| `/demand` | **Comercial:** Levantamento de demanda e proposta |
| `/execute` | Executar task existente do Notion |
| `/log` | Registrar trabalho já feito no Notion |
| `/task-update` | Atualizar % e status de task |

### 🛠️ Desenvolvimento

| Comando | Descrição |
|---------|-----------|
| `/create` | Criar nova aplicação (com testes obrigatórios) |
| `/test` | Gerar e rodar testes (TDD Metodologia) |
| `/debug` | Debug sistemático de problemas |
| `/orchestrate` | Coordenar múltiplos agentes |
| `/ui-ux-pro-max` | Design System e UI |

### ⚙️ Meta (Criar novos recursos)

| Comando | Descrição |
|---------|-----------|
| `/create-workflow` | Criar novo workflow |
| `/create-agent` | Criar novo agente especialista |
| `/create-skill` | Criar nova skill |

[Ver todos os workflows →](workflows/)

---

## 🏛️ Matriz de Governança

### Qual workflow usar?

| Situação | Workflow Recomendado |
|----------|----------------------|
| 💡 Ideia vaga, preciso explorar | `/new-project --brainstorm` |
| ✅ Ideia clara, documentação formal | `/new-project` |
| ⚡ Projeto rápido/MVP | `/new-project --quick` ou `/discovery` |
| 📦 Projeto legado para documentar | `/legacy-project` |
| ✨ Nova feature em projeto existente | `/enhance` ou `/tdd new` |
| 💰 Proposta comercial | `/demand` |

### Criação de Tasks no Notion

| Tipo de Demanda | Comando | Rastreamento (Notion) |
|-----------------|---------|-----------------------|
| 💰 **Comercial** | `/demand` | Database "Propostas Comerciais" |
| 🏗️ **Projeto Novo** | `/new-project` → `/tdd breakdown` | Database "Tasks" |
| ⚡ **Melhoria Rápida** | `/enhance` | Database "Tasks" (direto) |

### Execução de Tasks

| Cenário | Comando | O que faz |
|---------|---------|-----------|
| 📋 **Task existe no Notion** | `/execute 1.1` | Busca, executa e atualiza task existente |
| 🔄 **Atualizar progresso** | `/task-update 1.1 progress "msg"` | Atualiza % progresso no Notion |
| ✅ **Finalizar task** | `/task-update 1.1 done "msg"` | Marca como Concluído (100%) no Notion |

---

## 🧠 Skills Populares

| Skill | Uso |
|-------|-----|
| `tdd-workflow` | **TDD Metodologia:** RED-GREEN-REFACTOR |
| `brainstorming` | Perguntas Socráticas |
| `testing-patterns` | Pirâmide de testes, mocking |
| `frontend-design` | Design de interfaces e Design Tokens |
| `mobile-design` | Design mobile-first e Figma Import |
| `clean-code` | Padrões de código limpo |
| `database-design` | Modelagem de dados |
| `api-patterns` | REST, GraphQL, tRPC |
| `tdd-validation` | Validação de TDDs |

[Ver todas as skills →](skills/)

---

## ⚙️ Configuração

### 1. Notion Integration (Recomendado)

Para usar workflows que integram com Notion (`/discovery`, `/enhance`, `/execute`):

1. Configure o MCP server `notion-mcp-server`
2. Crie databases conforme documentação

#### 📊 Padrões de Status (OBRIGATÓRIO)

> [!IMPORTANT]
> Todos os workflows usam esta nomenclatura padronizada:

| Status | Quando usar | % Progresso |
|--------|-------------|-------------|
| `A Fazer` | Task ainda não iniciada | 0% |
| `Em Progresso` | Task em execução | 1-99% |
| `Concluído` | Task finalizada | 100% |

#### 👁️ View "Visão Cliente" (RECOMENDADO)

Para **transparência com o cliente**, crie uma view filtrada no Notion:

**Configuração:**
```
Nome: "📊 Visão Cliente"
Tipo: Table
Filtro: Status ≠ "A Fazer" (opcional)
Propriedades visíveis:
  ✅ Nome (Title)
  ✅ Status
  ✅ % Progresso
  ✅ Previsão (se existir)
  ❌ Agente (ocultar)
  ❌ TDD Ref (ocultar)
  ❌ Categoria (ocultar)
```

**Benefícios:**
- Cliente vê apenas informações relevantes
- Progresso visual claro
- Sem detalhes técnicos confusos

#### 🔗 Agrupamento por Demanda (OPCIONAL)

Para rastrear progresso de uma proposta comercial:

1. Adicione propriedade `Demanda` (Relation) no database de Tasks
2. Link para database "Propostas Comerciais"
3. No `/discovery`, linkar tasks à proposta aprovada

---

## 📄 Licença

MIT © Bruno Santana

---

> **Dica:** Leia `ARCHITECTURE.md` para entender o sistema completo de agentes, skills e regras.
