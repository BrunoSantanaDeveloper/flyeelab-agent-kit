# 🤖 Flyeelab Agent Kit

> Um framework de agentes, skills e workflows para potencializar o desenvolvimento assistido por IA.

---

## 📚 Documentação & Tutoriais

Para guias detalhados, tutoriais em vídeo e documentação completa:

| Recurso | Link |
|---------|------|
| 📖 **Documentação Completa** | [flyeelab.com/docs](https://flyeelab.com/docs) |
| 🎬 **Vídeo Tutoriais** | [flyeelab.com/videos](https://flyeelab.com/videos) |
| 🚀 **Quick Start Guide** | [flyeelab.com/videos/setup-guide-2026](https://flyeelab.com/videos/setup-guide-2026) |
| 💬 **Comunidade** | [flyeelab.com/#community](https://flyeelab.com/#community) |

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
├── skills/           # 40+ skills modulares
├── workflows/        # 40+ workflows automatizados
├── scripts/          # Scripts de automação
├── templates/        # Templates (PRD, SDD, ADR, README, etc.)
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
| `tdd-reviewer` | Validação de SDDs |

[Ver todos os agentes →](agents/)

---

## 🔧 Workflows Principais

### 🆕 Novo Projeto

| Comando | Descrição |
|---------|-----------|
| `/new-project [nome]` | **Fluxo completo:** PRD → SDD → Security → Testes → Código → Deploy |
| `/new-project --brainstorm [nome]` | Inclui fase de **exploração de ideias** antes do PRD |
| `/new-project --quick [nome]` | Modo **ágil** (sem PRD, direto para SDD) |
| `/new-project --resume` | **Retomar** de onde parou (`PROJECT-PROGRESS.md`) |
| `/discovery` | **Discovery ágil:** SDD + Tasks no Flyee (sem PRD formal) |

### 📦 Projeto Legado

| Comando | Descrição |
|---------|-----------|
| `/legacy-project [path]` | **Fluxo completo:** Foundation → Análise → Docs → SDD Reverso → Security → Melhorias |
| `/legacy-project --scope [módulo]` | Analisar apenas **um módulo** (monorepos) |
| `/legacy-project --resume` | **Retomar** de onde parou (`LEGACY-PROGRESS.md`) |
| `/legacy-project --critical-first` | Priorizar fluxos **críticos** (auth, payment) |
| `/document [fluxo]` | Documentar UM fluxo específico (registra em `docs/INDEX.md`) |

### 📝 Documentação e Planejamento

| Comando | Descrição |
|---------|-----------|
| `/prd` | **PRD:** Product Requirements Document (O QUE construir) |
| `/tdd` | **SDD:** Software Design Document (COMO construir) — salvo como `SDD-*.md` |
| `/plan` | Planejamento estruturado de features |
| `/brainstorm` | Explorar opções técnicas sem compromisso |

### ✨ Nova Feature (Projeto Existente)

| Comando | Descrição |
|---------|-----------|
| `/new-task [descrição]` | **Melhoria rápida** com tracking no Flyee |
| `/new-task --tdd [descrição]` | Modo **TDD obrigatório** (testes antes do código — metodologia) |
| `/new-task --backlog [descrição]` | **Apenas registro**: Cria a task no Flyee e encerra |
| `/new-task --resume` | **Retomar** de onde parou |
| `/tdd new [feature]` | Criar SDD para nova feature |

### 📈 Flyee Integration

| Comando | Descrição |
|---------|-----------|
| `/demand` | **Comercial:** Levantamento de demanda e proposta |
| `/execute` | Executar task existente do Flyee |
| `/log` | Registrar trabalho já feito no Flyee |
| `/task-update` | Atualizar % e status de task |
| `/task-complete` | **Finalizar task** com QA gate obrigatório |

### 🛠️ Desenvolvimento

| Comando | Descrição |
|---------|-----------|
| `/create` | Criar nova aplicação (com testes obrigatórios) |
| `/test` | Gerar e rodar testes (TDD Metodologia: RED-GREEN-REFACTOR) |
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
| ✨ Nova feature em projeto existente | `/new-task` ou `/tdd new` |
| 💰 Proposta comercial | `/demand` |

### Criação de Tasks no Flyee

| Tipo de Demanda | Comando | Rastreamento (Flyee) |
|-----------------|---------|-----------------------|
| 💰 **Comercial** | `/demand` | Database "Propostas Comerciais" |
| 🏗️ **Projeto Novo** | `/new-project` → `/tdd breakdown` | Database "Tasks" |
| ⚡ **Melhoria Rápida** | `/new-task` | Database "Tasks" (direto) |

### Execução de Tasks

| Cenário | Comando | O que faz |
|---------|---------|-----------|
| 📋 **Task existe no Flyee** | `/execute 1.1` | Busca, executa e atualiza task existente |
| 🔄 **Atualizar progresso** | `/task-update 1.1 progress "msg"` | Atualiza % progresso no Flyee |
| ✅ **Finalizar task** | `/task-complete 1.1 "30min"` | QA gate + sync Flyee + INDEX.md |

---

## 🧠 Skills Populares

| Skill | Uso |
|-------|-----|
| `tdd-workflow` | **TDD Metodologia:** RED-GREEN-REFACTOR |
| `brainstorming` | Perguntas Socráticas obrigatórias |
| `testing-patterns` | Pirâmide de testes, mocking |
| `frontend-design` | Design de interfaces e Design Tokens |
| `mobile-design` | Design mobile-first e Figma Import |
| `clean-code` | Padrões de código limpo |
| `database-design` | Modelagem de dados |
| `api-patterns` | REST, GraphQL, tRPC |
| `tdd-validation` | Validação de SDDs |
| `project-foundation` | Gera README, .env, SECURITY, INDEX, ADR-000 |
| `document-registry` | Mantém `docs/INDEX.md` atualizado (READ/WRITE/UPDATE) |
| `context-gathering-patterns` | Leitura de docs antes de implementar (gate obrigatório) |
| `history-check-patterns` | Consulta histórico de bugs/features anteriores |

[Ver todas as skills →](skills/)

---

## ⚙️ Configuração

### 1. Flyee Integration (Obrigatório)

Para usar workflows de tracking (`/discovery`, `/new-task`, `/execute`, `/task-complete`):

1. Configure o MCP server `notion-mcp-server` (backend do Flyee)
2. Configure o `bridge.py` com sua API key (`flyee.json`)
3. Crie os databases conforme documentação

#### 📊 Padrões de Status (OBRIGATÓRIO)

> [!IMPORTANT]
> Todos os workflows usam esta nomenclatura padronizada:

| Status | Quando usar | % Progresso |
|--------|-------------|-------------|
| `backlog` | Task registrada, aguardando início | 0% |
| `running` | Task em execução | 1-99% |
| `testing` | Implementação concluída, aguardando QA | 99% |
| `completed` | Task finalizada + QA aprovado | 100% |

#### 👁️ View "Visão Cliente" (RECOMENDADO)

Para **transparência com o cliente**, crie uma view filtrada no Flyee:

**Configuração:**
```
Nome: "📊 Visão Cliente"
Tipo: Table
Filtro: Status ≠ "backlog" (opcional)
Propriedades visíveis:
  ✅ Nome (Title)
  ✅ Status
  ✅ % Progresso
  ✅ Previsão (se existir)
  ❌ Agente (ocultar)
  ❌ SDD Ref (ocultar)
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
