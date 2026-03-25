---
description: Workflow completo de descoberta a produção. Brainstorm → TDD → Design System → Validação → Tarefas no Flyee. Fluxo automatizado e contínuo. Suporta busca dinâmica de database.
skills: project-tracking-patterns, ui-ux-discovery, content-strategy
---

# /discovery - Da Ideia à Execução (Automático)

$ARGUMENTS

**Arguments:**

| Flag | Descrição | Exemplo |
|------|-----------|---------|
| `--from-demand` | Importa dados de proposta aprovada no Flyee | `--from-demand "Nome da Proposta"` |
| `--from-project` | Analisa projeto existente para gerar TDD | `--from-project "c:\path\to\project"` |
| `--from-figma` | Importa Design System do Figma existente | `--from-figma "https://figma.com/file/..."` |
| `--no-design` | Pula geração de Design System | `--no-design` |
| `--no-tracker` | Pula criação de tasks no Tracker | `--no-tracker` |
| `--no-infra` | Pula definição de infraestrutura | `--no-infra` |
| `--flyee-project` | Especifica database do Tracker | `--flyee-project "Tasks Database"` |

---

## 🎯 PROPÓSITO

Workflow **unificado e automatizado** que transforma uma ideia em tarefas executáveis no Flyee.
Totalmente dinâmico e adaptável ao contexto do projeto.

---

## 🔀 QUANDO USAR `/discovery` vs `/new-project`?

> [!TIP]
> **Escolha o workflow certo:**

| Situação | Use | Por quê? |
|----------|-----|----------|
| Ideia clara, preciso de **documentação formal** (PRD + TDD) | `/new-project` | Fluxo completo com aprovações |
| Ideia clara, quero ir **rápido** sem PRD | `/discovery` ou `/new-project --quick` | Direto para TDD + Flyee |
| Tenho **proposta comercial** aprovada | `/discovery --from-demand` | Importa contexto da proposta |
| Tenho **código legado** para documentar | `/discovery --from-project` | Engenharia reversa |
| Tenho **Figma** pronto | `/discovery --from-figma` | Importa Design System |

> [!NOTE]
> `/discovery` é equivalente a `/new-project --quick` com integração nativa ao Flyee.
> Se você precisa apenas de TDD + Tasks rapidamente, use `/discovery`.

---

## 🔴 FLUXO AUTOMATIZADO

### Fase 0: INTEGRAÇÃO COM /demand (Se --from-demand)
... (Fases 0 a 4.6 permanecem inalteradas, focando na integração Flyee) ...

---

### Fase 0.1: REVERSE ENGINEERING (Se --from-project)

> [!TIP]
> **Para fluxo completo de projeto legado**, use `/legacy-project [path]`.
> Esta fase é executada automaticamente como parte daquele workflow.

**Trigger:** `/discovery --from-project "path/to/project"`

**Agentes Envolvidos:**
- `explorer-agent` - Análise de estrutura e mapeamento
- `backend-specialist` / `frontend-specialist` / `mobile-developer` - Análise técnica conforme stack

**Ações:**

1. **Detectar Stack Tecnológica:**
   | Arquivo | Stack |
   |---------|-------|
   | `package.json` | Node.js/React/Next.js |
   | `requirements.txt` / `pyproject.toml` | Python |
   | `pubspec.yaml` | Flutter |
   | `Gemfile` | Ruby |
   | `go.mod` | Go |
   | `Cargo.toml` | Rust |

2. **Mapear Estrutura de Diretórios:**
   ```
   projeto/
   ├── src/           → Código fonte
   ├── tests/         → Testes existentes
   ├── docs/          → Documentação existente
   ├── config/        → Configurações
   └── ...
   ```

3. **Identificar Entry Points:**
   - Main files (index.js, main.py, App.tsx)
   - Rotas/Controllers
   - Componentes principais

4. **Listar Dependências:**
   - Frameworks utilizados
   - Bibliotecas principais
   - Serviços externos (APIs, DBs)

5. **Gerar Outline do Projeto:**
   ```markdown
   # CODEBASE-{projeto}.md
   
   ## Stack
   - Frontend: {framework}
   - Backend: {framework}
   - Database: {tipo}
   
   ## Estrutura
   {tree simplificado}
   
   ## Componentes Principais
   - {componente 1}: {descrição}
   - {componente 2}: {descrição}
   
   ## Fluxos Identificados
   - [ ] {fluxo 1}
   - [ ] {fluxo 2}
   ```

**Output:**
- `docs/CODEBASE-{projeto}.md` - Visão geral do projeto
- Lista de fluxos para documentar com `/document`

**Gate de Saída:**
```
[ ] Stack identificada
[ ] Estrutura mapeada
[ ] Fluxos principais listados
```

**Próximo Passo:** Para cada fluxo identificado → `/document [fluxo]`

---

### Fase 4: DESIGN SYSTEM (Exceto --no-design)

> [!NOTE]
> **Pulado se:** Flag `--no-design` ou projeto é API/Backend puro.

> [!IMPORTANT]
> **SKILL OBRIGATÓRIA:** Seguir `ui-ux-discovery` para perguntas granulares.
> **WORKFLOW:** Executar `/ui-ux-pro-max` para obter recomendações profissionais.

**Objetivo:** Definir UI/UX e Design System com base em decisões do usuário.

**Trigger:**
```
TDD aprovado (ou Fase 3 concluída)
```

**Agentes Envolvidos:**
- `frontend-specialist` - Para projetos web
- `mobile-developer` - Para projetos mobile

---

#### Processo Completo (Skill: ui-ux-discovery)

> [!CAUTION]
> **OBRIGATÓRIO:** Seguir TODOS os 5 passos definidos na skill `ui-ux-discovery`.
> **NÃO** gerar Design System final sem respostas do usuário.

| Passo | Ação | Detalhes |
|-------|------|----------|
| 1 | Executar `/ui-ux-pro-max` | Obter recomendações modernas |
| 2 | **Perguntas Granulares ⭐** | Por aspecto: cores, tipografia, layout, efeitos, logo |
| 3 | Aguardar Respostas | **BLOQUEADOR** - Não prosseguir sem resposta |
| 4 | Consolidar Decisões | Combinar escolhas do usuário + recomendações |
| 5 | Validar e Aprovar | Aguardar aprovação humana |

**Gate de Saída:**
```
[ ] /ui-ux-pro-max executado
[ ] Perguntas granulares respondidas pelo usuário
[ ] Design System persistido
[ ] Design System aprovado pelo humano
```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir para Flyee sem Design System aprovado (exceto --no-design).

---

### Fase 4.5: CONTENT STRATEGY (Exceto --no-content)

> [!NOTE]
> **Pulado se:** Flag `--no-content` ou projeto é API/Backend puro.

> [!IMPORTANT]
> **SKILL:** Seguir `content-strategy` para definição de copy e conteúdo.
> **Documento:** `docs/content/CONTENT-STRATEGY-{nome}.md`

| Passo | Ação | Detalhes |
|-------|------|----------|
| 1 | Identificar Páginas | Listar todas as páginas que precisam de conteúdo |
| 2 | **Perguntas ao Usuário ⭐** | Tom de voz, público, USP, pricing |
| 3 | Gerar Documento | Hero, Features, FAQ, SEO metadata |
| 4 | Validar e Aprovar | Aguardar aprovação humana |

**Gate de Saída:**
```
[ ] CONTENT-STRATEGY-{nome}.md gerado
[ ] Copy da LP definido
[ ] Conteúdo aprovado pelo humano
```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir para Flyee sem Content Strategy aprovado (exceto --no-content).

---

### Fase 5: TASK INTEGRATION (Automático após aprovação)

> [!CAUTION]
> **GATE PRÉ-INTEGRAÇÃO: ESCOLHA DE TRACKING**
> 
> Antes de criar tarefas, verifique a configuração `Tracker de Tasks`.
> Se não estiver definida, pergunte ao usuário:
> *“Como deseja registrar as tarefas?”* (1. Flyee vs 2. Local `docs/TASKS.md`)
> 
> **Se Tracker = Local:** Pule a repetição Flyee e grave as tasks diretamente em `docs/TASKS.md`.
> **Se Tracker = Flyee:** Prossiga com a Criação via Bridge abaixo.

#### Fase 5.1: TASK CREATION (Execution)

**Trigger:** Usuário aprova User Stories

**Ações (Para CADA User Story):**
1. Ler documento `USER-STORIES-{nome}.md`
2. **Executar Bridge CLI:**

```bash
python3 .agent/flyee-bridge/bridge.py --create-task \
  --name "{Título da Task}" \
  --type implement_feature \
  --description "User Story: As a {user}, I want {action}, so that {benefit}. ACs: 1. Criteria 1" \
  --priority high
```

> [!CAUTION]
> A estimativa de complexidade ou horas deve constar na description se necessário, ou usar as flags adequadas do script.

#### 🔔 FLYEE BRIDGE EMIT (Condicional)

> Se `flyee.json` existe E `enabled: true`:

```bash
python .agent/flyee-bridge/bridge.py emit "dev.workflow_completed" '{"workflow": "discovery", "project": "{nome}"}'
```

> Se bridge não configurado → Pular silenciosamente.
