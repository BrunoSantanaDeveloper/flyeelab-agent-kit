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
> **Se Tracker = Flyee:** Prossiga com as Fases 5.1 e 5.2 abaixo.

#### Fase 5.1: DISCOVERY & VALIDATION (Pre-flight Flyee) 🔴 OBRIGATÓRIO (Se Tracker = Flyee)

**Trigger:** Usuário aprova User Stories

**Agente Responsável:** `orchestrator` (Validador de integração)
**Skills:** `api-patterns`, `brainstorming` (feedback de erro)

**Ações:**

1. **Discover Database:**
   *   Se flag `--flyee-project` informada: Buscar por name exato.
   *   Se não: Buscar por "Tarefas", "Tasks", "Daily", "Sprint".
   ```
   API-post-search:
   - query: "{query}"
   - filter: { "value": "database" }
   ```

2.  **Validate Schema & Map:**
    *   Ao encontrar, validar schema e mapear propriedades **dinamicamente**:
    *   `Status` (Status) -> Guardar options (ex: To Do / Doing / Done)
    *   `Prioridade` (Select) -> Guardar options real (ex: P0/P1 ou Alta/Baixa)
    *   `Estimativa` (Select) -> Guardar options real (ex: XS/S/M ou 1/2/3)
    
3.  **Check "Tempo Gasto":**
    *   Verificar se propriedade existe.
    *   Se não: Perguntar se deseja criar (opcional).

4. **Decisão Automática:**
   - **❌ Falha:** Se não encontrar database ou schema incompatível (sem Status/Title) -> **NOTIFICAR USUÁRIO**.
   - **✅ Sucesso:** Guardar `{DATABASE_ID}` e `{SCHEMA_MAP}` para Fase 5.2.

**Mensagem de Sucesso (Obrigatória no plano):**
```
✅ FLYEE DISCOVERY PASSED

Database: {nome_encontrado}
ID: {DATABASE_ID}

Mapeamento:
- Status: Usando "Backlog"
- Prioridade: Usando "High", "Medium", "Low"
```

---

#### Fase 5.2: TASK CREATION (Execution)

**Trigger:** Discovery = PASS

**Ações (Para CADA User Story):**
1. Ler documento `USER-STORIES-{nome}.md`
2. **Passo 1 - Criar página dinamicamente:**
   ```
   API-post-page:
   - parent: { database_id: "{DATABASE_ID_ENCONTRADO}" }
   - properties: {
       "Título": { title: [{ text: { content: "{Título da Task}" } }] },
       "ID": { rich_text: [{ text: { content: "{N.X}" } }] },
       "Épico": { select: { name: "{Nome do Épico}" } },
       "Status": { status: { name: "{STATUS_MAPPED}" } },
       "Prioridade": { select: { name: "{PRIORITY_MAPPED}" } },
       "Estimativa": { number: {horas_estimadas} },  // ✅ OBRIGATÓRIO
       // ... outras props mapeadas
     }
   ```
   
   > [!CAUTION]
   > **OBRIGATÓRIO:** `Estimativa` deve ser preenchido ao criar task.
   
   > **Geração de ID:** Formato `{Épico}.{Sequência}`, ex: `1.1`, `1.2`, `2.1`
3. **Passo 2 - Adicionar corpo (OBRIGATÓRIO):**
   ```
   ```
   API-patch-block-children:
   - block_id: { id retornado do passo 1 }
   - children: [
       {
         "heading_2": { "rich_text": [{ "text": { "content": "📖 User Story" } }] }
       },
       {
         "paragraph": { "rich_text": [{ "text": { "content": "As a {user}, I want {action}, so that {benefit}." } }] }
       },
       {
         "heading_2": { "rich_text": [{ "text": { "content": "✅ Acceptance Criteria" } }] }
       },
       {
         "to_do": { "rich_text": [{ "text": { "content": "Criteria 1" } }], "checked": false }
       }
     ]
   ```
   ```

#### 🔔 FLYEE BRIDGE EMIT (Condicional)

> Se `flyee.json` existe E `enabled: true`:

```bash
python .agent/flyee-bridge/bridge.py emit "dev.workflow_completed" '{"workflow": "discovery", "tasks_created": {N}, "project": "{nome}"}'
```

> Se bridge não configurado → Pular silenciosamente.

---

## 🔧 EXAMPLE REQUESTS

**Exemplo Dinâmico (Busca e Criação):**
```json
// Busca
POST API-post-search { "query": "Tarefas", "filter": { "value": "database" } }
// Retorna ID: "b7e8..."

// Criação
POST API-post-page
{
  "parent": { "database_id": "b7e8..." },
  "properties": { 
     // Propriedades adaptadas ao schema retornado
  }
}
```

> [!TIP]
> **Nunca assuma IDs.** Se o `/enhance` ou `/log` já rodaram e encontraram um ID, você pode (e deve) reutilizá-lo para consistência.
