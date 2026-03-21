---
description: Workflow unificado para projeto legado. Análise → Documentação → TDD Reverso → Design System → Melhorias. Engenharia reversa e modernização. Suporta projetos grandes com checkpointing.
skills: checkpointing-patterns, project-tracking-patterns
---

# /legacy-project - Projeto Legado Completo

$ARGUMENTS

**Arguments:**

| Flag               | Descrição                                 | Exemplo            |
| ------------------ | ----------------------------------------- | ------------------ |
| `--scope [path]`   | Analisar apenas um módulo/domínio         | `--scope src/auth` |
| `--resume`         | Retomar de onde parou                     | `--resume`         |
| `--critical-first` | Priorizar fluxos críticos (auth, payment) | `--critical-first` |
| `--analyze-only`   | Apenas análise, sem TDD                   | `--analyze-only`   |
| `--quick`          | Análise rápida + TDD direto               | `--quick`          |
| `--flyee`          | Sincronizar progresso com Flyee           | `--flyee`          |
| `--force`          | Forçar re-análise (ignora cache)          | `--force`          |

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

| Situação                           | Workflow                           |
| ---------------------------------- | ---------------------------------- |
| Projeto existente sem documentação | `/legacy-project`                  |
| Monorepo grande                    | `/legacy-project --scope [módulo]` |
| Retomar trabalho interrompido      | `/legacy-project --resume`         |
| Documentar UM fluxo específico     | `/document [fluxo]`                |
| Projeto novo do zero               | `/new-project`                     |

---

## 🧩 SUBCOMMANDS

| Comando                                   | Ação                                      |
| ----------------------------------------- | ----------------------------------------- |
| `/legacy-project [path]`                  | Fluxo **completo** com seleção de escopo  |
| `/legacy-project --scope [módulo] [path]` | Analisar **apenas** o módulo especificado |
| `/legacy-project --resume`                | **Retomar** de onde parou                 |
| `/legacy-project --critical-first [path]` | Priorizar **fluxos críticos**             |
| `/legacy-project --quick [path]`          | Análise rápida + TDD direto               |
| `/legacy-project status`                  | Mostrar **status** e progresso            |

---

## 💾 SISTEMA DE CHECKPOINTING

> [!IMPORTANT]
> **Projetos grandes precisam de persistência.**
> O workflow salva progresso em `docs/LEGACY-PROGRESS.md` a cada fase.
> Seguir skill `checkpointing-patterns` para detalhes de persistência e resume.

### Arquivo de Controle: `docs/LEGACY-PROGRESS.md`

Criado automaticamente ao iniciar o projeto. Contém:

| Seção                 | Conteúdo                                      |
| --------------------- | --------------------------------------------- |
| Status Geral          | Projeto, path, fase atual, última atualização |
| Configurações         | Destino de Tasks, Idioma                      |
| Mapeamento de Escopos | Lista de todos os módulos e seu status        |
| Escopo Atual          | Checklist detalhado da fase em andamento      |
| Histórico             | Log de ações realizadas                       |

### Retomada: `--resume`

```bash
/legacy-project --resume
```

Ao executar `--resume`:

1. Carrega `docs/LEGACY-PROGRESS.md`
2. Identifica fase pendente
3. Executa **Auto-Anchor** de tasks órfãs (Phase 0 Passo 0.5)
4. Executa **Retroactive Task-Complete Gate** (Phase 0 Passo 0.55)
5. Executa **Context Re-Check** se retomando Phase 7B (Phase 0 Passo 0.6)
6. Continua execução

---

## 🔴 FLUXO COMPLETO

```
Phase 0   →  Phase 1  →  Phase 2  →  Phase 2.5 → Phase 3  →  Phase 3.5
CHECKPOINT   OVERVIEW    ESCOPO     CROSS-SCOPE   ANÁLISE    TASK SETUP
   ✅          ✅          ✋           🔗          ✅          ✅

→  Phase 4    →  Phase 5  →  Phase 5.5 → Phase 6  → Phase 7A → Phase 7B → Phase 8 → Phase 8.5 → Phase 9
   DOCUMENTAÇÃO  TDD REVERSO  DESIGN SYS  TESTES    BREAKDOWN   EXECUÇÃO   HANDOVER   USER MANUAL  PRÓXIMO
     ✅ 🔄         ✋ 🔄        ✅ 🔄       ✅ 🔄      ✋ Gate     ✅ 🔄      📚          📖         🔁
```

> 🔗 = Carrega contexto de escopos concluídos (handover, TDD, flows, débitos)
> 🔄 = TASK SYNC obrigatório (skill `project-tracking-patterns` → seção 7)
> 📚 = Handover + Publicação técnica (skill `documentation-publishing`)
> 📖 = Manual do Usuário (skill `documentation-publishing`)

---

### Phase 0: CHECKPOINTING - Verificar Estado

**Objetivo:** Verificar se existe trabalho anterior e decidir ação.

**Trigger:** `/legacy-project [path]`

**Ações:**

1. Verificar se existe `docs/LEGACY-PROGRESS.md`
2. Se existe: Perguntar ao usuário (retomar / reiniciar / novo escopo)
3. Se não existe: Criar arquivo e prosseguir

#### Passo 0.5: Auto-Anchor de Tasks Órfãs (--resume, APENAS MODO FLYEE)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Ao retomar, ANTES de continuar qualquer fase,
> verificar tasks órfãs no Flyee (criadas em conversas paralelas).

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Pular Passos 0.5 e 0.55 inteiramente.

1. Consultar todas as tasks no database "Tarefas" (paginado)
2. Comparar com "📋 Registro de Tasks Flyee" do `LEGACY-PROGRESS.md`
3. Para cada task órfã — auto-classificar por Categoria/Épico:

| Categoria da task | Fase destino |
| ----------------- | ------------ |
| Documentação      | Phase 4 ou 8 |
| Refatoração       | Phase 7B     |
| Testes            | Phase 6      |
| Outra             | Phase 8      |

4. Verificar duplicatas → fechar se idêntica a task já rastreada
5. Atualizar `LEGACY-PROGRESS.md` com tasks ancoradas

#### Passo 0.55: Retroactive Task-Complete Gate (--resume, APENAS MODO FLYEE)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Verificar se tasks "✅ Concluído" no LEGACY-PROGRESS.md
> foram **completamente** sincronizadas no Flyee. Sessões anteriores podem ter
> feito sync parcial (causa raiz das falhas v1-v4).

> **Skill:** `project-tracking-patterns` → seção "7. TASK SYNC" para regras e anti-patterns.

Para cada task concluída no LEGACY-PROGRESS.md:

1. Verificar no Flyee: Status = Concluído? Comentário existe? Nota inline existe?
2. Se QUALQUER faltando → executar `/task-complete` retroativamente
3. Checklist pós-sync (BLOQUEIA prosseguimento):

```
| Task | patch-page | nota inline | comentário | LEGACY-PROGRESS |
|------|-----------|-------------|------------|-----------------| 
| #{id} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
```

> 🚫 **ANTI-PATTERN:** Chamadas avulsas a `API-patch-page` SEM `/task-complete` completo.

#### Passo 0.6: Context Re-Check (--resume de Phase 7B)

> [!CAUTION]
> Se retomando Phase 7B, verificar Context Gathering da task em andamento.

1. Buscar seção `🔧 TASK ATIVA` no LEGACY-PROGRESS.md
   - Se existe → Task interrompida. Retomar do passo registrado
   - Se não existe → Buscar task `[/]` em progresso
2. Verificar checklist `📖 CONTEXT GATHERING — Task #{id}`
   - Se preenchida → prosseguir
   - Se incompleta → re-executar Context Gathering (Phase 7B Passo 0)

---

### Phase 1: OVERVIEW - Mapeamento de Alto Nível

**Objetivo:** Entender a estrutura geral do projeto SEM analisar tudo.

**Ações:**

1. Detectar tipo de projeto (Monorepo / Modular / Monolítico)
2. Mapear módulos/domínios de alto nível
3. Identificar fluxos críticos por keywords:

| Keyword | Criticidade |
|---------|-------------|
| `auth`, `login`, `session` | 🔴 Alta |
| `payment`, `checkout`, `billing` | 🔴 Alta |
| `user`, `profile`, `account` | 🟡 Média |
| Outros | 🟢 Normal |

4. Gerar `docs/CODEBASE-{projeto}.md`

---

### Phase 2: SELEÇÃO DE ESCOPO

**Objetivo:** Escolher qual módulo analisar primeiro.

**Ações:**

1. Apresentar módulos com recomendação
2. **AGUARDAR** seleção do usuário (ou usar `--scope` / `--critical-first`)
3. Registrar escopo no LEGACY-PROGRESS.md

> Se `flyee.json` existe: Registrar decisão via `bridge.py --create-decision`

---

### Phase 2.5: CROSS-SCOPE CONTEXT

> [!CAUTION]
> **Se existem escopos já concluídos**, esta fase é OBRIGATÓRIA antes da análise.
> Se é o primeiro escopo → pular para Phase 3.

> **Skill:** `code-truth-validation` → seção "3. Cross-Scope Doc-vs-Code"

**Ações:**

1. Identificar escopos concluídos no LEGACY-PROGRESS.md
2. Carregar docs de cada escopo (handover → TDD → flows → test guide)
3. Construir mapa de dependências cruzadas:
   - Endpoints/APIs consumidos entre escopos
   - Models/Entities compartilhadas
   - Melhorias que impactam o novo escopo
   - Débitos técnicos referentes ao novo escopo
4. **Validar doc-vs-code** (skill `code-truth-validation` → seções 1 e 3)
5. Registrar contexto e divergências no LEGACY-PROGRESS.md

**Gate de Saída:**
```
[ ] Docs de escopos anteriores lidos
[ ] Mapa de dependências cruzadas construído
[ ] Divergências doc-vs-code verificadas
[ ] Contexto registrado em LEGACY-PROGRESS.md
```

---

### Phase 3: ANÁLISE DETALHADA DO ESCOPO

**Objetivo:** Analisar profundamente o módulo selecionado.

> [!IMPORTANT]
> Se Phase 2.5 foi executada, levar em conta o contexto cross-scope.

**Ações:**

1. Executar `/discovery --from-project [escopo]`
2. Detectar stack, mapear estrutura, identificar entry points e fluxos
3. Listar dependências internas e externas
4. Atualizar `docs/CODEBASE-{projeto}.md` com seção do módulo

---

### Phase 3.5: TASK SETUP + BREAKDOWN DE FASES

> [!CAUTION]
> **REGRA BLOQUEANTE:** DEVE ser executada ANTES de qualquer trabalho nas fases 4-7.
> Toda atividade pós-análise precisa de tasks registradas.

> **Skill:** `project-tracking-patterns` → seções 4-7 para sync e completion.

#### Passo 0: Escolha de Destino das Tasks

Perguntar ao usuário: **Flyee** ou **Local**?

- **Flyee** → Tasks no database "Tarefas" (transparência com cliente)
- **Local** → Tasks em `docs/analysis/{escopo}/BREAKDOWN-{escopo}.md`

Salvar em LEGACY-PROGRESS.md → "⚙️ Configurações".

#### Passo 1: Discovery/Validação (APENAS FLYEE)

> Se Local → pular para Passo 3.

1. Buscar database "Tarefas" no Flyee
2. Validar schema (propriedades obrigatórias)
3. ID Continuity Check (construir mapa de IDs, detectar gaps)

#### Passo 2: Perguntar Idioma (se não definido)

#### Passo 3: Criar Tasks para Fases 4-7

Tasks a criar (1 por fluxo identificado + TDD + DS + testes):

> [!CAUTION]
> **Títulos SEM prefixos** (`[DOC]`, `[TDD]` etc.) — Categoria já cumpre essa função.
> **Tasks de melhorias (Phase 7A)** são criadas DEPOIS do TDD Reverso.

> [!CAUTION]
> **CORPO OBRIGATÓRIO (operação atômica):**
> 1. `API-post-page` (criar com propriedades)
> 2. `API-patch-block-children` (adicionar corpo)
> 3. Só então próxima task. **NÃO** fazer batch da etapa 1.

**Se Local:** Criar `BREAKDOWN-{escopo}.md` com template de tasks locais.
LEGACY-PROGRESS.md mantém apenas referência ao BREAKDOWN + checklist de IDs.

#### Verificação e Relatório

- Verificar 100% das tasks com corpo preenchido
- Exibir relatório de tasks criadas
- Atualizar LEGACY-PROGRESS.md

---

### Phase 4: DOCUMENTAÇÃO DOS FLUXOS

**Objetivo:** Documentar cada fluxo do módulo selecionado.

> [!CAUTION]
> **PRÉ-REQUISITO:** Phase 3.5 DEVE estar concluída.

> **Skill:** `code-truth-validation` → seção "1. Checklist de Validação" (antes de salvar cada doc)

#### 🔁 Loop: Para cada fluxo identificado

**Etapa A — Gerar Documentação:**

1. Executar `/document [nome-do-fluxo]`
2. Gerar documentação estruturada
3. **CODE-TRUTH VALIDATION** (skill `code-truth-validation` → seções 1-2)
4. Salvar em `docs/flows/{módulo}/{fluxo}.md`

**Etapa B — 🛑 GATE OBRIGATÓRIO:**

5. **EXECUTAR `/task-complete {task_id} "{tempo}"`** — workflow completo

> **Skill:** `project-tracking-patterns` → seção "7. TASK SYNC" para template e regras.
> 🚫 **PROIBIDO** substituir `/task-complete` por chamadas avulsas a `API-patch-page`.

#### 🧠 Self-Check Anti-Bypass

> **Skill:** `project-tracking-patterns` → "Self-Check Anti-Bypass"
> Antes de iniciar próximo fluxo, verificar: `/task-complete` executado? Comentário no Flyee? LEGACY-PROGRESS atualizado?

---

### Phase 5: TDD REVERSO

**Objetivo:** Gerar TDD a partir do código analisado.

> **Skill:** `tdd-workflow` para princípios de TDD.

**Ações:**

1. Consolidar informações das documentações
2. Extrair arquitetura do módulo
3. Identificar débitos técnicos e priorizar:

| Prioridade | Critério |
|------------|----------|
| P0 | Segurança, bugs críticos |
| P1 | Performance, fluxos principais |
| P2 | Refactoring, qualidade |
| P3 | Nice-to-have |

4. Gerar `docs/design/TDD-{projeto}-{módulo}.md`
5. **AGUARDAR** aprovação humana
6. **EXECUTAR `/task-complete`** após aprovação

> [!IMPORTANT]
> **POST-TDD:** Débitos P0-P3 serão transformados em tasks na Phase 7A.
> **NÃO** criar tasks de melhorias aqui.

---

### Phase 5.5: DESIGN SYSTEM (Se projeto tem UI)

> Pulado se projeto é apenas API/Backend.

> **Skills:** `ui-ux-discovery` (processo completo) + `design-system-enforcement` (gates)

**Ações:** Seguir TODOS os 5 passos do skill `ui-ux-discovery`:

1. Extrair identidade visual atual
2. Executar `/ui-ux-pro-max`
3. Perguntas granulares por aspecto (cores, tipografia, layout, efeitos, logo)
4. Consolidar decisões (mantidos + modernizados)
5. Validar e aprovar (aguardar humano)
6. **EXECUTAR `/task-complete`** após aprovação

### 🛑 GATE: Phase 5.5 → Phase 6 (Se projeto tem UI)

> **Skill:** `design-system-enforcement` (Pre-Delivery Checklist)

```
[ ] /ui-ux-pro-max executado?
[ ] Design System documentado?
[ ] Pre-Delivery Checklist verificado?
[ ] ui-validation script PASSOU?
[ ] Design System aprovado?
```

---

### Phase 6: TESTES INCREMENTAIS

**Objetivo:** Adicionar testes ao código legado de forma incremental.

**Estratégia:**

| Fase | Tipo        | Foco              | Cobertura Alvo |
| ---- | ----------- | ----------------- | -------------- |
| 1    | Integration | Fluxos críticos   | 60%            |
| 2    | Unit        | Funções complexas | 70%            |
| 3    | E2E         | Happy paths       | 80%            |
| 4    | Edge cases  | Bugs conhecidos   | 85%+           |

**Ações:** Identificar → Priorizar → Gerar testes (`/test [componente]`) → Verificar cobertura
**TASK SYNC:** `/task-complete` ao concluir cada lote (skill `project-tracking-patterns` → seção 7)

---

### Phase 7A: BREAKDOWN DE MELHORIAS (Planejamento)

**Objetivo:** Transformar débitos técnicos do TDD em tasks priorizadas.

> **Skill:** `project-tracking-patterns` para sync e gates.

#### Passo 1: Gerar Breakdown

1. Ler "Débitos Técnicos" do TDD
2. Executar `/tdd breakdown docs/design/TDD-{projeto}-{módulo}.md`
3. Criar tasks P0-P3

#### Passo 1.5: Cross-Scope Impact Analysis (OBRIGATÓRIO)

> [!CAUTION]
> Analisar outros módulos ANTES de finalizar breakdown.

1. Ler handover/TDD de TODOS os módulos já processados
2. Classificar cada débito:

| Classificação | Ação |
|---------------|------|
| ✅ Já corrigido em outro escopo | REMOVER do breakdown |
| 🔗 Afeta código compartilhado | EXPANDIR escopo |
| 🔴 Depende de outro módulo | MARCAR como bloqueado |
| ✅ Independente | Manter |

3. Gerar relatório de impacto cross-scope

#### Passo 2.7: Aprovação do Breakdown (GATE OBRIGATÓRIO)

> [!CAUTION]
> O agente NÃO PODE criar tasks sem aprovação explícita do usuário.

Apresentar lista completa + Cross-Scope Impact → AGUARDAR aprovação.

#### Passo 3-4: Criar Tasks + Popular Corpos

- **Flyee:** Seguir operação atômica (post-page → patch-block-children)
- **Local:** Adicionar ao `BREAKDOWN-{escopo}.md`

### 🛑 GATE: Phase 7A → Phase 7B

```
[ ] Todos os débitos P0-P3 têm task no Tracker?
[ ] Cada task tem corpo preenchido?
[ ] Usuário aprovou breakdown e prioridades?
[ ] Escopo de execução definido (ex: apenas P0)?
```

---

### Phase 7B: EXECUÇÃO DE MELHORIAS (Implementação)

**Objetivo:** Implementar melhorias aprovadas no breakdown.

> **Skills:**
> - `context-gathering-patterns` → Context Gathering por task
> - `project-tracking-patterns` → TASK SYNC e `/task-complete`
> - `local-verification` → Verificação local

> [!IMPORTANT]
> Executar apenas tasks aprovadas no gate (tipicamente P0s).

#### 🔄 Context Loss Resilience

**Ao INICIAR cada task:**

1. Marcar `[/]` no checklist Phase 7B do LEGACY-PROGRESS.md
2. Adicionar seção `🔧 TASK ATIVA` com: Task, Passo, Status, Início, Workflow
3. Atualizar campo `Passo` conforme avança

**Ao CONCLUIR cada task:**

1. Remover seção `🔧 TASK ATIVA`
2. Marcar `[x]` no checklist
3. Re-ler LEGACY-PROGRESS.md para próxima task pendente

#### Processo: Para CADA Task Aprovada

**Passo 0: Context Gathering** (GATE POR TASK)

> **Skill:** `context-gathering-patterns`

- Ler corpo da task (Flyee ou BREAKDOWN)
- Ler referências (TDD, docs de fluxo relevantes)
- Preencher checklist de evidência (decisões, tipos, restrições)

**Passo 0.5: Cross-Module Impact Check**

> [!CAUTION]
> Se task modifica contratos compartilhados (enums, interfaces, APIs, configs),
> verificar compatibilidade em todos os módulos consumidores.

```
🔒 CROSS-MODULE IMPACT — Task #{id}
[ ] Contratos modificados identificados
[ ] Módulos consumidores mapeados
[ ] Compatibilidade verificada por módulo
[ ] Sub-tasks criados para módulos afetados (se necessário)
```

**Passos 1-4:** Atualizar Tracker → Implementar → Testar → Verificar

**Passo 4.5: Doc Impact Check**

> **Skill:** `code-truth-validation` → seção "4. Doc Impact Check"

**Passo 5:** `/task-complete` (skill `project-tracking-patterns` → seção 7)

#### 🔁 Loop Continuation

Após `/task-complete`: remover TASK ATIVA → re-ler progresso → próxima task ou Gate 7B→8.

---

### Gate 7B → 8: DOC FRESHNESS GATE

> **Skill:** `code-truth-validation` → seção "5. Doc Freshness Gate"

Re-validar TODOS os docs contra código atual antes de publicar.

---

### Phase 8: HANDOVER + PUBLICAÇÃO DE DOCUMENTAÇÃO TÉCNICA

> **Skill:** `documentation-publishing` → seções 1 e 2

> [!CAUTION]
> **DUAS partes obrigatórias:** (1) Criar HANDOVER + TEST-GUIDE, (2) Publicar docs.
> Uma sem a outra = fase INCOMPLETA.

**Ações:**

1. Criar `docs/handover/{escopo}/HANDOVER-{escopo}.md` (skill → template)
2. Criar `docs/tests/{escopo}/TEST-GUIDE-{escopo}.md` (skill → template)
3. **Se Flyee:** Publicar TODOS os artefatos (flow docs, TDD, DS, handover, test-guide)
4. **Se Local:** Registrar docs criados no LEGACY-PROGRESS.md
5. `/task-complete` para task de handover

---

### Phase 8.5: PUBLICAÇÃO DO MANUAL DO USUÁRIO

> **Skill:** `documentation-publishing` → seção 3

> [!CAUTION]
> Para cada fluxo publicado, DEVE existir versão em linguagem acessível.

**Ações:**

1. **Se Flyee:** Discovery database "Manual do Usuário" → mapear fluxos → publicar guias
2. **Se Local:** Gerar guias em `docs/user-guides/{escopo}/` → registrar no LEGACY-PROGRESS.md

---

### Phase 9: PRÓXIMO ESCOPO (GATE BLOQUEANTE)

> [!CAUTION]
> O workflow NÃO está concluído enquanto houver escopos `⏳ Pendente`.

**Ações:**

1. Ler LEGACY-PROGRESS.md → "Mapeamento de Escopos"
2. Se há pendentes → apresentar ao usuário (continuar agora / pausar com `--resume`)
3. Se todos concluídos → relatório final

> [!CAUTION]
> **Ao propor próximo escopo**, a ordem obrigatória é:
> Análise → **Criar tasks no Tracker** → Documentação → TDD → Testes → Melhorias → Publicação.
> Plano sem task creation antes de documentação = **INVÁLIDO**.

---

## 📁 Estrutura de Arquivos Gerados

```
projeto/
├── docs/
│   ├── LEGACY-PROGRESS.md              # ⭐ Controle (checklists + refs)
│   ├── CODEBASE-{projeto}.md           # Visão geral
│   ├── analysis/
│   │   └── {escopo}/
│   │       └── BREAKDOWN-{escopo}.md   # ⭐ Tasks locais (se modo Local)
│   ├── flows/
│   │   └── {módulo}/                   # Docs por fluxo
│   ├── design/
│   │   └── TDD-{projeto}-{módulo}.md   # TDD por módulo
│   ├── handover/
│   │   └── {escopo}/HANDOVER-{escopo}.md
│   ├── tests/
│   │   └── {escopo}/TEST-GUIDE-{escopo}.md
│   └── user-guides/
│       └── {escopo}/                   # Guias (modo Local)
```

---

## 📋 Template: LEGACY-PROGRESS.md

````markdown
# Legacy Project Progress - {projeto}

> Arquivo de controle para retomar workflow de onde parou.
> ⚠️ NÃO EDITAR MANUALMENTE - Atualizado automaticamente.

## 📊 Status Geral

| Campo              | Valor           |
| ------------------ | --------------- |
| Projeto            | {nome}          |
| Path               | {caminho}       |
| Iniciado em        | {data}          |
| Última atualização | {data}          |
| Status             | 🟡 Em Progresso |
| Fase Atual         | {fase}/8        |
| Escopo Atual       | {módulo}        |

---

## ⚙️ Configurações

| Campo              | Valor            |
| ------------------ | ---------------- |
| Destino de Tasks   | {Flyee / Local}  |
| Idioma             | {idioma}         |

---

## 🗺️ Mapeamento de Escopos

| Escopo        | Criticidade | Status          | Fase | Última Ação   |
| ------------- | ----------- | --------------- | ---- | ------------- |
| `src/auth`    | 🔴 Alta     | ✅ Completo     | 8/8  | Tasks criadas |
| `src/payment` | 🔴 Alta     | 🟡 Em Progresso | 5/8  | TDD Reverso   |
| `src/users`   | 🟡 Média    | ⏳ Pendente     | -    | -             |

---

## 📝 Escopo Atual: `{módulo}`

### Phase 3.5: Task Setup ✅
### Phase 4: Documentação 🟡
- [x] `docs/flows/{módulo}/fluxo-1.md`
- [ ] `docs/flows/{módulo}/fluxo-2.md`
### Phase 5: TDD Reverso ⏳
### Phase 5.5: Design System ⏳
### Phase 6: Testes ⏳
### Phase 7A: Breakdown ⏳
### Phase 7B: Execução ⏳
### Phase 8: Handover + Publicação ⏳
### Phase 8.5: Manual do Usuário ⏳
### Phase 9: Próximo Escopo ⏳

---

## 📜 Histórico de Ações

| Data             | Fase | Ação                        |
| ---------------- | ---- | --------------------------- |
| 2025-01-15 10:30 | 1    | Overview concluído          |

---

## 🔄 Para Retomar

```bash
/legacy-project --resume
```
````

---

## 🔴 REGRAS CRÍTICAS

1. **Sempre salvar checkpoint** após cada fase
2. **Um módulo por vez** — não paralelizar análise
3. **Aprovação humana** no TDD Reverso
4. **Priorizar críticos** — auth e payment primeiro
5. **Testes antes de refactoring**
6. **Incremental** — não tentar analisar tudo de uma vez
7. **🔄 TASK TRACKING OBRIGATÓRIO** — Toda atividade pós-análise (Phase 4+) DEVE ter task registrada. Seguir skill `project-tracking-patterns` → seção 7 para `/task-complete`
8. **🔀 PHASE 7A ≠ 7B** — 7A (Breakdown) planeja, 7B (Execução) implementa. NUNCA misturar. Gate obrigatório
9. **📚 HANDOVER + DOCS** — Phase 8 + 8.5: seguir skill `documentation-publishing`. AMBAS as partes obrigatórias
10. **🛡️ ESCOPOS PENDENTES = INCOMPLETO** — Workflow não encerra com escopos `⏳ Pendente`
11. **📋 SEQUÊNCIA OBRIGATÓRIA** — Phase 4→5→5.5→6→7A→7B→8→8.5→9. Consultar LEGACY-PROGRESS.md para próxima fase
12. **📊 PROGRESS SYNC** — Ao concluir fase: checklist ✅, fase incrementada, histórico atualizado
13. **📄 DOC REFRESH** — Após Phase 7B, re-validar docs via skill `code-truth-validation` → "Doc Freshness Gate"

---

## 📋 Comparativo de Modos

| Aspecto                | Completo      | --scope          | --quick      | --critical-first |
| ---------------------- | ------------- | ---------------- | ------------ | ---------------- |
| Overview               | ✅            | ❌               | ✅           | ✅               |
| Seleção interativa     | ✅            | ❌ (usa scope)   | ❌           | ❌ (auto)        |
| Documentação detalhada | ✅            | ✅               | ❌           | ✅               |
| TDD Reverso            | ✅            | ✅               | ✅ (simples) | ✅               |
| Checkpointing          | ✅            | ✅               | ✅           | ✅               |
| Múltiplos escopos      | ✅            | ❌ (1 por vez)   | ❌           | ✅               |
| Recomendado para       | Projeto médio | Debug específico | MVP rápido   | Projeto grande   |

---

## Usage Examples

```bash
# Análise completa com seleção interativa de escopo
/legacy-project /projetos/meu-app-grande

# Analisar apenas um módulo específico
/legacy-project --scope src/auth /projetos/monorepo

# Priorizar fluxos críticos automaticamente
/legacy-project --critical-first /projetos/app

# Retomar de onde parou
/legacy-project --resume

# Ver status detalhado
/legacy-project status

# Com sincronização Flyee
/legacy-project --flyee /projetos/app

# Forçar re-análise
/legacy-project --scope src/auth --force /projetos/app
```
