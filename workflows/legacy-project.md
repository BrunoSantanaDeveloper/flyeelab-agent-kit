---
description: Workflow unificado para projeto legado. Análise → Documentação → TDD Reverso → Design System → Melhorias. Engenharia reversa e modernização. Suporta projetos grandes com checkpointing.
skills: notion-task-patterns, checkpointing-patterns, history-check-patterns, project-tracking-patterns, ui-ux-discovery, local-verification, content-strategy, design-system-enforcement

---

# /legacy-project - Projeto Legado Completo

$ARGUMENTS

**Arguments:**

| Flag | Descrição | Exemplo |
|------|-----------|---------|
| `--scope [path]` | Analisar apenas um módulo/domínio | `--scope src/auth` |
| `--resume` | Retomar de onde parou | `--resume` |
| `--critical-first` | Priorizar fluxos críticos (auth, payment) | `--critical-first` |
| `--analyze-only` | Apenas análise, sem TDD | `--analyze-only` |
| `--quick` | Análise rápida + TDD direto | `--quick` |
| `--notion` | Sincronizar progresso com Notion | `--notion` |
| `--force` | Forçar re-análise (ignora cache) | `--force` |

---

## 🎯 PROPÓSITO

Workflow **orquestrador** para trabalhar com projetos existentes/legados, garantindo:
- Análise **incremental** por escopo/módulo
- Documentação estruturada dos fluxos
- TDD reverso (do código para documentação técnica)
- **Checkpointing** para retomar de onde parou
- Plano de melhorias e refactoring priorizado

---

## 📊 QUANDO USAR?

| Situação | Workflow |
|----------|----------|
| Projeto existente sem documentação | `/legacy-project` |
| Monorepo grande | `/legacy-project --scope [módulo]` |
| Retomar trabalho interrompido | `/legacy-project --resume` |
| Documentar UM fluxo específico | `/document [fluxo]` |
| Projeto novo do zero | `/new-project` |

---

## 🧩 SUBCOMMANDS

| Comando | Ação |
|---------|------|
| `/legacy-project [path]` | Fluxo **completo** com seleção de escopo |
| `/legacy-project --scope [módulo] [path]` | Analisar **apenas** o módulo especificado |
| `/legacy-project --resume` | **Retomar** de onde parou |
| `/legacy-project --critical-first [path]` | Priorizar **fluxos críticos** |
| `/legacy-project --quick [path]` | Análise rápida + TDD direto |
| `/legacy-project status` | Mostrar **status** e progresso |

---

## 💾 SISTEMA DE CHECKPOINTING

> [!IMPORTANT]
> **Projetos grandes precisam de persistência.**
> O workflow salva progresso em `docs/LEGACY-PROGRESS.md` a cada fase.

### Arquivo de Controle: `docs/LEGACY-PROGRESS.md`

Este arquivo é **criado automaticamente** e contém:

| Seção | Conteúdo |
|-------|----------|
| Status Geral | Projeto, path, fase atual, última atualização |
| Mapeamento de Escopos | Lista de todos os módulos e seu status |
| Escopo Atual | Checklist detalhado da fase em andamento |
| Histórico | Log de ações realizadas |

### Retomada Automática

```bash
# Retomar de onde parou
/legacy-project --resume

# Ver status detalhado
/legacy-project status
```

Ao executar `--resume`:
1. Carrega `docs/LEGACY-PROGRESS.md`
2. Identifica fase pendente
3. Continua execução

---

## 🔴 FLUXO COMPLETO

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   OVERVIEW   │───▶│   ESCOPO     │───▶│   ANÁLISE    │───▶│ NOTION SETUP │───▶│ DOCUMENTAÇÃO │───▶│  TDD REVERSO │───▶│   TESTES     │───▶│  BREAKDOWN   │───▶│  EXECUÇÃO    │───▶│ PUBLICAÇÃO   │
│  (Mapear)    │    │  (Escolher)  │    │  (Detalhar)  │    │ + BREAKDOWN  │    │  (Fluxos)    │    │  (Técnico)   │    │  (Cobrir)    │    │ 7A (Planejar)│    │ 7B (Executar)│    │  (Notion)    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       ✅                  ✋                  ✅                  ✅                 ✅ 🔄                ✋ 🔄               ✅ 🔄                ✋ Gate              ✅ 🔄                📚
   Automático          Seleção           Automático         + Tasks Notion     Automático+Sync      Aprovação+Sync     Incremental+Sync     Aprovação         Implement+Sync     Docs→Cliente
```

> 🔄 = NOTION SYNC obrigatório ao final da fase (ver skill `notion-task-patterns` → "PHASE TASK TRACKING")
> 📚 = Publicação de documentação nas databases "Documentação Técnica" e "Manual do Usuário"

---

### Phase 0: CHECKPOINTING - Verificar Estado

**Objetivo:** Verificar se existe trabalho anterior e decidir ação.

**Trigger:**
```
/legacy-project [path]
```

**Ações:**
1. Verificar se existe `docs/LEGACY-PROGRESS.md`
2. Se existe:
   ```
   ⚠️ Encontrado progresso anterior:
   - Projeto: {nome}
   - Fase atual: 3/5 - TDD Reverso
   - Escopo: src/payment
   
   Deseja:
   1. Retomar de onde parou
   2. Reiniciar análise completa
   3. Analisar novo escopo
   ```
3. Se não existe: Criar arquivo e prosseguir

#### Passo 0.5: Auto-Anchor de Tasks Órfãs (OBRIGATÓRIO no --resume)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Ao retomar (`--resume`), ANTES de continuar qualquer fase,
> executar verificação de tasks órfãs no Notion. Tasks criadas em conversas paralelas
> podem existir sem estarem rastreadas no `LEGACY-PROGRESS.md`.

**0.5.1 - Consultar todas as tasks existentes no database "Tarefas":**

Usar `post-search` paginado para obter todas as pages do database.

**0.5.2 - Comparar com seção "📋 Registro de Tasks Notion" do `LEGACY-PROGRESS.md`:**

Extrair IDs de todas as linhas da tabela. Identificar IDs presentes no Notion mas
**ausentes** no registro local.

**0.5.3 - Para cada task órfã detectada, auto-classificar e ancorar:**

| Categoria / Épico da task | Fase destino | Onde ancorar no checklist |
|---------------------------|-------------|--------------------------|
| Documentação | Phase 4 ou 8 | Checklist da fase correspondente |
| Refatoração / Melhoria | Phase 7B | Adicionar como item `[ ]` no checklist |
| Testes | Phase 6 | Checklist de testes |
| Outra | Phase 8 | Fallback: Próximo Escopo |

**0.5.4 - Verificar duplicatas:**

Se a task órfã tem escopo **idêntico** a uma task já rastreada:
1. Fechar a task duplicada no Notion (Status: "Concluído", comentário explicando)
2. Marcar no registro como `❌ Duplicata (#XX)`

**0.5.5 - Atualizar `LEGACY-PROGRESS.md`:**

1. Adicionar tasks órfãs ao "📋 Registro de Tasks Notion" com a fase correta
2. Adicionar como `[ ]` no checklist da fase destino
3. Reportar ao usuário:

```
🔍 **AUTO-ANCHOR: {N} task(s) órfã(s) detectada(s)**

| # | Task | Ação |
|---|------|------|
| {id} | {título} | Ancorada na Phase {X} |
| {id} | {título} | ❌ Fechada como duplicata de #{XX} |

Registro e checklists atualizados automaticamente.
```

> [!TIP]
> Se NENHUMA task órfã for encontrada, prosseguir silenciosamente.

**Checkpoint salvo:** Estado inicial registrado + tasks órfãs resolvidas

#### Passo 0.6: Context Re-Check (OBRIGATÓRIO se retomando Phase 7B)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Se a fase atual é 7B, o agente DEVE verificar se o
> Context Gathering foi completado para a task em andamento ANTES de retomar
> a implementação. Truncamento de conversa ou checkpoint pode ter apagado
> o contexto lido anteriormente.

**0.6.1 - Identificar task em andamento:**

Ler `LEGACY-PROGRESS.md` → encontrar task com status `[/]` (em progresso) na Phase 7B.

**0.6.2 - Verificar checklist de Context Gathering:**

Buscar no `LEGACY-PROGRESS.md` a seção `📖 CONTEXT GATHERING — Task #{id}`.

- **Se existe e está preenchida** → prosseguir com a implementação
- **Se NÃO existe ou está incompleta** → executar Context Gathering (Phase 7B, Passo 0) obrigatoriamente antes de continuar

> [!TIP]
> Isso garante que mesmo após truncamento de conversa, o agente releia
> a documentação antes de tomar decisões de implementação.

**Checkpoint salvo:** Context verificado para task em andamento

---

### Phase 1: OVERVIEW - Mapeamento de Alto Nível

**Objetivo:** Entender a estrutura geral do projeto SEM analisar tudo.

**Trigger:**
```
Phase 0 concluída ou /legacy-project --force
```

**Agentes Envolvidos:**
- `explorer-agent` - Análise de estrutura

**Ações:**
1. **Detectar tipo de projeto:**
   | Estrutura | Tipo |
   |-----------|------|
   | `packages/` ou `apps/` | Monorepo |
   | `src/modules/` | Modular |
   | Flat structure | Monolítico |

2. **Mapear módulos/domínios de alto nível:**
   ```
   projeto/
   ├── src/
   │   ├── auth/          ← Módulo 1
   │   ├── payment/       ← Módulo 2
   │   ├── users/         ← Módulo 3
   │   └── products/      ← Módulo 4
   ```

3. **Identificar fluxos críticos** (baseado em keywords):
   | Keyword | Criticidade |
   |---------|-------------|
   | `auth`, `login`, `session` | 🔴 Alta |
   | `payment`, `checkout`, `billing` | 🔴 Alta |
   | `user`, `profile`, `account` | 🟡 Média |
   | Outros | 🟢 Normal |

4. **Gerar `docs/CODEBASE-{projeto}.md`** (visão geral)

**Output:**
```markdown
# CODEBASE-{projeto}.md

## Tipo de Projeto
Monorepo com 4 módulos

## Módulos Identificados

| Módulo | Criticidade | Arquivos | Status |
|--------|-------------|----------|--------|
| `src/auth` | 🔴 Alta | 23 | ⏳ Pendente |
| `src/payment` | 🔴 Alta | 45 | ⏳ Pendente |
| `src/users` | 🟡 Média | 18 | ⏳ Pendente |
| `src/products` | 🟢 Normal | 67 | ⏳ Pendente |

## Ordem Recomendada de Análise
1. `src/auth` (crítico, menor)
2. `src/payment` (crítico)
3. `src/users` (médio)
4. `src/products` (maior, pode dividir)
```

**Checkpoint salvo:** Lista de escopos identificados

---

### Phase 2: SELEÇÃO DE ESCOPO

**Objetivo:** Escolher qual módulo analisar primeiro.

**Trigger:**
```
Phase 1 concluída
```

**Ações:**
1. Apresentar módulos identificados com recomendação
2. **AGUARDAR** seleção do usuário (ou usar `--scope` / `--critical-first`)
3. Registrar escopo selecionado no arquivo de progresso

**Opções:**
```
📦 Módulos disponíveis para análise:

1. [RECOMENDADO] src/auth (🔴 crítico, 23 arquivos)
2. src/payment (🔴 crítico, 45 arquivos)
3. src/users (🟡 médio, 18 arquivos)
4. src/products (🟢 normal, 67 arquivos)

Qual módulo deseja analisar primeiro?
(Digite número ou path)
```

**Se `--critical-first`:** Seleciona automaticamente o primeiro crítico
**Se `--scope [path]`:** Usa o path especificado

**Checkpoint salvo:** Escopo selecionado

---

### Phase 3: ANÁLISE DETALHADA DO ESCOPO

**Objetivo:** Analisar profundamente o módulo selecionado.

**Trigger:**
```
Escopo selecionado
```

**Agentes Envolvidos:**
- `explorer-agent` - Mapeamento
- Especialista conforme stack (backend/frontend/mobile)

**Ações:**
1. Executar `/discovery --from-project [escopo]`
2. Detectar stack do módulo
3. Mapear estrutura interna
4. Identificar entry points e fluxos
5. Listar dependências internas e externas

**Output:**
- Atualização de `docs/CODEBASE-{projeto}.md` seção do módulo
- Lista de fluxos para documentar

**Checkpoint salvo:** Análise do módulo concluída

---

### Phase 3.5: NOTION SETUP + BREAKDOWN DE FASES

> [!CAUTION]
> **REGRA BLOQUEANTE:** Esta fase DEVE ser executada ANTES de iniciar qualquer trabalho
> nas fases 4-7. Toda atividade pós-análise precisa de tasks no Notion para
> **transparência com o cliente**.

**Objetivo:** Configurar Notion e criar tasks antecipadas para todas as fases seguintes.

**Trigger:**
```
Phase 3 concluída → Automático
```

**Agentes Envolvidos:**
- `orchestrator` - Integração Notion

> [!IMPORTANT]
> **SKILL:** Seguir `notion-task-patterns` → seção "PHASE TASK TRACKING" OBRIGATORIAMENTE.

#### Passo 1: Discovery e Validação do Database

> Seguir skill `notion-task-patterns` → seção "VALIDAÇÃO DE SCHEMA"

```json
// Tool: mcp_notion-mcp-server_API-post-search
{
  "query": "Tarefas",
  "filter": { "property": "object", "value": "data_source" }
}
```

```json
// Tool: mcp_notion-mcp-server_API-retrieve-a-database
{ "database_id": "{DATABASE_ID}" }
```

> Se propriedades ausentes → PARAR e notificar usuário (ver skill para mensagem).

#### Passo 2: Perguntar Idioma (se não definido)

> Seguir skill `notion-task-patterns` → seção "IDIOMA DAS TASKS"

Salvar preferência em `docs/LEGACY-PROGRESS.md` → seção "Configurações".

#### Passo 2.5: ID Continuity Check (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de criar QUALQUER task nova, o agente DEVE verificar
> quais tasks já existem no Notion para evitar gaps de numeração no rastreamento.

**2.5.1 - Consultar todas as tasks existentes:**
```
Use: mcp_notion-mcp-server_API-post-search
query: ""
filter: { "property": "object", "value": "page" }
page_size: 100
```

> Se `has_more: true`, paginar com `start_cursor` até obter todas.

**2.5.2 - Construir mapa de IDs:**

Para cada resultado, extrair:
- `properties.ID.unique_id.number` → Notion ID
- `properties.Nome da tarefa.title[0].plain_text` → Título
- `properties.Status.status.name` → Status

**2.5.3 - Comparar com LEGACY-PROGRESS.md:**

1. Ler seção "📋 Registro de Tasks Notion" do `LEGACY-PROGRESS.md`
2. Identificar IDs presentes no Notion mas **ausentes** no arquivo local
3. Se houver IDs não rastreados:

```
⚠️ **TASKS NÃO RASTREADAS DETECTADAS**

As seguintes tasks existem no Notion mas NÃO estão em LEGACY-PROGRESS.md:

| # | Task | Status | Criado em |
|---|------|--------|----------|
| {id} | {título} | {status} | {data} |

→ Registrando automaticamente antes de criar novas tasks...
```

4. Adicionar tasks não rastreadas ao "📋 Registro de Tasks Notion" no `LEGACY-PROGRESS.md`
5. Só então prosseguir para criação de novas tasks

> [!IMPORTANT]
> **Último ID registrado:** O agente DEVE anotar o maior ID existente (`max_id`).
> As novas tasks criadas terão IDs a partir de `max_id + 1`.
> Usar este valor ao documentar as tasks no LEGACY-PROGRESS.md.

#### Passo 3: Criar Tasks para Fases 4-7

Baseado nos fluxos identificados na Phase 3, criar tasks antecipadas:

> Seguir skill `notion-task-patterns` → seção "PHASE TASK TRACKING" → "Processo: Breakdown de Fases"

**Para cada task: ETAPA 1 (criar página) → ETAPA 2 (adicionar corpo) → próxima task.**

Tasks a criar (exemplo para módulo `{módulo}`):

| # | Task | Categoria | Épico | Template |
|---|------|-----------|-------|----------|
| 1 | Documentar fluxo: {fluxo 1} | Documentação | {módulo} - Documentação | Documentação |
| 2 | Documentar fluxo: {fluxo 2} | Documentação | {módulo} - Documentação | Documentação |
| ... | (1 task por fluxo identificado) | ... | ... | ... |
| N | TDD Reverso: {módulo} | Documentação | {módulo} - TDD | Documentação |
| N+1 | Design System: extração (se UI) | Melhoria | {módulo} - Design System | Documentação |
| N+2 | Testes: Integration (fluxos críticos) | Melhoria | {módulo} - Testes | Documentação |
| N+3 | Testes: Unit (funções complexas) | Melhoria | {módulo} - Testes | Documentação |
| N+4 | Testes: E2E (happy paths) | Melhoria | {módulo} - Testes | Documentação |

> [!WARNING]
> **Tasks de melhorias/refatoração (Phase 7A)** são criadas DEPOIS, quando o TDD Reverso
> identificar os débitos técnicos. Não antecipar estas tasks aqui.

#### Passo 4: Relatório de Tasks Criadas

```markdown
📋 **BREAKDOWN DE FASES - {módulo}**

| # | Task | Categoria | Épico | Estimativa |
|---|------|-----------|-------|------------|
| 1 | {nome} | {cat} | {épico} | {Xh} |
| ... | ... | ... | ... | ... |

Total: {N} tasks criadas
Estimativa total: {Xh}

✅ Cliente pode acompanhar em: Notion → Database "Tarefas"
```

**Gate de Saída:**
```
[ ] Database "Tarefas" encontrado e validado
[ ] ID Continuity Check executado (sem gaps)
[ ] Idioma definido e salvo em LEGACY-PROGRESS.md
[ ] Tasks criadas para Phases 4-6 (1 por fluxo + TDD + DS + testes)
[ ] TODAS as tasks com corpo preenchido (Template Documentação)
[ ] LEGACY-PROGRESS.md atualizado com lista de tasks + Registro de Tasks
```

**Checkpoint salvo:** Tasks criadas no Notion

---

### Phase 4: DOCUMENTAÇÃO DOS FLUXOS

**Objetivo:** Documentar cada fluxo do módulo selecionado.

**Trigger:**
```
Phase 3 concluída → Automático
```

**Agentes Envolvidos:**
- `documentation-writer` - Geração de docs
- Especialistas de domínio

**Ações:**
Para cada fluxo identificado:
1. Executar `/document [nome-do-fluxo]`
2. Gerar documentação estruturada
3. Salvar em `docs/flows/{módulo}/{fluxo}.md`
4. **Atualizar checkpoint** após cada fluxo

**Checkpoint salvo:** Após cada fluxo documentado

> [!TIP]
> Se o fluxo for interrompido, ao retomar ele continuará do próximo fluxo não documentado.

#### 🔄 NOTION SYNC - Phase 4 (OBRIGATÓRIO)

> [!CAUTION]
> **Ao concluir CADA fluxo documentado**, executar sync da task correspondente.
> Seguir skill `notion-task-patterns` → seção "PHASE TASK TRACKING" → "Gate: NOTION SYNC".

Para cada fluxo concluído:
1. Atualizar task → Status: "Concluído", `Tempo Gasto`, `% Progresso: 100`
2. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    { "type": "callout", "callout": { "icon": { "type": "emoji", "emoji": "✅" }, "rich_text": [{ "type": "text", "text": { "content": "Concluído em {data}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📋 {resumo da implementação}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📁 Arquivos: {lista de arquivos modificados}" } }] } }
  ]
}
```

3. Adicionar comentário rico de conclusão

**Ao concluir TODOS os fluxos:**
4. Verificar que TODAS as tasks de documentação estão synced (Gate de Conclusão)
5. Atualizar `LEGACY-PROGRESS.md`

---

### Phase 5: TDD REVERSO

**Objetivo:** Gerar TDD a partir do código analisado.

**Trigger:**
```
Phase 4 concluída
```

**Agentes Envolvidos:**
- `project-planner` - Estruturação
- `tdd-reviewer` - Validação

**Ações:**
1. Consolidar informações das documentações
2. Extrair arquitetura do módulo
3. Identificar débitos técnicos
4. Priorizar por impacto/esforço:

   | Prioridade | Critério |
   |------------|----------|
   | P0 | Segurança, bugs críticos |
   | P1 | Performance, fluxos principais |
   | P2 | Refactoring, qualidade |
   | P3 | Nice-to-have |

5. Gerar `docs/design/TDD-{projeto}-{módulo}.md`
6. **AGUARDAR** aprovação humana

#### 🔄 NOTION SYNC - Phase 5 (OBRIGATÓRIO)

> [!CAUTION]
> **Após TDD aprovado**, executar sync.
> Seguir skill `notion-task-patterns` → seção "PHASE TASK TRACKING" → "Gate: NOTION SYNC".

1. Atualizar task "TDD Reverso: {módulo}" → Status: "Concluído", `Tempo Gasto`, `% Progresso: 100`
2. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    { "type": "callout", "callout": { "icon": { "type": "emoji", "emoji": "✅" }, "rich_text": [{ "type": "text", "text": { "content": "Concluído em {data}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📋 {resumo da implementação}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📁 Arquivos: {lista de arquivos modificados}" } }] } }
  ]
}
```

3. Adicionar comentário rico de conclusão
4. Verificar Gate de Conclusão da fase

> [!IMPORTANT]
> **POST-TDD:** Os débitos técnicos P0/P1/P2/P3 identificados no TDD serão
> transformados em tasks na **Phase 7A (Breakdown)**. O agente DEVE referenciar
> a seção "Débitos Técnicos" do TDD ao criar o breakdown.
> **NÃO** criar tasks de melhorias aqui — isso é responsabilidade da Phase 7A.

**Checkpoint salvo:** TDD gerado e synced no Notion

---

### Phase 5.5: DESIGN SYSTEM (Se projeto tem UI)

> [!NOTE]
> **Pulado se:** Projeto é apenas API/Backend sem interface.

> [!IMPORTANT]
> **SKILL:** Seguir `ui-ux-discovery` para processo completo.
> **WORKFLOW:** Executar `/ui-ux-pro-max` para recomendações profissionais.

**Objetivo:** Definir Design System com base em decisões granulares do usuário.

**Trigger:**
```
TDD Reverso aprovado
```

**Agentes Envolvidos:**
- `frontend-specialist` - Para projetos web
- `mobile-developer` - Para projetos mobile

---

#### Processo Completo (Skill: ui-ux-discovery)

> [!CAUTION]
> **OBRIGATÓRIO:** Seguir TODOS os 5 passos definidos na skill `ui-ux-discovery`.

| Passo | Ação | Detalhes |
|-------|------|----------|
| 1 | Extrair Identidade Atual | Cores, fontes, elementos do legado |
| 2 | Executar `/ui-ux-pro-max` | Obter recomendações modernas |
| 3 | Perguntas Granulares ⭐ | Por aspecto: cores, tipografia, layout, efeitos, logo |
| 4 | Consolidar Decisões | Combinar mantidos + modernizados |
| 5 | Validar e Aprovar | Aguardar aprovação humana |

**Gate de Saída:**
```
[ ] Identidade visual atual extraída
[ ] /ui-ux-pro-max executado
[ ] Perguntas granulares respondidas pelo usuário
[ ] Design System consolidado com decisões híbridas
[ ] Pre-Delivery Checklist verificado
[ ] Design System aprovado pelo humano
```

#### 🔄 NOTION SYNC - Phase 5.5 (OBRIGATÓRIO)

> [!CAUTION]
> **Após Design System aprovado**, executar sync.
> Seguir skill `notion-task-patterns` → seção "PHASE TASK TRACKING" → "Gate: NOTION SYNC".

1. Atualizar task "Design System: extração" → Status: "Concluído", `Tempo Gasto`, `% Progresso: 100`
2. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    { "type": "callout", "callout": { "icon": { "type": "emoji", "emoji": "✅" }, "rich_text": [{ "type": "text", "text": { "content": "Concluído em {data}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📋 {resumo da implementação}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📁 Arquivos: {lista de arquivos modificados}" } }] } }
  ]
}
```

3. Adicionar comentário rico de conclusão
4. Verificar Gate de Conclusão da fase

**Checkpoint salvo:** Design System definido e synced no Notion

---

### 🛑 GATE: Phase 5.5 → Phase 6 (Se projeto tem UI)

> [!CAUTION]
> **BLOQUEADOR:** Se projeto tem UI, você NÃO PODE prosseguir sem completar Phase 5.5.

**Passo 1: Executar Validação Automatizada**

> **Skill:** `ui-validation`

```bash
python .agent/skills/ui-validation/scripts/ui_antipattern_check.py .
```

**Passo 2: Checklist (OBRIGATÓRIO)**
```markdown
⚠️ VERIFICAÇÃO ANTES DE TESTES

[ ] /ui-ux-pro-max executado?
[ ] Design System documentado?
[ ] Pre-Delivery Checklist verificado?
[ ] 🔴 ui-validation script PASSOU?
[ ] Design System aprovado?

❌ Se QUALQUER item desmarcado → Voltar para Phase 5.5
✅ TODOS marcados → Prosseguir para Phase 6
```

---

### Phase 6: TESTES INCREMENTAIS

**Objetivo:** Adicionar testes ao código legado de forma incremental.

**Trigger:**
```
TDD aprovado
```

**Estratégia:**

| Fase | Tipo | Foco | Cobertura Alvo |
|------|------|------|----------------|
| 1 | Integration | Fluxos críticos | 60% |
| 2 | Unit | Funções complexas | 70% |
| 3 | E2E | Happy paths | 80% |
| 4 | Edge cases | Bugs conhecidos | 85%+ |

**Ações:**
1. Identificar código sem cobertura
2. Priorizar por criticidade
3. Gerar testes usando `/test [componente]`
4. Verificar cobertura incremental
5. **Atualizar checkpoint** após cada lote de testes

#### 🔄 NOTION SYNC - Phase 6 (OBRIGATÓRIO)

> [!CAUTION]
> **Ao concluir CADA lote de testes** (Integration, Unit, E2E, Edge), executar sync.
> Seguir skill `notion-task-patterns` → seção "PHASE TASK TRACKING" → "Gate: NOTION SYNC".

Para cada lote concluído:
1. Atualizar task correspondente → Status: "Concluído", `Tempo Gasto`, `% Progresso: 100`
2. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    { "type": "callout", "callout": { "icon": { "type": "emoji", "emoji": "✅" }, "rich_text": [{ "type": "text", "text": { "content": "Concluído em {data}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📋 {resumo da implementação}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📁 Arquivos: {lista de arquivos modificados}" } }] } }
  ]
}
```

3. Adicionar comentário rico de conclusão

**Ao concluir TODOS os lotes:**
4. Verificar que TODAS as tasks de testes estão synced (Gate de Conclusão)
5. Atualizar `LEGACY-PROGRESS.md`

**Checkpoint salvo:** Cobertura atual registrada e synced no Notion

---

### Phase 7A: BREAKDOWN DE MELHORIAS (Planejamento)

**Objetivo:** Transformar débitos técnicos do TDD em tasks priorizadas no Notion.

**Trigger:**
```
Phase 6 concluída (ou parcialmente se cobertura aceitável)
```

**Agentes Envolvidos:**
- `project-planner` - Estruturação de tasks
- `orchestrator` - Integração Notion

> [!IMPORTANT]
> **Transparência para Cliente:** Todas as melhorias identificadas devem ser
> registradas no Notion para visibilidade do progresso.

#### Passo 1: Gerar Breakdown

1. Ler seção "Débitos Técnicos" do TDD (`docs/design/TDD-{projeto}-{módulo}.md`)
2. Executar `/tdd breakdown docs/design/TDD-{projeto}-{módulo}.md`
3. Criar tasks priorizadas:
   - P0: Segurança e bugs críticos
   - P1: Débitos técnicos de alto impacto
   - P2: Refactoring e qualidade
   - P3: Melhorias futuras

#### Passo 2: Discovery e Validação do Notion (OBRIGATÓRIO)

> [!CAUTION]
> **Seguir skill `notion-task-patterns` OBRIGATORIAMENTE.**
> NÃO pular validação de schema.

**2.1 - Buscar Database "Tarefas":**
```
Use: mcp_notion-mcp-server_API-post-search
query: "Tarefas"
filter: { "property": "object", "value": "data_source" }
```

> **ATENÇÃO:** Buscar EXATAMENTE "Tarefas", não usar outro database.

**2.2 - Validar Schema (OBRIGATÓRIO):**
```
Use: mcp_notion-mcp-server_API-retrieve-a-database
database_id: {DATABASE_ID}
```

Verificar propriedades obrigatórias:

> **Seguir skill `notion-task-patterns`** → Seção "📋 PROPRIEDADES OBRIGATÓRIAS"

**Se QUALQUER propriedade estiver ausente:**
```
⚠️ **PROPRIEDADES AUSENTES** no database 'Tarefas':

| Propriedade | Tipo Esperado |
|-------------|---------------|
| {nome} | {tipo} |

**Por favor, crie estas propriedades no Notion antes de continuar.**

🔗 [Abrir database no Notion]({notion_url})

**AGUARDANDO** confirmação após criar as propriedades...
```

> [!CAUTION]
> **NÃO prossiga** para o Passo 3 até que TODAS as propriedades existam.

**Se não encontrar database "Tarefas":**
```
⚠️ Database "Tarefas" não encontrado.

Para registrar as melhorias no Notion:
1. Crie um database "Tarefas" com as propriedades obrigatórias
2. Execute: /legacy-project --resume

Ou prossiga sem Notion (não recomendado para transparência).
```

#### Passo 2.5: ID Continuity Check (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de criar QUALQUER task nova, verificar IDs existentes
> no Notion para evitar gaps de numeração no `LEGACY-PROGRESS.md`.
> **Mesmo procedimento da Phase 3.5 — Passo 2.5.**

**2.5.1 - Consultar todas as tasks existentes no database:**

Usar `post-search` com paginação para obter todas as pages do database.

**2.5.2 - Construir mapa de IDs existentes:**

Extrair `properties.ID.unique_id.number`, título e status de cada task.

**2.5.3 - Comparar com `LEGACY-PROGRESS.md` → seção "📋 Registro de Tasks Notion":**

1. Identificar IDs presentes no Notion mas **ausentes** no arquivo local
2. Se houver gaps → registrar tasks faltantes ANTES de criar novas
3. Anotar `max_id` para documentar corretamente os novos IDs

> [!IMPORTANT]
> **Último ID registrado:** Anotar o maior ID existente. Novas tasks terão IDs
> a partir de `max_id + 1`. Usar este valor ao documentar no LEGACY-PROGRESS.md.

#### Passo 3: Criar Tasks no Notion

Para **CADA melhoria** identificada:

> **Seguir skill `notion-task-patterns`** → Seção "➕ Criar Task"

> [!CAUTION]
> **OBRIGATÓRIO:** `Estimativa` deve ser preenchido ao criar cada task.

> **ID para Refatorações:** Usar `R.{seq}` (ex: `R.1`, `R.2`) ou `{módulo}.{seq}` (ex: `auth.1`)

#### Passo 4: Popular Corpo da Task

> **Seguir skill `notion-task-patterns`** → Seção "📝 Adicionar Corpo" com template por categoria.

#### Passo 5: Relatório de Tasks Criadas

```
📊 TASKS CRIADAS PARA {projeto} - {módulo}

| # | Task | Prioridade | Estimativa | Link |
|---|------|------------|------------|------|
| 1 | Remover código morto em auth | P1 | 4h | 🔗 |
| 2 | Atualizar dependências | P2 | 2h | 🔗 |
| 3 | Adicionar validação de input | P0 | 3h | 🔗 |

Total: X tasks criadas
Estimativa total: Xh

✅ Cliente pode acompanhar progresso em: View "Visão Cliente"
```

### 🛑 GATE: Phase 7A → Phase 7B (APROVAÇÃO OBRIGATÓRIA)

> [!CAUTION]
> **BLOQUEADOR:** O agente NÃO PODE iniciar a execução (Phase 7B) sem aprovação
> explícita do breakdown pelo usuário.

**Checklist (OBRIGATÓRIO):**
```markdown
⚠️ VERIFICAÇÃO ANTES DE EXECUTAR MELHORIAS

[ ] Todos os débitos P0/P1/P2/P3 do TDD têm task no Notion?
[ ] Cada task tem corpo preenchido (Problema + Solução + Impacto)?
[ ] Usuário aprovou o breakdown e prioridades?
[ ] Escopo de execução definido (ex: apenas P0 neste ciclo)?

❌ Se QUALQUER item desmarcado → NÃO PROSSEGUIR
✅ TODOS marcados → Prosseguir para Phase 7B
```

**Checkpoint salvo:** Tasks criadas no Notion, breakdown aprovado

---

### Phase 7B: EXECUÇÃO DE MELHORIAS (Implementação)

> **Skill obrigatória:** `context-gathering-patterns` — seguir PROCESSO DE CONTEXT GATHERING antes de cada task.

**Objetivo:** Implementar as melhorias aprovadas no breakdown (Phase 7A).

**Trigger:**
```
Phase 7A concluída + Gate aprovado pelo usuário
```

**Agentes Envolvidos:**
- Especialista conforme stack (backend/frontend/mobile)
- `orchestrator` - Integração Notion

> [!IMPORTANT]
> **Escopo:** Executar apenas as tasks aprovadas no gate (tipicamente P0s).
> P1/P2/P3 ficam como backlog para próximos ciclos.

#### Processo: Para CADA Task Aprovada

#### 🛑 Passo 0: Context Gathering (GATE OBRIGATÓRIO POR TASK)

> [!CAUTION]
> **GATE BLOQUEANTE POR TASK:** Para CADA task da Phase 7B, o agente DEVE completar
> o checklist abaixo E registrá-lo no `LEGACY-PROGRESS.md` ANTES de tocar no código.
>
> Se a conversa for retomada (resume/checkpoint), o agente DEVE verificar se o
> checklist está preenchido para a task atual — se não estiver, re-executar.
> (Ver Phase 0 → Passo 0.6)

> [!WARNING]
> **Anti-pattern real (Task #21):** Agente retomou conversa truncada e saltou
> Context Gathering. Inferiu tipos (`unavailable_products`) a partir do código,
> ignorando documentação de fluxo de checkout/pagamento. Resultado: decisão de
> tipo potencialmente incorreta que poderia causar bugs em runtime.
> **NUNCA** inferir comportamento esperado apenas do código — consultar docs primeiro.

**Ações do Context Gathering:**

   a. Ler o **corpo completo da task no Notion** (checklist, critérios de aceite, arquivos afetados)
   b. Ler seção **🔗 Referências** da task → abrir TDD referenciado (seções específicas)
   c. Buscar **documentação de fluxo** relevante em `docs/flows/` (usar keywords da task: pagamento → `checkout/`, autenticação → `auth/`, etc.)
   d. Se a task envolver pagamento/checkout/cart → ler `docs/flows/shop/checkout/` obrigatoriamente
   e. Sintetizar contexto e preencher checklist de evidência abaixo

**Checklist de Evidência (salvar em `LEGACY-PROGRESS.md` sob a task):**

```markdown
📖 CONTEXT GATHERING — Task #{id}: {título}
[ ] Corpo da task lido no Notion (ID: {page_id})
[ ] TDD referenciado lido: {seção específica ou "N/A"}
[ ] Docs de fluxo consultados: {lista de arquivos em docs/flows/ ou "Nenhum relevante"}
[ ] Síntese de contexto escrita abaixo

**Decisões de negócio relevantes:**
- {decisão 1}

**Tipos/contratos esperados (do TDD/docs, NÃO do código):**
- {tipo 1}: {definição conforme documentação}

**Restrições identificadas:**
- {restrição 1}
```

> [!IMPORTANT]
> **Validação:** O agente deve ter PELO MENOS 1 item preenchido em cada seção
> (decisões, tipos, restrições) para prosseguir. Se a documentação está vazia ou
> inexistente para o escopo da task, registrar:
> `"⚠️ Docs ausentes — decisões baseadas em análise do código (risco elevado)"`
> como flag explícita de risco.

**Somente após o checklist estar preenchido e salvo:**

1. **Atualizar Notion:** Status → "Em Progresso", `% Progresso: 10`
2. **Implementar:** Aplicar a correção **considerando o contexto do Passo 0**
3. **Testar:** Executar testes existentes + novos se necessário
4. **Verificar:** Confirmar que nenhum teste quebrou
5. **Completar:** Executar `/task-complete` (atualiza Notion + LEGACY-PROGRESS.md)

#### 🔄 NOTION SYNC - Phase 7B (OBRIGATÓRIO)

> [!CAUTION]
> **Ao concluir CADA task de melhoria**, executar sync.
> Seguir skill `notion-task-patterns` → seção "PHASE TASK TRACKING" → "Gate: NOTION SYNC".

Para cada task concluída:
1. Atualizar task → Status: "Concluído", `Tempo Gasto`, `% Progresso: 100`
2. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    { "type": "callout", "callout": { "icon": { "type": "emoji", "emoji": "✅" }, "rich_text": [{ "type": "text", "text": { "content": "Concluído em {data}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📋 {resumo da implementação}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📁 Arquivos: {lista de arquivos modificados}" } }] } }
  ]
}
```

3. Adicionar comentário rico de conclusão

**Ao concluir TODAS as tasks aprovadas:**
4. Verificar que TODAS as tasks de melhorias estão synced (Gate de Conclusão)
5. Atualizar `LEGACY-PROGRESS.md`

**Checkpoint salvo:** Melhorias implementadas e synced no Notion

---

### Phase 8: PUBLICAÇÃO DE DOCUMENTAÇÃO TÉCNICA NO NOTION

> [!CAUTION]
> **REGRA BLOQUEANTE:** Toda documentação gerada nas fases 4-6 DEVE ser publicada
> na database "Documentação Técnica" do Notion para **acesso da equipe de desenvolvimento**.
> Os devs leem no Notion — NÃO acessam o repositório.

**Objetivo:** Publicar documentação completa na database Notion "Documentação Técnica" para acesso dos devs.

**Trigger:**
```
Phase 7B concluída → Automático
```

**Agentes Envolvidos:**
- `orchestrator` - Integração Notion

> [!IMPORTANT]
> **SKILL:** Seguir `notion-task-patterns` → seção "DOCUMENTATION DATABASES" OBRIGATORIAMENTE.

#### Passo 1: Discovery e Validação da Database "Documentação Técnica"

> Seguir skill `notion-task-patterns` → seção "DATABASE 1"

```json
// Tool: mcp_notion-mcp-server_API-post-search
{
  "query": "Documentação Técnica",
  "filter": { "property": "object", "value": "data_source" }
}
```

```json
// Tool: mcp_notion-mcp-server_API-retrieve-a-database
{ "database_id": "{DOC_TECNICA_DATABASE_ID}" }
```

> Se database ausente ou propriedades faltando → PARAR e notificar usuário (ver skill para mensagem).

#### Passo 2: Coletar Artefatos Gerados

Listar todos os docs gerados nas fases anteriores:

| Fonte | Tipo | Arquivo Local | Publicar? |
|---|---|---|---|
| Phase 1 | Arquitetura | `docs/CODEBASE-{projeto}.md` | ✅ |
| Phase 4 | Fluxo | `docs/flows/{módulo}/{fluxo}.md` (cada) | ✅ |
| Phase 5 | TDD | `docs/design/TDD-{projeto}-{módulo}.md` | ✅ |
| Phase 5.5 | Design System | `design-system/MASTER.md` | ✅ (se UI) |
| Phase 6 | Testes | (relatório de cobertura) | ✅ |

#### Passo 3: Para Cada Artefato — Publicar

> Seguir skill `notion-task-patterns` → seção "Processo: Publicação de Documentação Técnica"

Para cada doc:

1. **Verificar upsert** — doc já existe na database? (query por Nome + Módulo)
2. **Ler conteúdo completo** do arquivo local
3. **Criar ou atualizar** página Notion com template correto para o tipo
4. **Preencher propriedades:** Nome, Módulo, Tipo, Status, Última Atualização, Arquivo Local, Tasks Relacionadas
5. **Incluir histórico** de atualizações referenciando tasks da database "Tarefas"

#### Passo 4: Relatório de Publicação

```markdown
📚 **DOCUMENTAÇÃO TÉCNICA PUBLICADA - {módulo}**

| # | Documento | Tipo | Status | Notion |
|---|-----------|------|--------|--------|
| 1 | {nome} | Fluxo | Publicado | 🔗 |
| 2 | {nome} | TDD | Publicado | 🔗 |
| ... | ... | ... | ... | ... |

Total: {N} documentos publicados
✅ Devs podem consultar em: Notion → Database "Documentação Técnica"
```

**Gate de Saída:**
```
[ ] Database "Documentação Técnica" encontrado e validado
[ ] Todos os artefatos de Phase 4-6 publicados
[ ] Upsert verificado (sem duplicatas)
[ ] Histórico de atualizações em cada doc
[ ] Tasks relacionadas referenciadas em cada doc
[ ] LEGACY-PROGRESS.md atualizado
```

**Checkpoint salvo:** Documentação técnica publicada no Notion

---

### Phase 8.5: PUBLICAÇÃO DO MANUAL DO USUÁRIO NO NOTION

> [!CAUTION]
> **REGRA BLOQUEANTE:** Para cada fluxo publicado na Phase 8, DEVE existir uma versão
> em linguagem acessível na database "Manual do Usuário" do Notion.
> Usuários finais e operadores leem estes guias — sem código, sem jargão técnico.

**Objetivo:** Publicar guias em linguagem acessível na database Notion "Manual do Usuário".

**Trigger:**
```
Phase 8 concluída → Automático
```

**Agentes Envolvidos:**
- `orchestrator` - Integração Notion

> [!IMPORTANT]
> **SKILL:** Seguir `notion-task-patterns` → seção "Processo: Publicação do Manual do Usuário" OBRIGATORIAMENTE.

#### Passo 1: Discovery e Validação da Database "Manual do Usuário"

> Seguir skill `notion-task-patterns` → seção "DATABASE 2"

```json
// Tool: mcp_notion-mcp-server_API-post-search
{
  "query": "Manual do Usuário",
  "filter": { "property": "object", "value": "data_source" }
}
```

> Se database ausente → PARAR e notificar usuário (ver skill para mensagem).

#### Passo 2: Mapear Fluxos → Guias

> Seguir skill `notion-task-patterns` → tabela "Mapear Fluxos Técnicos → Guias de Usuário"

Para cada fluxo publicado na Phase 8, gerar versão em linguagem acessível.

#### Passo 3: Publicar Guias

Para cada guia:
1. **Verificar upsert** — guia já existe? (query por Nome)
2. **Gerar conteúdo** em linguagem simples (sem código, sem componentes, sem libs)
3. **Criar ou atualizar** página com template de guia do usuário
4. **Definir propriedades:** Nome, Seção, Status, Público-alvo

#### Passo 4: Relatório de Publicação

```markdown
📖 **MANUAL DO USUÁRIO PUBLICADO - {módulo}**

| # | Guia | Público-alvo | Seção | Status |
|---|------|-------------|-------|--------|
| 1 | {nome} | Usuário Final | {seção} | Publicado |
| ... | ... | ... | ... | ... |

Total: {N} guias publicados
✅ Usuários e operadores podem consultar em: Notion → Database "Manual do Usuário"
```

**Gate de Saída:**
```
[ ] Database "Manual do Usuário" encontrado e validado
[ ] Todos os fluxos mapeados para guias
[ ] Upsert verificado (sem duplicatas)
[ ] Conteúdo sem jargão técnico
[ ] LEGACY-PROGRESS.md atualizado
```

**Checkpoint salvo:** Manual do usuário publicado no Notion

---

### Phase 9: PRÓXIMO ESCOPO (GATE BLOQUEANTE)

> [!CAUTION]
> **REGRA BLOQUEANTE:** O workflow `/legacy-project` NÃO PODE ser considerado concluído
> enquanto houver escopos com status `⏳ Pendente` no `LEGACY-PROGRESS.md`.
> O agente DEVE obrigatoriamente executar esta phase antes de encerrar.

**Objetivo:** Verificar se há mais módulos para analisar e **impedir encerramento prematuro**.

**Trigger:**
```
Phase 8.5 concluída
```

**Ações:**
1. Ler `docs/LEGACY-PROGRESS.md` → seção "Mapeamento de Escopos"
2. Contar escopos com status `⏳ Pendente`
3. Atualizar task master no Notion (se houver)

**Se há escopos pendentes (OBRIGATÓRIO):**
```
✅ Módulo {módulo} concluído!

📊 Resumo:
- Fluxos documentados: X
- Tasks criadas no Notion: Y
- Cobertura de testes: Z%
- 📚 Docs publicados para cliente: W

📚 Devs consultam: Notion → Database "Documentação Técnica"
📖 Usuários consultam: Notion → Database "Manual do Usuário"

⚠️ ATENÇÃO: Existem {N} escopos ainda NÃO analisados:

| Escopo | Criticidade | Status |
|--------|-------------|--------|
| {escopo} | {criticidade} | ⏳ Pendente |

🔴 O workflow NÃO está concluído até que todos os escopos sejam analisados.

Deseja:
1. Continuar com o próximo módulo agora
2. Pausar e retomar depois (/legacy-project --resume)
```

> [!WARNING]
> **O agente NÃO PODE encerrar a sessão sem mostrar esta mensagem.**
> Mesmo que o usuário escolha "pausar", os escopos pendentes ficam registrados
> no `LEGACY-PROGRESS.md` para retomada futura.

**Se todos concluídos:**
```
🎉 TODOS os escopos foram analisados!

📊 Relatório Final:
| Escopo | Phases | Tasks | Docs |
|--------|--------|-------|------|
| {escopo} | 8/8 ✅ | {N} | {N} |

📚 Documentação completa disponível em:
  - Notion → Database "Documentação Técnica" (devs)
  - Notion → Database "Manual do Usuário" (usuários e operadores)
```

**Checkpoint salvo:** Módulo marcado como completo, escopos pendentes listados

---

## 📁 Estrutura de Arquivos Gerados

```
projeto/
├── docs/
│   ├── LEGACY-PROGRESS.md              # ⭐ Arquivo de controle
│   ├── CODEBASE-{projeto}.md           # Visão geral
│   ├── INDEX.md                         # Atualizado
│   ├── flows/
│   │   ├── auth/                        # Por módulo
│   │   │   ├── login.md
│   │   │   └── register.md
│   │   └── payment/
│   │       ├── checkout.md
│   │       └── refund.md
│   └── design/
│       ├── TDD-{projeto}-auth.md        # TDD por módulo
│       └── TDD-{projeto}-payment.md
└── tests/
    ├── integration/
    └── unit/
```

---

## 📋 Template: LEGACY-PROGRESS.md

```markdown
# Legacy Project Progress - {projeto}

> Arquivo de controle para retomar workflow de onde parou.
> ⚠️ NÃO EDITAR MANUALMENTE - Atualizado automaticamente.

## 📊 Status Geral

| Campo | Valor |
|-------|-------|
| Projeto | {nome} |
| Path | {caminho} |
| Iniciado em | {data} |
| Última atualização | {data} |
| Status | 🟡 Em Progresso |
| Fase Atual | {fase}/8 |
| Escopo Atual | {módulo} |

---

## 🗺️ Mapeamento de Escopos

| Escopo | Criticidade | Status | Fase | Última Ação |
|--------|-------------|--------|------|-------------|
| `src/auth` | 🔴 Alta | ✅ Completo | 8/8 | Tasks criadas |
| `src/payment` | 🔴 Alta | 🟡 Em Progresso | 5/8 | TDD Reverso |
| `src/users` | 🟡 Média | ⏳ Pendente | - | - |

---

## 📝 Escopo Atual: `{módulo}`

### Phase 3: Análise ✅
- [x] Stack detectada
- [x] Estrutura mapeada
- [x] Fluxos identificados: {N}

### Phase 4: Documentação 🟡
- [x] `docs/flows/{módulo}/fluxo-1.md`
- [ ] `docs/flows/{módulo}/fluxo-2.md`
- [ ] `docs/flows/{módulo}/fluxo-3.md`

### Phase 5: TDD Reverso ⏳
### Phase 6: Testes ⏳
### Phase 7A: Breakdown de Melhorias ⏳
### Phase 7B: Execução de Melhorias ⏳
### Phase 8: Publicação ⏳
### Phase 9: Próximo Escopo ⏳

---

## 📜 Histórico de Ações

| Data | Fase | Ação |
|------|------|------|
| 2025-01-15 10:30 | 1 | Overview concluído |
| 2025-01-15 11:00 | 2 | Escopo src/auth selecionado |
| 2025-01-15 14:00 | 4 | Fluxo login documentado |
| ... | ... | ... |

---

## 🔄 Para Retomar

\```bash
/legacy-project --resume
\```
```

---

## 🔗 INTEGRAÇÃO COM NOTION (Automática na Phase 7A)

> [!IMPORTANT]
> A integração com Notion é **automática** na Phase 7A.
> A flag `--notion` agora é apenas para tracking do workflow em si.

### Tasks de Melhorias (Phase 7A/7B)

Para cada melhoria identificada, uma task é criada automaticamente:

| Propriedade | Valor |
|-------------|-------|
| Título | `{descrição}` |
| ID | `R.{seq}` ou `{módulo}.{seq}` |
| Épico | `{módulo}` (ex: auth, payment) |
| Status | `A Fazer` |
| Categoria | `Refatoração` |
| Prioridade | `P0-P3` |
| Corpo | Contexto + Problema + Solução |

### View "Visão Cliente"

Para transparência, crie view filtrada no Notion:
- Apenas: Nome, Status
- Ver instruções em `README.md` seção "Configuração > Notion"

### Tracking do Workflow (Opcional com --notion)

Se `--notion` especificado, também cria:

1. **Task Master:** `🏗️ Legacy: {projeto}` (% calculado)
2. **Sub-tasks:** Uma por módulo (`📦 {módulo}`)

---

## 🔴 REGRAS CRÍTICAS

1. **Sempre salvar checkpoint** após cada fase
2. **Um módulo por vez** - não paralelizar análise
3. **Aprovação humana** no TDD Reverso
4. **Priorizar críticos** - auth e payment primeiro
5. **Testes antes de refactoring**
6. **Incremental** - não tentar analisar tudo de uma vez
7. **🔄 NOTION OBRIGATÓRIO** - Toda atividade pós-análise (Phase 4+) DEVE ter task no Notion. Seguir skill `notion-task-patterns` → "PHASE TASK TRACKING". Trabalho sem task = falha de transparência
8. **🔀 PHASE 7A ≠ 7B** - Phase 7A (Breakdown) cria tasks no Notion a partir do TDD. Phase 7B (Execução) implementa as melhorias aprovadas. NUNCA misturar planejamento com execução na mesma phase. O gate entre 7A→7B é OBRIGATÓRIO
9. **📚 DOCUMENTAÇÃO PARA DEVS E USUÁRIOS** - Ao final de cada módulo (Phase 8 + 8.5), publicar docs completos nas databases "Documentação Técnica" e "Manual do Usuário" do Notion. Seguir skill `notion-task-patterns` → "DOCUMENTATION DATABASES"
10. **🛡️ ESCOPOS PENDENTES = WORKFLOW INCOMPLETO** - O workflow NÃO PODE ser considerado encerrado se existirem escopos com status `⏳ Pendente` no `LEGACY-PROGRESS.md`. Ao finalizar qualquer phase, o agente DEVE verificar escopos pendentes e informar o usuário. Ignorar escopos = falha de cobertura
11. **📋 SEQUÊNCIA DE PHASES/TASKS OBRIGATÓRIA** - O agente DEVE seguir a ordem numérica: Phase 4 → 5 → 5.5 → 6 → 7A → 7B → 8 → 9. Ao sugerir "próximos passos", DEVE consultar `LEGACY-PROGRESS.md` para identificar a próxima phase pendente. **PROIBIDO** sugerir tasks de phases posteriores enquanto a phase atual tiver tasks incompletas. Exemplo: NÃO sugerir Phase 7B (Execução) quando Phase 7A (Breakdown) ainda não foi aprovada
12. **📊 PROGRESS SYNC OBRIGATÓRIO** - Ao concluir QUALQUER phase, o `LEGACY-PROGRESS.md` DEVE ser atualizado IMEDIATAMENTE com: (a) checklist da phase marcado como ✅, (b) fase atual incrementada, (c) data de última atualização, (d) entrada no histórico de ações. Antes de sugerir "próximos passos", o agente DEVE verificar se o `LEGACY-PROGRESS.md` está atualizado

---

## Usage Examples

```bash
# Análise completa com seleção interativa de escopo
/legacy-project c:\projetos\meu-app-grande

# Analisar apenas um módulo específico
/legacy-project --scope src/auth c:\projetos\monorepo

# Priorizar fluxos críticos automaticamente
/legacy-project --critical-first c:\projetos\app

# Retomar de onde parou
/legacy-project --resume

# Ver status detalhado
/legacy-project status

# Com sincronização Notion
/legacy-project --notion c:\projetos\app

# Forçar re-análise
/legacy-project --scope src/auth --force c:\projetos\app
```

---

## 📋 Comparativo de Modos

| Aspecto | Completo | --scope | --quick | --critical-first |
|---------|----------|---------|---------|------------------|
| Overview | ✅ | ❌ | ✅ | ✅ |
| Seleção interativa | ✅ | ❌ (usa scope) | ❌ | ❌ (auto) |
| Documentação detalhada | ✅ | ✅ | ❌ | ✅ |
| TDD Reverso | ✅ | ✅ | ✅ (simples) | ✅ |
| Checkpointing | ✅ | ✅ | ✅ | ✅ |
| Múltiplos escopos | ✅ | ❌ (1 por vez) | ❌ | ✅ |
| Recomendado para | Projeto médio | Debug específico | MVP rápido | Projeto grande |
