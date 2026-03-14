---
description: Workflow unificado para projeto legado. Análise → Documentação → TDD Reverso → Design System → Melhorias. Engenharia reversa e modernização. Suporta projetos grandes com checkpointing.
skills: checkpointing-patterns, history-check-patterns, project-tracking-patterns, ui-ux-discovery, local-verification, content-strategy, design-system-enforcement
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
| `--flyee`         | Sincronizar progresso com Flyee| `--flyee`         |
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

### Arquivo de Controle: `docs/LEGACY-PROGRESS.md`

Este arquivo é **criado automaticamente** e contém:

| Seção                 | Conteúdo                                      |
| --------------------- | --------------------------------------------- |
| Status Geral          | Projeto, path, fase atual, última atualização |
| Mapeamento de Escopos | Lista de todos os módulos e seu status        |
| Escopo Atual          | Checklist detalhado da fase em andamento      |
| Histórico             | Log de ações realizadas                       |

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
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐
│   OVERVIEW   │───▶│   ESCOPO     │───▶│CROSS-SCOPE   │───▶│   ANÁLISE    │───▶│ FLYEE SETUP │───▶│ DOCUMENTAÇÃO │───▶│  TDD REVERSO │───▶│   TESTES     │───▶│  BREAKDOWN   │───▶│  EXECUÇÃO    │───▶│ HANDOVER + PUBLICAÇÃO │
│  (Mapear)    │    │  (Escolher)  │    │  CONTEXT     │    │  (Detalhar)  │    │ + BREAKDOWN  │    │  (Fluxos)    │    │  (Técnico)   │    │  (Cobrir)    │    │ 7A (Planejar)│    │ 7B (Executar)│    │     (Flyee)          │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────────────┘
       ✅                  ✋                 🔗                   ✅                  ✅                 ✅ 🔄                ✋ 🔄               ✅ 🔄                ✋ Gate              ✅ 🔄                📚 Handover+Docs→Cliente
```

> 🔗 = Carrega contexto de escopos concluídos (handover, TDD, flows, débitos)
> 🔄 = TASK SYNC obrigatório ao final da fase (Flyee: ver Flyee API → "PHASE TASK TRACKING" / Local: atualizar `LEGACY-PROGRESS.md`)
> 📚 = Handover (HANDOVER.md + TEST-GUIDE.md) + Publicação de documentação (Flyee: databases "Documentação Técnica" e "Manual do Usuário" / Local: `docs/` + registro no LEGACY-PROGRESS.md)

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

#### Passo 0.5: Auto-Anchor de Tasks Órfãs (OBRIGATÓRIO no --resume — APENAS MODO FLYEE)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Ao retomar (`--resume`), ANTES de continuar qualquer fase,
> executar verificação de tasks órfãs no Flyee. Tasks criadas em conversas paralelas
> podem existir sem estarem rastreadas no `LEGACY-PROGRESS.md`.

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Pular Passos 0.5 e 0.55 inteiramente.
> Tasks locais não podem ficar órfãs porque existem apenas no `LEGACY-PROGRESS.md`.

**0.5.1 - Consultar todas as tasks existentes no database "Tarefas":**

Usar `post-search` paginado para obter todas as pages do database.

**0.5.2 - Comparar com seção "📋 Registro de Tasks Flyee" do `LEGACY-PROGRESS.md`:**

Extrair IDs de todas as linhas da tabela. Identificar IDs presentes no Flyee mas
**ausentes** no registro local.

**0.5.3 - Para cada task órfã detectada, auto-classificar e ancorar:**

| Categoria / Épico da task | Fase destino | Onde ancorar no checklist              |
| ------------------------- | ------------ | -------------------------------------- |
| Documentação              | Phase 4 ou 8 | Checklist da fase correspondente       |
| Refatoração / Melhoria    | Phase 7B     | Adicionar como item `[ ]` no checklist |
| Testes                    | Phase 6      | Checklist de testes                    |
| Outra                     | Phase 8      | Fallback: Próximo Escopo               |

**0.5.4 - Verificar duplicatas:**

Se a task órfã tem escopo **idêntico** a uma task já rastreada:

1. Fechar a task duplicada no Tracker (Status: "Concluído", comentário explicando)
2. Marcar no registro como `❌ Duplicata (#XX)`

**0.5.5 - Atualizar `LEGACY-PROGRESS.md`:**

1. Adicionar tasks órfãs ao "📋 Registro de Tasks Flyee" com a fase correta
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

#### Passo 0.55: Retroactive Task-Complete Gate (OBRIGATÓRIO no --resume — APENAS MODO FLYEE)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Ao retomar (`--resume`), APÓS o auto-anchor (0.5), verificar
> se tasks marcadas como "✅ Concluído" no `LEGACY-PROGRESS.md` foram **completamente**
> sincronizadas no Flyee. Sessões anteriores podem ter feito sync parcial.

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Este passo é pulado (já pulado junto com 0.5).
> Tasks locais são atualizadas diretamente no `LEGACY-PROGRESS.md` e não podem ficar dessincronizadas.
>
> 🔴 **FALHA QUE GEROU ESTA REGRA (v3):** Tasks #1-#3 marcadas Concluído no LEGACY-PROGRESS
> mas no Flyee: Status = "Não iniciado", sem comentário, sem nota inline. O --resume fez
> apenas `API-patch-page` (Status + %) mas NÃO adicionou comentário nem nota inline.
>
> 🔴 **FALHA v4 (admin/ --resume):** Mesmo com esta regra v3 escrita, o agente da sessão
> seguinte detectou tasks #48-#55 com sync incompleto e fez **chamadas diretas a
> `API-patch-page`** (Status + % + Tempo Gasto) SEM: comentário, nota inline, atualização
> do LEGACY-PROGRESS.md. **Causa raiz:** a instrução "Executar `/task-complete`" era textual
> — o agente não leu `task-complete.md` e substituiu o workflow por chamadas avulsas.

**0.55.1 - Para cada task com "✅ Concluído" no LEGACY-PROGRESS.md:**

1. Consultar a task no Tracker (`retrieve-a-comment` + `retrieve-a-page`)
2. Verificar 3 itens:
   - Status no Tracker = "Concluído"?
   - Existe pelo menos 1 comentário?
   - Existe nota de conclusão no corpo (callout ✅)?

**0.55.2 - Se QUALQUER item estiver faltando:**

```
⚠️ **SYNC INCOMPLETO DETECTADO — Task #{id}: {título}**

| Check       | Status |
|-------------|--------|
| Flyee Status = Concluído | ✅/❌ |
| Comentário de conclusão   | ✅/❌ |
| Nota inline no corpo      | ✅/❌ |

→ Executando `/task-complete` retroativamente...
```

> [!CAUTION]
> 🚫 **ANTI-PATTERN (PROIBIDO):**
> ```
> Flyee API: update_task()  ← PROIBIDO ISOLADAMENTE
> ```
> Chamadas avulsas a `API-patch-page` SEM as etapas 2.5 e 3 do `/task-complete`
> são a causa raiz das falhas v1, v2, v3 e v4. NUNCA fazer isso.
>
> ✅ **PADRÃO CORRETO (OBRIGATÓRIO):**
> 1. Ler `task-complete.md` via `view_file` (se não lido na sessão)
> 2. Executar as **5 etapas** do `/task-complete` na ordem:
>    - Etapa 1: Log de Execução
>    - Etapa 1.5: Resumo de Execução (O que foi feito, Arquivos, Verificação)
>    - Etapa 2: `API-patch-page` (Status + % + Tempo)
>    - Etapa 2.5: `API-patch-block-children` (nota inline ✅)
>    - Etapa 3: `API-create-a-comment` (comentário rico)
>    - Etapa 4: Atualizar LEGACY-PROGRESS.md
> 3. Exibir mensagem de confirmação

**Para cada task com sync incompleto**, executar `/task-complete {id} "{tempo}"` **seguindo
obrigatoriamente as 5 etapas descritas em `.agent/workflows/task-complete.md`**.

> [!WARNING]
> **É PROIBIDO** fazer sync parcial (ex: só `API-patch-page` sem comentário).
> O workflow `/task-complete` DEVE ser executado integralmente.

**0.55.2.1 - Checklist pós-sync (BLOQUEIA prosseguimento):**

Após executar `/task-complete` para TODAS as tasks com sync incompleto:

```
✅ CHECKLIST PÓS-SYNC RETROATIVO

| Task | patch-page | nota inline | comentário | LEGACY-PROGRESS |
|------|-----------|-------------|------------|-----------------|
| #{id} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |

→ Se QUALQUER ❌ → PARAR e completar ANTES de prosseguir
→ Se TODOS ✅ → Prosseguir para próxima fase
```

**0.55.3 - Se TODAS as tasks concluídas estão com sync completo:**

Prosseguir silenciosamente.

**Checkpoint salvo:** Sync retroativo concluído

#### Passo 0.6: Context Re-Check (OBRIGATÓRIO se retomando Phase 7B)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Se a fase atual é 7B, o agente DEVE verificar se o
> Context Gathering foi completado para a task em andamento ANTES de retomar
> a implementação. Truncamento de conversa ou checkpoint pode ter apagado
> o contexto lido anteriormente.

**0.6.1 - Detectar Task Ativa (PRIORIDADE MÁXIMA):**

Buscar seção `🔧 TASK ATIVA` no `LEGACY-PROGRESS.md`.

- **Se existe** → Task foi interrompida por perda de contexto. O agente DEVE:
  1. Ler o workflow `/legacy-project` (Phase 7B) para restaurar o loop
  2. Verificar em qual Passo a task parou (registrado na tabela da seção)
  3. Se Passo < 5 → CONTINUAR a implementação a partir do passo registrado
  4. Se Passo = 5 (task-complete) → Executar `/task-complete` retroativamente
  5. Informar ao usuário:

  ```
  🔄 **RETOMADA DE TASK INTERROMPIDA**

  Task #{id}: {título}
  Último passo registrado: {passo}
  Ação: {retomando implementação / executando task-complete retroativo}
  ```

- **Se NÃO existe** → Seguir fluxo normal (0.6.2 e 0.6.3)

**0.6.2 - Identificar task em andamento:**

Ler `LEGACY-PROGRESS.md` → encontrar task com status `[/]` (em progresso) na Phase 7B.

**0.6.3 - Verificar checklist de Context Gathering:**

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

| Módulo         | Criticidade | Arquivos | Status      |
| -------------- | ----------- | -------- | ----------- |
| `src/auth`     | 🔴 Alta     | 23       | ⏳ Pendente |
| `src/payment`  | 🔴 Alta     | 45       | ⏳ Pendente |
| `src/users`    | 🟡 Média    | 18       | ⏳ Pendente |
| `src/products` | 🟢 Normal   | 67       | ⏳ Pendente |

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

### Phase 2.5: CROSS-SCOPE CONTEXT (se há escopos anteriores concluídos)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Se existem escopos já concluídos (verificar `LEGACY-PROGRESS.md`),
> esta fase DEVE ser executada ANTES da análise detalhada. O novo escopo precisa
> estar **ciente** do estado atual do projeto para evitar retrabalho e inconsistências.

**Objetivo:** Carregar contexto dos escopos anteriores para informar a análise do novo escopo.

**Trigger:**

```
Escopo selecionado + existem escopos com status ✅ no LEGACY-PROGRESS.md
```

> Se é o **primeiro** escopo analisado (nenhum `✅`), **pular para Phase 3** diretamente.

**Ações:**

#### Passo 1: Identificar escopos concluídos

Ler `docs/LEGACY-PROGRESS.md` → seção "Mapeamento de Escopos". Listar todos com status `✅`.

#### Passo 2: Carregar documentação dos escopos anteriores

Para cada escopo concluído `{escopo}`, ler na seguinte ordem de prioridade:

| #   | Documento  | Caminho                                       | O que extrair                                |
| --- | ---------- | --------------------------------------------- | -------------------------------------------- |
| 1   | Handover   | `docs/handover/{escopo}/HANDOVER-{escopo}.md` | Arquitetura, decisões, issues conhecidas     |
| 2   | TDD        | `docs/design/TDD-*-{escopo}.md`               | Componentes, contratos API, débitos técnicos |
| 3   | Flow docs  | `docs/flows/{escopo}/**/*.md`                 | Endpoints consumidos, dependências cruzadas  |
| 4   | Test guide | `docs/tests/{escopo}/TEST-GUIDE.md`           | Cobertura, gaps de teste                     |

> [!TIP]
> Nem todos os documentos existirão para cada escopo. Ler apenas os que existem.

#### Passo 3: Construir mapa de dependências cruzadas

Identificar especificamente:

1. **Endpoints/APIs** que o escopo anterior consome do novo escopo (ou vice-versa)
2. **Models/Entities** compartilhadas entre escopos
3. **Melhorias feitas** que impactam o novo escopo (ex: refatorações, bug fixes)
4. **Débitos técnicos** registrados que se referem ao novo escopo

```markdown
📋 **CROSS-SCOPE CONTEXT — {novo_escopo}**

### De {escopo_anterior}:

- **Endpoints consumidos:** {lista de endpoints do novo escopo usados pelo anterior}
- **Models compartilhadas:** {entidades que aparecem em ambos}
- **Melhorias relevantes:** {refatorações/fixes que afetam o novo escopo}
- **Débitos apontados:** {débitos técnicos que mencionam o novo escopo}
- **Issues conhecidas:** {problemas documentados no handover}
```

#### Passo 3.5: Validar doc-vs-code dos escopos anteriores

> [!WARNING]
> Documentação de escopos anteriores pode conter **afirmações desatualizadas ou incorretas**
> (ex: flow doc do `shop/` dizendo "gateway = Pagar.me" quando o código real tem `Cielo.php`).
> Divergências detectadas aqui DEVEM ser corrigidas ou registradas como errata.

Para cada **integração, gateway ou componente cross-scope** identificado no Passo 3:

1. Verificar se o arquivo/classe referenciado **existe** no codebase do novo escopo
2. Se o doc anterior diz "ativo/implementado" → confirmar no código (não é stub?)
3. Se o doc anterior diz "planejado" → verificar se foi implementado desde então
4. Registrar divergências encontradas no formato:

```markdown
### ⚠️ Divergências Doc → Código

| Doc Fonte    | Afirmação         | Realidade no Código  | Ação                            |
| ------------ | ----------------- | -------------------- | ------------------------------- |
| {arquivo.md} | {o que o doc diz} | {o que o código tem} | Corrigir doc / Registrar débito |
```

#### Passo 4: Registrar contexto no LEGACY-PROGRESS.md

Adicionar seção `📖 CROSS-SCOPE CONTEXT — {novo_escopo}` no `LEGACY-PROGRESS.md`
com o mapa construído no Passo 3 + divergências do Passo 3.5. Este contexto DEVE ser referenciado durante Phase 3.

**Gate de Saída:**

```
[ ] Escopos anteriores concluídos identificados
[ ] Documentação dos escopos lida (handover, TDD, flows)
[ ] Mapa de dependências cruzadas construído
[ ] Divergências doc-vs-code verificadas e registradas
[ ] Contexto registrado em LEGACY-PROGRESS.md
```

**Checkpoint salvo:** Contexto cross-scope carregado

---

### Phase 3: ANÁLISE DETALHADA DO ESCOPO

**Objetivo:** Analisar profundamente o módulo selecionado.

**Trigger:**

```
Phase 2.5 concluída (ou Phase 2 se primeiro escopo)
```

> [!IMPORTANT]
> Se Phase 2.5 foi executada, a análise DEVE levar em conta o contexto cross-scope
> carregado. Especificamente: validar endpoints documentados pelo escopo anterior,
> verificar se melhorias anteriores impactam a estrutura atual, e cruzar débitos técnicos.

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

### Phase 3.5: TASK SETUP + BREAKDOWN DE FASES

> [!CAUTION]
> **REGRA BLOQUEANTE:** Esta fase DEVE ser executada ANTES de iniciar qualquer trabalho
> nas fases 4-7. Toda atividade pós-análise precisa de tasks registradas para
> **acompanhamento e transparência**.

**Objetivo:** Definir destino das tasks (Flyee ou Local) e criar tasks antecipadas para todas as fases seguintes.

**Trigger:**

```
Phase 3 concluída → Automático
```

**Agentes Envolvidos:**

- `orchestrator` - Integração Tracker (se modo Flyee)

> [!IMPORTANT]
> **SKILL:** Se modo Flyee, seguir Flyee API → seção "PHASE TASK TRACKING" OBRIGATORIAMENTE.

#### Passo 0: Escolha de Destino das Tasks (GATE OBRIGATÓRIO)

> [!IMPORTANT]
> **Antes de configurar Flyee ou criar tasks**, o agente DEVE perguntar ao usuário
> onde as tasks serão registradas. Esta escolha será **persistida** no `LEGACY-PROGRESS.md`
> e aplicada em TODAS as phases subsequentes (4-8).

**Perguntar ao usuário:**

```
📋 **DESTINO DAS TASKS**

As tasks de acompanhamento podem ser registradas em:

1. **Flyee** — Tasks criadas no database "Tarefas" do Flyee
   (recomendado para transparência com cliente)
2. **Local** — Tasks registradas apenas no `LEGACY-PROGRESS.md`
   com estrutura equivalente (sem integração Flyee)

Onde deseja registrar as tasks?
```

**Salvar escolha em `LEGACY-PROGRESS.md` → seção "⚙️ Configurações":**

```markdown
## ⚙️ Configurações

| Campo              | Valor            |
| ------------------ | ---------------- |
| Destino de Tasks   | Flyee / Local   |
| Idioma             | {idioma}         |
```

**Se "Local":**
- Pular Passos 1, 2, 2.5 (Discovery/Validação/ID Check do Flyee)
- No Passo 3, criar arquivo `docs/analysis/{escopo}/BREAKDOWN-{escopo}.md` com tasks locais
- O `LEGACY-PROGRESS.md` mantém apenas **referência** ao BREAKDOWN + checklist de IDs (`[ ] T-01`)
- Todos os TRACKER SYNC de phases posteriores são convertidos para LOCAL SYNC
  (atualizar task no `BREAKDOWN-{escopo}.md` + checklist no `LEGACY-PROGRESS.md`)
- `/task-complete` em modo local executa apenas os passos de atualização do
  `BREAKDOWN-{escopo}.md` e `LEGACY-PROGRESS.md` (sem API calls Flyee)

**Se "Flyee":**
- Fluxo atual sem alterações (Passos 1-4 normais)
- Prosseguir para Passo 1

#### Passo 1: Discovery e Validação do Database (APENAS MODO FLYEE)

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Pular diretamente para Passo 3.

> Seguir Flyee API → seção "VALIDAÇÃO DE SCHEMA"

```json
// Tool: Flyee API: list_tasks()
{
  "query": "Tarefas",
  "filter": { "property": "object", "value": "data_source" }
}
```

```json
// Tool: Flyee API: list_tasks()
{ "database_id": "{DATABASE_ID}" }
```

> Se propriedades ausentes → PARAR e notificar usuário (ver skill para mensagem).

#### Passo 2: Perguntar Idioma (se não definido)

> Seguir Flyee API → seção "IDIOMA DAS TASKS"

Salvar preferência em `docs/LEGACY-PROGRESS.md` → seção "Configurações".

#### Passo 2.5: ID Continuity Check (OBRIGATÓRIO — APENAS MODO FLYEE)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de criar QUALQUER task nova, o agente DEVE verificar
> quais tasks já existem no Flyee para evitar gaps de numeração no rastreamento.
> **Se `Destino de Tasks = Local`:** Pular para Passo 3.

**2.5.1 - Consultar todas as tasks existentes:**

```
Use: Flyee API: list_tasks()
query: ""
filter: { "property": "object", "value": "page" }
page_size: 100
```

> Se `has_more: true`, paginar com `start_cursor` até obter todas.

**2.5.2 - Construir mapa de IDs:**

Para cada resultado, extrair:

- `properties.ID.unique_id.number` → Task ID
- `properties.Nome da tarefa.title[0].plain_text` → Título
- `properties.Status.status.name` → Status

**2.5.3 - Comparar com LEGACY-PROGRESS.md:**

1. Ler seção "📋 Registro de Tasks Flyee" do `LEGACY-PROGRESS.md`
2. Identificar IDs presentes no Flyee mas **ausentes** no arquivo local
3. Se houver IDs não rastreados:

```
⚠️ **TASKS NÃO RASTREADAS DETECTADAS**

As seguintes tasks existem no Flyee mas NÃO estão em LEGACY-PROGRESS.md:

| # | Task | Status | Criado em |
|---|------|--------|----------|
| {id} | {título} | {status} | {data} |

→ Registrando automaticamente antes de criar novas tasks...
```

4. Adicionar tasks não rastreadas ao "📋 Registro de Tasks Flyee" no `LEGACY-PROGRESS.md`
5. Só então prosseguir para criação de novas tasks

> [!IMPORTANT]
> **Último ID registrado:** O agente DEVE anotar o maior ID existente (`max_id`).
> As novas tasks criadas terão IDs a partir de `max_id + 1`.
> Usar este valor ao documentar as tasks no LEGACY-PROGRESS.md.

#### Passo 3: Criar Tasks para Fases 4-7

Baseado nos fluxos identificados na Phase 3, criar tasks antecipadas.

Tasks a criar (exemplo para módulo `{módulo}`):

| #   | Task                                  | Categoria    | Épico                    | Template     |
| --- | ------------------------------------- | ------------ | ------------------------ | ------------ |
| 1   | Documentar fluxo: {fluxo 1}           | Documentação | {módulo} - Documentação  | Documentação |
| 2   | Documentar fluxo: {fluxo 2}           | Documentação | {módulo} - Documentação  | Documentação |
| ... | (1 task por fluxo identificado)       | ...          | ...                      | ...          |
| N   | TDD Reverso: {módulo}                 | Documentação | {módulo} - TDD           | Documentação |
| N+1 | Design System: extração (se UI)       | Melhoria     | {módulo} - Design System | Documentação |
| N+2 | Testes: Integration (fluxos críticos) | Melhoria     | {módulo} - Testes        | Documentação |
| N+3 | Testes: Unit (funções complexas)      | Melhoria     | {módulo} - Testes        | Documentação |
| N+4 | Testes: E2E (happy paths)             | Melhoria     | {módulo} - Testes        | Documentação |

> [!WARNING]
> **Tasks de melhorias/refatoração (Phase 7A)** são criadas DEPOIS, quando o TDD Reverso
> identificar os débitos técnicos. Não antecipar estas tasks aqui.

> [!CAUTION]
> **REGRA BLOQUEANTE — NOMENCLATURA:** Títulos de tasks SEM prefixos (`[DOC]`, `[TDD]`, `[TEST]`,
> `F1 —`, etc.). A Categoria já cumpre essa função.

##### Se `Destino de Tasks = Flyee`:

> Seguir Flyee API → seção "PHASE TASK TRACKING" → "Processo: Breakdown de Fases"

> [!CAUTION]
> **REGRA BLOQUEANTE — CORPO OBRIGATÓRIO:** Para CADA task, executar sequencialmente:
>
> 1. **ETAPA 1:** `API-post-page` (criar página com propriedades)
> 2. **ETAPA 2:** `API-patch-block-children` (adicionar corpo com template)
> 3. Só então prosseguir para a **próxima task**
>
> **Se ETAPA 2 falhar** (ex: erro de API), resolver o erro ANTES de criar próxima task.
> **NÃO** fazer batch de ETAPA 1 para todas as tasks. Isso GARANTE que nenhuma task fica sem corpo.

##### Se `Destino de Tasks = Local`:

Criar arquivo `docs/analysis/{escopo}/BREAKDOWN-{escopo}.md` seguindo o padrão estabelecido.

**Template do arquivo BREAKDOWN:**

```markdown
# Breakdown de Tasks — Módulo `{escopo}`

> Phase 3.5 do workflow `/legacy-project`
> Escopo: `{escopo}` | Data: {data}

---

## 📊 Resumo

| Prioridade | Qtd | Categoria |
|------------|-----|-----------|
| 🔴 P0 | {n} | {categorias} |
| 🟡 P1 | {n} | {categorias} |
| 🟢 P2 | {n} | {categorias} |
| Total | **{N}** | |

---

## 🔴 P0 — {Categoria}

### T-{seq}: {título}
- **Status:** [ ] Pendente
- **Criticidade:** 🔴 Alta
- **Esforço:** ~{X}h
- **Descrição:** {descrição detalhada}
- **Arquivos afetados:**
  - {lista de arquivos}
- **Acceptance Criteria:**
  - [ ] {critério 1}
  - [ ] {critério 2}

---

## 🟡 P1 — {Categoria}

### T-{seq}: {título}
...

---

## 📅 Ordem de Execução Sugerida

{Fases de execução agrupadas logicamente}
```

**Adicionalmente, registrar no `LEGACY-PROGRESS.md`:**

1. Referência ao arquivo: `→ BREAKDOWN: docs/analysis/{escopo}/BREAKDOWN-{escopo}.md`
2. Checklist resumido com apenas IDs:

```markdown
### Phase 3.5: Task Setup ✅

→ BREAKDOWN: `docs/analysis/{escopo}/BREAKDOWN-{escopo}.md`

- [ ] T-01: {título}
- [ ] T-02: {título}
- ...
```

> [!IMPORTANT]
> As tasks locais (`T-{seq}`) DEVEM manter a mesma estrutura informacional
> das tasks Flyee para permitir migração futura se o usuário mudar de decisão.
> O `LEGACY-PROGRESS.md` mantém apenas **referências e checklists**, nunca o corpo das tasks.

#### Passo 3.5: Verificação de Corpos (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Após criar todas as tasks, o agente DEVE verificar que
> **100% das tasks** possuem corpo preenchido. NÃO avançar para Passo 4 sem esta verificação.

##### Se `Destino de Tasks = Flyee`:

**Para cada task criada, executar:**

```json
// Tool: Flyee API: get_task()
{ "block_id": "{page_id}" }
```

**Se `results` estiver vazio → task SEM corpo → PARAR e completar ETAPA 2 antes de avançar.**

##### Se `Destino de Tasks = Local`:

Verificar no `docs/analysis/{escopo}/BREAKDOWN-{escopo}.md` que cada task `T-{seq}` possui
**Descrição**, **Arquivos afetados** e **Acceptance Criteria** preenchidos (não vazios).
Se alguma task estiver incompleta → PARAR e completar antes de avançar.

#### Passo 4: Relatório de Tasks Criadas

```markdown
📋 **BREAKDOWN DE FASES - {módulo}**

| #   | Task   | Categoria | Épico   | Estimativa | Destino |
| --- | ------ | --------- | ------- | ---------- | ------- |
| 1   | {nome} | {cat}     | {épico} | {Xh}       | {Flyee/Local} |
| ... | ...    | ...       | ...     | ...        | ...     |

Total: {N} tasks criadas
Estimativa total: {Xh}
Destino: {Flyee / Local}

✅ {Se Flyee: "Cliente pode acompanhar em: Flyee → Database 'Tarefas'"}
✅ {Se Local: "Tasks registradas em docs/analysis/{escopo}/BREAKDOWN-{escopo}.md"}
```

**Gate de Saída (Modo Flyee):**

```
[ ] Destino de Tasks definido e salvo em LEGACY-PROGRESS.md
[ ] Database "Tarefas" encontrado e validado
[ ] ID Continuity Check executado (sem gaps)
[ ] Idioma definido e salvo em LEGACY-PROGRESS.md
[ ] Tasks criadas para Phases 4-6 (1 por fluxo + TDD + DS + testes)
[ ] Títulos SEM prefixos ([DOC], [TDD], [TEST], etc.)
[ ] TODAS as tasks com corpo preenchido (verificado via get-block-children)
[ ] LEGACY-PROGRESS.md atualizado com lista de tasks + Registro de Tasks
```

**Gate de Saída (Modo Local):**

```
[ ] Destino de Tasks definido e salvo em LEGACY-PROGRESS.md
[ ] Idioma definido e salvo em LEGACY-PROGRESS.md
[ ] BREAKDOWN-{escopo}.md criado em docs/analysis/{escopo}/
[ ] Tasks registradas no BREAKDOWN (1 por fluxo + TDD + DS + testes)
[ ] Títulos SEM prefixos ([DOC], [TDD], [TEST], etc.)
[ ] TODAS as tasks com corpo preenchido (verificado no BREAKDOWN)
[ ] LEGACY-PROGRESS.md atualizado com referência ao BREAKDOWN + checklist de IDs
```

**Checkpoint salvo:** Tasks criadas ({Flyee / Local})

---

### Phase 4: DOCUMENTAÇÃO DOS FLUXOS

**Objetivo:** Documentar cada fluxo do módulo selecionado.

**Trigger:**

```
Phase 3.5 concluída → Automático
```

> [!CAUTION]
> **PRÉ-REQUISITO BLOQUEANTE:** Phase 3.5 (Flyee Setup + Breakdown) DEVE estar concluída
> antes de iniciar esta phase. Se as tasks NÃO foram criadas no Flyee, PARAR e executar
> Phase 3.5 primeiro. Verificar em `LEGACY-PROGRESS.md` → seção "📋 Registro de Tasks Flyee"
> que existem tasks para o escopo atual.

**Agentes Envolvidos:**

- `documentation-writer` - Geração de docs
- Especialistas de domínio

**Ações:**

> [!CAUTION]
> 🔴 **HISTÓRICO DE FALHAS QUE GERARAM AS REGRAS ABAIXO:**
>
> **FALHA v1 (api/):** 6 tasks (#27-#32) marcadas Concluído sem comentário, sem Tempo Gasto,
> sem nota de conclusão. O gate não estava listado na sequência de ações.
>
> **FALHA v2 (subscriptions/):** 3 tasks (#1, #2, #3) marcadas Concluído via `API-patch-page`
> (Status + % Progresso), mas SEM: comentário de conclusão, Tempo Gasto, nota inline no corpo,
> nem atualização de LEGACY-PROGRESS.md. **Causa raiz:** o gate era o passo 6 de 6 numa lista,
> e o agente focou na geração de docs e pulou o gate. A estrutura não forçava parada obrigatória.
>
> **FALHA v3 (subscriptions/ --resume):** Mesmo com o gate v2 escrito, o agente da sessão
> seguinte NÃO executou `/task-complete` para as tasks #1-#3 já concluídas. Quando o --resume
> detectou que as tasks estavam sem sync no Flyee, fez apenas `API-patch-page` (Status + %)
> mas NÃO adicionou comentário, nota inline, nem atualizou LEGACY-PROGRESS.md.
> **Causa raiz:** o gate era textual/descritivo — o agente não era forçado a invocar
> `/task-complete` como subroutine obrigatória.

#### 🔁 LOOP OBRIGATÓRIO: Para cada fluxo identificado

O loop abaixo tem **EXATAMENTE 2 etapas**. A Etapa B é **BLOQUEANTE** — o agente
NÃO PODE pular para o próximo fluxo sem completá-la.

**Etapa A — Gerar Documentação:**

1. Executar `/document [nome-do-fluxo]`
2. Gerar documentação estruturada
3. **CODE-TRUTH VALIDATION (OBRIGATÓRIO — ver regra abaixo)**
4. Salvar em `docs/flows/{módulo}/{fluxo}.md`

**Etapa B — 🛑 GATE OBRIGATÓRIO (NÃO PULAR):**

5. **EXECUTAR `/task-complete {task_id} "{tempo}"`** — workflow completo com TODAS as etapas

> [!CAUTION]
> 🔴 **REGRA BLOQUEANTE ABSOLUTA:** O agente DEVE executar o workflow `/task-complete`
> (arquivo `.agent/workflows/task-complete.md`) COMPLETO para a task correspondente ao fluxo.
> Este workflow executa automaticamente os 8 passos obrigatórios:
>
> 1. ✅ Log de Execução exibido
> 2. ✅ **Resumo de Execução produzido** (O que foi feito, Arquivos, Verificação, Decisões)
> 3. ✅ Flyee: Status → Concluído + % Progresso → 100 + Tempo Gasto (`API-patch-page`)
> 4. ✅ Flyee: Nota de conclusão inline no corpo (`API-patch-block-children`) — com dados do Resumo
> 5. ✅ Flyee: Comentário de conclusão (`API-create-a-comment`) — com dados do Resumo
> 6. ✅ LEGACY-PROGRESS.md: Status da task atualizado
> 7. ✅ LEGACY-PROGRESS.md: Histórico atualizado
> 8. ✅ Mensagem de confirmação exibida
>
> **É PROIBIDO substituir `/task-complete` por chamadas avulsas a `API-patch-page`.**
> Chamadas avulsas causam bypass dos itens 2, 4, 5, 6, 7 e 8.

#### 🧠 SELF-CHECK OBRIGATÓRIO (Anti-Bypass)

**ANTES de iniciar o próximo fluxo**, o agente DEVE responder mentalmente:

```
❓ SELF-CHECK — Fluxo anterior ({nome})

1. Executei `/task-complete` para a Task #{id}? → SIM/NÃO
2. O comentário de conclusão aparece no Flyee? → SIM/NÃO
3. LEGACY-PROGRESS.md foi atualizado? → SIM/NÃO

→ Se QUALQUER resposta = NÃO → PARAR e completar ANTES de prosseguir
→ Se TODAS = SIM → Prosseguir para próximo fluxo
```

> [!WARNING]
> **Se o agente detectar que um fluxo anterior foi concluído SEM `/task-complete`**
> (ex: durante `--resume`), DEVE executar `/task-complete` retroativamente ANTES
> de prosseguir. NÃO é aceitável fazer apenas `API-patch-page`.

**Checkpoint salvo:** Após cada fluxo documentado + gate completo

> [!TIP]
> Se o fluxo for interrompido, ao retomar ele continuará do próximo fluxo não documentado.

#### 🔒 REGRA: CODE-TRUTH VALIDATION (Phase 4)

> [!CAUTION]
> **ANTES de salvar qualquer flow doc**, o agente DEVE executar a validação abaixo.
> Esta regra existe porque documentação sem verificação contra o código real gera
> inconsistências graves (ex: documentar gateway X quando o código implementa gateway Y).

**Para cada afirmação técnica no documento gerado:**

1. **Integrações / Gateways / APIs externas:**
   - Verificar que o arquivo/classe mencionado **existe** no codebase (`find_by_name` / `grep_search`)
   - Verificar que está **registrado** no enum/config correspondente
   - Se o doc diz "ativo/implementado" → confirmar que o código NÃO é stub/mock/placeholder
   - Se o doc diz "será implementado" / "planejado" → marcar com `⏳ PLANEJADO` visível

2. **Componentes / Arquivos mencionados:**
   - Verificar que CADA arquivo referenciado existe no path indicado
   - Verificar que funções/métodos citados existem na assinatura real

3. **Enums / Constantes / Configs:**
   - Confirmar valores referenciados contra o fonte real (ex: `PaymentGatewayType.php`)

**Se a validação detectar divergência:**

- **NÃO** documentar o estado planejado como se fosse o estado atual
- Separar claramente em duas seções:

  ```markdown
  ## Estado Atual (verificado no código)

  [O que realmente existe — com referências a arquivos]

  ## Estado Planejado / Decisão de Projeto

  > ⏳ **Ainda não implementado no código**
  > [O que deveria existir — com justificativa e referência à decisão]
  ```

- Registrar a divergência como débito técnico na seção de débitos do doc

#### 🔄 TASK SYNC - Phase 4 (OBRIGATÓRIO)

> [!CAUTION]
> **Ao concluir CADA fluxo documentado**, executar sync da task correspondente.
> Se modo Flyee: seguir Flyee API → seção "PHASE TASK TRACKING" → "Gate: TRACKER SYNC".

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Substituir chamadas a APIs do Flyee por
> atualização direta no `BREAKDOWN-{escopo}.md` (Status da task) e `LEGACY-PROGRESS.md` (checklist).
> Na task do BREAKDOWN: marcar Status como `[x] Concluído`, preencher Esforço real.
> No `LEGACY-PROGRESS.md`: marcar `[x]` no checklist da fase.
> O `/task-complete` em modo local atualiza ambos os arquivos (sem API calls Flyee).

Para cada fluxo concluído:

1. Atualizar task → Status: "Concluído", `Tempo Gasto`, `% Progresso: 100`
2. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

```json
// Tool: Flyee API: update_task() (output)
{
  "block_id": "{page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    {
      "type": "callout",
      "callout": {
        "icon": { "type": "emoji", "emoji": "✅" },
        "rich_text": [
          { "type": "text", "text": { "content": "Concluído em {data}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": { "content": "📋 {resumo da implementação}" }
          }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          { "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "📁 Arquivos: {lista de arquivos modificados}"
            }
          }
        ]
      }
    }
  ]
}
```

3. Adicionar comentário rico de conclusão

**Ao concluir TODOS os fluxos:** 4. Verificar que TODAS as tasks de documentação estão synced (Gate de Conclusão) 5. Atualizar `LEGACY-PROGRESS.md`

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

   | Prioridade | Critério                       |
   | ---------- | ------------------------------ |
   | P0         | Segurança, bugs críticos       |
   | P1         | Performance, fluxos principais |
   | P2         | Refactoring, qualidade         |
   | P3         | Nice-to-have                   |

5. Gerar `docs/design/TDD-{projeto}-{módulo}.md`
6. **AGUARDAR** aprovação humana

#### 🔄 TASK SYNC - Phase 5 (OBRIGATÓRIO)

> [!CAUTION]
> **Após TDD aprovado**, executar sync.
> Se modo Flyee: seguir Flyee API → seção "PHASE TASK TRACKING" → "Gate: TRACKER SYNC".

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Atualizar task correspondente no
> `BREAKDOWN-{escopo}.md` (Status, Esforço real) e checklist no `LEGACY-PROGRESS.md`.
> Pular chamadas a APIs do Flyee.

1. Atualizar task "TDD Reverso: {módulo}" → Status: "Concluído", `Tempo Gasto`, `% Progresso: 100`
2. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

```json
// Tool: Flyee API: update_task() (output)
{
  "block_id": "{page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    {
      "type": "callout",
      "callout": {
        "icon": { "type": "emoji", "emoji": "✅" },
        "rich_text": [
          { "type": "text", "text": { "content": "Concluído em {data}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": { "content": "📋 {resumo da implementação}" }
          }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          { "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "📁 Arquivos: {lista de arquivos modificados}"
            }
          }
        ]
      }
    }
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

**Checkpoint salvo:** TDD gerado e synced no Flyee

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

| Passo | Ação                      | Detalhes                                              |
| ----- | ------------------------- | ----------------------------------------------------- |
| 1     | Extrair Identidade Atual  | Cores, fontes, elementos do legado                    |
| 2     | Executar `/ui-ux-pro-max` | Obter recomendações modernas                          |
| 3     | Perguntas Granulares ⭐   | Por aspecto: cores, tipografia, layout, efeitos, logo |
| 4     | Consolidar Decisões       | Combinar mantidos + modernizados                      |
| 5     | Validar e Aprovar         | Aguardar aprovação humana                             |

**Gate de Saída:**

```
[ ] Identidade visual atual extraída
[ ] /ui-ux-pro-max executado
[ ] Perguntas granulares respondidas pelo usuário
[ ] Design System consolidado com decisões híbridas
[ ] Pre-Delivery Checklist verificado
[ ] Design System aprovado pelo humano
```

#### 🔄 TASK SYNC - Phase 5.5 (OBRIGATÓRIO)

> [!CAUTION]
> **Após Design System aprovado**, executar sync.
> Se modo Flyee: seguir Flyee API → seção "PHASE TASK TRACKING" → "Gate: TRACKER SYNC".

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Atualizar task correspondente no
> `BREAKDOWN-{escopo}.md` (Status, Esforço real) e checklist no `LEGACY-PROGRESS.md`.
> Pular chamadas a APIs do Flyee.

1. Atualizar task "Design System: extração" → Status: "Concluído", `Tempo Gasto`, `% Progresso: 100`
2. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

```json
// Tool: Flyee API: update_task() (output)
{
  "block_id": "{page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    {
      "type": "callout",
      "callout": {
        "icon": { "type": "emoji", "emoji": "✅" },
        "rich_text": [
          { "type": "text", "text": { "content": "Concluído em {data}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": { "content": "📋 {resumo da implementação}" }
          }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          { "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "📁 Arquivos: {lista de arquivos modificados}"
            }
          }
        ]
      }
    }
  ]
}
```

3. Adicionar comentário rico de conclusão
4. Verificar Gate de Conclusão da fase

**Checkpoint salvo:** Design System definido e synced no Flyee

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

| Fase | Tipo        | Foco              | Cobertura Alvo |
| ---- | ----------- | ----------------- | -------------- |
| 1    | Integration | Fluxos críticos   | 60%            |
| 2    | Unit        | Funções complexas | 70%            |
| 3    | E2E         | Happy paths       | 80%            |
| 4    | Edge cases  | Bugs conhecidos   | 85%+           |

**Ações:**

1. Identificar código sem cobertura
2. Priorizar por criticidade
3. Gerar testes usando `/test [componente]`
4. Verificar cobertura incremental
5. **Atualizar checkpoint** após cada lote de testes

#### 🔄 TASK SYNC - Phase 6 (OBRIGATÓRIO)

> [!CAUTION]
> **Ao concluir CADA lote de testes** (Integration, Unit, E2E, Edge), executar sync.
> Se modo Flyee: seguir Flyee API → seção "PHASE TASK TRACKING" → "Gate: TRACKER SYNC".

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Atualizar task correspondente no
> `BREAKDOWN-{escopo}.md` (Status, Esforço real) e checklist no `LEGACY-PROGRESS.md`.
> Pular chamadas a APIs do Flyee.

Para cada lote concluído:

1. Atualizar task correspondente → Status: "Concluído", `Tempo Gasto`, `% Progresso: 100`
2. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

```json
// Tool: Flyee API: update_task() (output)
{
  "block_id": "{page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    {
      "type": "callout",
      "callout": {
        "icon": { "type": "emoji", "emoji": "✅" },
        "rich_text": [
          { "type": "text", "text": { "content": "Concluído em {data}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": { "content": "📋 {resumo da implementação}" }
          }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          { "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "📁 Arquivos: {lista de arquivos modificados}"
            }
          }
        ]
      }
    }
  ]
}
```

3. Adicionar comentário rico de conclusão

**Ao concluir TODOS os lotes:** 4. Verificar que TODAS as tasks de testes estão synced (Gate de Conclusão) 5. Atualizar `LEGACY-PROGRESS.md`

**Checkpoint salvo:** Cobertura atual registrada e synced no Flyee

---

### Phase 7A: BREAKDOWN DE MELHORIAS (Planejamento)

**Objetivo:** Transformar débitos técnicos do TDD em tasks priorizadas no Flyee.

**Trigger:**

```
Phase 6 concluída (ou parcialmente se cobertura aceitável)
```

**Agentes Envolvidos:**

- `project-planner` - Estruturação de tasks
- `orchestrator` - Integração Tracker

> [!IMPORTANT]
> **Transparência para Cliente:** Todas as melhorias identificadas devem ser
> registradas no Flyee para visibilidade do progresso.

#### Passo 1: Gerar Breakdown

1. Ler seção "Débitos Técnicos" do TDD (`docs/design/TDD-{projeto}-{módulo}.md`)
2. Executar `/tdd breakdown docs/design/TDD-{projeto}-{módulo}.md`
3. Criar tasks priorizadas:
   - P0: Segurança e bugs críticos
   - P1: Débitos técnicos de alto impacto
   - P2: Refactoring e qualidade
   - P3: Melhorias futuras

#### Passo 1.5: Cross-Scope Impact Analysis (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** O agente DEVE analisar os outros módulos do projeto
> ANTES de finalizar o breakdown. Pular esta etapa causa:
> - Tasks duplicadas (débito já corrigido em outro escopo)
> - Tasks impossíveis (sem endpoint backend correspondente)
> - Inconsistências (renomear arquivo compartilhado em só um módulo)

**1.5.1 - Ler Handover docs de TODOS os módulos já processados:**

```
Para cada módulo em docs/handover/:
  → Ler seção "Débitos Técnicos" → subseção "✅ Corrigidos"
  → Ler seção "Débitos Técnicos" → subseção "⏳ Pendentes"
```

**1.5.2 - Ler TDDs de TODOS os módulos:**

```
Para cada TDD em docs/design/TDD-*.md e docs/flows/*/tdd-*.md:
  → Ler seção de débitos técnicos
  → Cruzar com o breakdown atual
```

**1.5.3 - Para CADA débito no breakdown atual, classificar:**

| Classificação | Ação |
|---|---|
| ✅ Já corrigido em outro escopo | **REMOVER** do breakdown |
| 🔗 Afeta código compartilhado entre módulos | **EXPANDIR** escopo ou criar como task cross-module |
| 🔴 Depende de endpoint/feature de outro módulo que não existe | **MARCAR** como bloqueado + documentar dependência |
| ✅ Independente, sem impacto cross-scope | Manter no breakdown |

**1.5.4 - Gerar relatório de impacto (interno):**

O agente DEVE documentar internamente:

```markdown
## Cross-Scope Impact Report

### Removidos (já corrigidos)
- {ID}: {descrição} — corrigido em {módulo} task #{N}

### Expandidos (cross-module)
- {ID}: {descrição} — afeta também {módulo} → escopo expandido

### Bloqueados (dependência externa)
- {ID}: {descrição} — depende de {módulo} endpoint {X}

### Independentes
- {ID}: {descrição} — sem impacto cross-scope
```

> [!IMPORTANT]
> O relatório de impacto DEVE ser incluído na apresentação ao usuário (Passo 2.7).

#### Passo 2: Discovery e Validação (OBRIGATÓRIO)

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Pular Passos 2, 2.2, 2.5 (discovery/schema/ID check do Flyee).
> Ir diretamente para Passo 2.7 (Apresentação e Aprovação do Breakdown).
> Tasks serão adicionadas ao `BREAKDOWN-{escopo}.md` existente (ou novo arquivo criado).

##### Se `Destino de Tasks = Flyee`:

> [!CAUTION]
> **Seguir Flyee API OBRIGATORIAMENTE.**
> NÃO pular validação de schema.

**2.1 - Buscar Database "Tarefas":**

```
Use: Flyee API: list_tasks()
query: "Tarefas"
filter: { "property": "object", "value": "data_source" }
```

> **ATENÇÃO:** Buscar EXATAMENTE "Tarefas", não usar outro database.

**2.2 - Validar Schema (OBRIGATÓRIO):**

```
Use: Flyee API: list_tasks()
database_id: {DATABASE_ID}
```

Verificar propriedades obrigatórias:

> **Seguir Flyee API** → Seção "📋 PROPRIEDADES OBRIGATÓRIAS"

**Se QUALQUER propriedade estiver ausente:**

```
⚠️ **PROPRIEDADES AUSENTES** no database 'Tarefas':

| Propriedade | Tipo Esperado |
|-------------|---------------|
| {nome} | {tipo} |

**Por favor, crie estas propriedades no Flyee antes de continuar.**

🔗 [Abrir database no Tracker]({flyee_url})

**AGUARDANDO** confirmação após criar as propriedades...
```

> [!CAUTION]
> **NÃO prossiga** para o Passo 3 até que TODAS as propriedades existam.

**Se não encontrar database "Tarefas":**

```
⚠️ Database "Tarefas" não encontrado.

Para registrar as melhorias no Flyee:
1. Crie um database "Tarefas" com as propriedades obrigatórias
2. Execute: /legacy-project --resume

Ou prossiga sem Flyee (não recomendado para transparência).
```

#### Passo 2.5: ID Continuity Check (OBRIGATÓRIO — APENAS MODO FLYEE)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de criar QUALQUER task nova, verificar IDs existentes
> no Flyee para evitar gaps de numeração no `LEGACY-PROGRESS.md`.
> **Mesmo procedimento da Phase 3.5 — Passo 2.5.**
> **Se `Destino de Tasks = Local`:** Pular para Passo 2.7. IDs locais (`T-{seq}`) são
> sequenciais no `BREAKDOWN-{escopo}.md`.

**2.5.1 - Consultar todas as tasks existentes no database:**

Usar `post-search` com paginação para obter todas as pages do database.

**2.5.2 - Construir mapa de IDs existentes:**

Extrair `properties.ID.unique_id.number`, título e status de cada task.

**2.5.3 - Comparar com `LEGACY-PROGRESS.md` → seção "📋 Registro de Tasks Flyee":**

1. Identificar IDs presentes no Flyee mas **ausentes** no arquivo local
2. Se houver gaps → registrar tasks faltantes ANTES de criar novas
3. Anotar `max_id` para documentar corretamente os novos IDs

> [!IMPORTANT]
> **Último ID registrado:** Anotar o maior ID existente. Novas tasks terão IDs
> a partir de `max_id + 1`. Usar este valor ao documentar no LEGACY-PROGRESS.md.

#### Passo 2.7: Aprovação do Breakdown pelo Usuário (GATE OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** O agente NÃO PODE criar NENHUMA task no Tracker sem
> aprovação explícita do usuário. Criar tasks sem aprovação é **PROIBIDO**.

**2.7.1 - Apresentar lista completa ao usuário:**

O agente DEVE usar `notify_user` para apresentar:

```markdown
📋 **BREAKDOWN PROPOSTO — {projeto}/{módulo}**

## Tasks Propostas

| # | Task | Prioridade | Débitos Incluídos | Estimativa | Notas |
|---|------|------------|-------------------|------------|-------|
| 1 | {nome} | P0/Alta | ARCH-01, ARCH-03 | 3h | {cross-scope se houver} |
| 2 | {nome} | P1/Alta | ARCH-02, ARCH-06 | 3h | |
| ... | ... | ... | ... | ... | |

**Total:** {N} tasks, {Xh} estimativa

## Cross-Scope Impact
{relatório do Passo 1.5.4}

**Confirma a criação destas tasks no Tracker?**
**Quer ajustar agrupamento, remover/adicionar débitos, ou mudar prioridades?**
```

**2.7.2 - AGUARDAR resposta do usuário:**

- Se **aprovado** → Prosseguir para Passo 3
- Se **ajustes solicitados** → Refazer lista e re-submeter (volta para 2.7.1)
- Se **rejeitado** → Parar Phase 7A, documentar no LEGACY-PROGRESS.md

> [!WARNING]
> O agente NÃO PODE interpretar "prossiga" ou comandos anteriores como
> aprovação implícita do breakdown. A aprovação DEVE ser específica para
> a lista de tasks apresentada neste passo.

#### Passo 3: Criar Tasks

##### Se `Destino de Tasks = Flyee`:

Para **CADA melhoria** identificada:

> **Seguir Flyee API** → Seção "➕ Criar Task"

> [!CAUTION]
> **OBRIGATÓRIO:** `Estimativa` deve ser preenchido ao criar cada task.

##### Se `Destino de Tasks = Local`:

Para **CADA melhoria** identificada, adicionar ao `docs/analysis/{escopo}/BREAKDOWN-{escopo}.md`
usando o template de task local (mesmo da Phase 3.5). Preencher: ID (`T-{seq}`),
Status, Criticidade, Esforço, Descrição, Arquivos afetados, e Acceptance Criteria.
Atualizar também o checklist no `LEGACY-PROGRESS.md` com os novos IDs.

#### Passo 4: Popular Corpo da Task

##### Se `Destino de Tasks = Flyee`:

> **Seguir Flyee API** → Seção "📝 Adicionar Corpo" com template por categoria.

##### Se `Destino de Tasks = Local`:

Verificar no `BREAKDOWN-{escopo}.md` que cada task adicionada possui Descrição,
Arquivos afetados e Acceptance Criteria preenchidos.

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

[ ] Todos os débitos P0/P1/P2/P3 do TDD têm task no Tracker?
[ ] Cada task tem corpo preenchido (Problema + Solução + Impacto)?
[ ] Usuário aprovou o breakdown e prioridades?
[ ] Escopo de execução definido (ex: apenas P0 neste ciclo)?

❌ Se QUALQUER item desmarcado → NÃO PROSSEGUIR
✅ TODOS marcados → Prosseguir para Phase 7B
```

**Checkpoint salvo:** Tasks criadas no Flyee, breakdown aprovado

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
- `orchestrator` - Integração Tracker

> [!IMPORTANT]
> **Escopo:** Executar apenas as tasks aprovadas no gate (tipicamente P0s).
> P1/P2/P3 ficam como backlog para próximos ciclos.

#### 🔄 CONTEXT LOSS RESILIENCE (Phase 7B)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de implementar QUALQUER task na Phase 7B,
> o agente DEVE registrar o estado ativo no `LEGACY-PROGRESS.md`.
> Isso permite retomada automática se a conversa for truncada.

**Ao INICIAR cada task:**

1. Marcar a task como `[/]` no checklist da Phase 7B no `LEGACY-PROGRESS.md`
2. Adicionar seção `🔧 TASK ATIVA` ao `LEGACY-PROGRESS.md` (após a tabela de Status Geral):

```markdown
## 🔧 TASK ATIVA

| Campo | Valor |
|-------|-------|
| Task | #{id}: {título} |
| Passo | {0: Context Gathering / 0.5: Cross-Module / 1: Implementação / 2: Testes / 3: Verificação / 4: Doc Impact / 5: task-complete} |
| Flyee Status | Em Progresso |
| Início | {timestamp} |
| Workflow | `/legacy-project` Phase 7B |
| Retomar com | `/legacy-project --resume` |
```

3. Atualizar o campo `Passo` conforme o agente avança pelos sub-passos

**Ao CONCLUIR cada task:**

1. Remover seção `🔧 TASK ATIVA` do `LEGACY-PROGRESS.md`
2. Marcar task como `[x]` no checklist
3. **RE-LER** `LEGACY-PROGRESS.md` para identificar próxima task pendente
4. Continuar o loop OU notificar o usuário se todas as tasks foram concluídas

> [!IMPORTANT]
> O registro DEVE ser feito **ANTES** de qualquer modificação de código.
> Se o truncamento ocorrer antes do registro, a informação será perdida.
> Por isso, registrar o estado é a PRIMEIRA ação de cada task.

---

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

##### Se `Destino de Tasks = Flyee`:
a. Ler o **corpo completo da task no Tracker** (checklist, critérios de aceite, arquivos afetados)

##### Se `Destino de Tasks = Local`:
a. Ler o **corpo completo da task** no `docs/analysis/{escopo}/BREAKDOWN-{escopo}.md` (Descrição, Arquivos afetados, Acceptance Criteria)

##### Comum a ambos os modos:
b. Ler seção **🔗 Referências** da task (se houver) → abrir TDD referenciado (seções específicas)
c. Buscar **documentação de fluxo** relevante em `docs/flows/` (usar keywords da task: pagamento → `checkout/`, autenticação → `auth/`, etc.)
d. Se a task envolver pagamento/checkout/cart → ler `docs/flows/shop/checkout/` obrigatoriamente
e. Sintetizar contexto e preencher checklist de evidência abaixo

**Checklist de Evidência (salvar em `LEGACY-PROGRESS.md` sob a task):**

```markdown
📖 CONTEXT GATHERING — Task #{id}: {título}
[ ] Corpo da task lido no Flyee (ID: {page_id})
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

#### 🔒 Passo 0.5: Cross-Module Impact Check (OBRIGATÓRIO)

> [!CAUTION]
> **GATE BLOQUEANTE:** Se a task modifica **contratos compartilhados** (enums, interfaces/types,
> APIs, configurações em `config/`), o agente DEVE completar este checklist ANTES de implementar.
>
> **Anti-pattern real (Task #33):** Agente adicionou `PAGARME` ao enum PHP `PaymentGatewayType`
> e à config `shop.php`, mas não verificou o frontend (`shop/src/types/index.ts`), que manteve
> 11 gateways legados no enum TS `PaymentGateway`. Resultado: incompatibilidade backend↔frontend
> descoberta apenas na fase seguinte.

**Checklist de Impacto Cross-Module:**

```markdown
🔒 CROSS-MODULE IMPACT — Task #{id}
[ ] Contratos modificados identificados: {lista de enums/interfaces/APIs/configs}
[ ] Módulos consumidores mapeados: {ex: shop/, admin/, api/}
[ ] Compatibilidade verificada por módulo:
    - {módulo 1}: {status — compatível | requer mudança | N/A}
    - {módulo 2}: {status}
[ ] Sub-tasks ou flags criados para módulos afetados: {IDs ou "Nenhum necessário"}
```

> [!IMPORTANT]
> **Regra:** Se QUALQUER módulo consumidor requer mudança, o agente DEVE:
> 1. Documentar o impacto em `LEGACY-PROGRESS.md`
> 2. Se Flyee: Criar sub-task(s) no Flyee para os módulos afetados
>    Se Local: Adicionar sub-task(s) ao `BREAKDOWN-{escopo}.md`
> 3. Informar o usuário via `notify_user` antes de prosseguir

1. **Atualizar Tracker:** Status → "Em Progresso", `% Progresso: 10`
2. **Implementar:** Aplicar a correção **considerando o contexto do Passo 0 E Passo 0.5**
3. **Testar:** Executar testes existentes + novos se necessário
4. **Verificar:** Confirmar que nenhum teste quebrou

#### 📄 Passo 4.5: Doc Impact Check (OBRIGATÓRIO POR TASK)

> [!CAUTION]
> **GATE POR TASK:** Após implementar e testar cada task, o agente DEVE verificar
> se os arquivos modificados são referenciados em documentação existente.
> Docs desatualizados publicados no Flyee = informação errada para os devs.

**Ações:**

a. Listar os arquivos modificados pela task
b. Para cada arquivo, buscar referências em `docs/flows/` e `docs/design/TDD-*.md`:
   ```bash
   grep -rl "{nome_do_arquivo}" docs/flows/ docs/design/ 2>/dev/null
   ```
c. Se **referências encontradas** → Abrir cada doc e verificar se a descrição ainda corresponde ao estado real do código
d. Se **divergência detectada** → Atualizar o doc para refletir o estado pós-mudança, seguindo a mesma regra de CODE-TRUTH VALIDATION (Phase 4)
e. Registrar docs atualizados no `LEGACY-PROGRESS.md` sob a task:

```markdown
📄 DOC IMPACT — Task #{id}
- Arquivos modificados: {lista}
- Docs afetados: {lista de docs em docs/flows/ e docs/design/ ou "Nenhum"}
- Docs atualizados: {lista ou "N/A"}
```

5. **Completar:** Executar `/task-complete` (atualiza Flyee + LEGACY-PROGRESS.md)

#### 🔁 LOOP CONTINUATION (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** O agente NÃO PODE encerrar a sessão ou aguardar input
> entre tasks consecutivas da Phase 7B (a menos que o contexto esteja
> próximo do limite — ver estimativa abaixo).

Após concluir `/task-complete` para uma task da Phase 7B:

1. **Remover** seção `🔧 TASK ATIVA` do `LEGACY-PROGRESS.md`
2. **Re-ler** `LEGACY-PROGRESS.md` → seção Phase 7B checklist
3. **Identificar** próxima task `[ ]` (não concluída)
4. **Se existe próxima task** → Voltar ao Passo 0 (Context Gathering) daquela task
5. **Se TODAS concluídas** → Prosseguir para Gate 7B → 8

> [!TIP]
> **Estimativa de contexto:** Se o agente estima que a próxima task consumirá
> mais de 50% do contexto restante, notificar o usuário:
> ```
> ⚠️ Contexto próximo do limite. Tasks restantes: {N}
> Recomendo pausar e retomar com `/legacy-project --resume`.
> ```

#### 🔄 TASK SYNC - Phase 7B (OBRIGATÓRIO)

> [!CAUTION]
> **Ao concluir CADA task de melhoria**, executar sync.
> Se modo Flyee: seguir Flyee API → seção "PHASE TASK TRACKING" → "Gate: TRACKER SYNC".

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Atualizar task correspondente no
> `BREAKDOWN-{escopo}.md` (Status → `[x] Concluído`, Esforço real) e checklist no `LEGACY-PROGRESS.md`.
> Pular chamadas a APIs do Flyee.

Para cada task concluída:

1. Atualizar task → Status: "Concluído", `Tempo Gasto`, `% Progresso: 100`
2. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

```json
// Tool: Flyee API: update_task() (output)
{
  "block_id": "{page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    {
      "type": "callout",
      "callout": {
        "icon": { "type": "emoji", "emoji": "✅" },
        "rich_text": [
          { "type": "text", "text": { "content": "Concluído em {data}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": { "content": "📋 {resumo da implementação}" }
          }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          { "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }
        ]
      }
    },
    {
      "type": "bulleted_list_item",
      "bulleted_list_item": {
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "📁 Arquivos: {lista de arquivos modificados}"
            }
          }
        ]
      }
    }
  ]
}
```

3. Adicionar comentário rico de conclusão

**Ao concluir TODAS as tasks aprovadas:** 4. Verificar que TODAS as tasks de melhorias estão synced (Gate de Conclusão) 5. Atualizar `LEGACY-PROGRESS.md`

**Checkpoint salvo:** Melhorias implementadas e synced no Flyee

---

### Gate 7B → 8: DOC FRESHNESS GATE (OBRIGATÓRIO)

> [!CAUTION]
> **GATE BLOQUEANTE:** Antes de publicar qualquer documentação no Flyee (Phase 8),
> o agente DEVE re-validar TODOS os docs gerados nas phases 4-5 contra o código atual.
> Phase 7B pode ter alterado comportamento documentado — publicar sem re-validar
> significa entregar docs incorretos aos devs.

**Checklist:**

```markdown
⚠️ DOC FRESHNESS GATE — Antes da Phase 8

[ ] Re-executar CODE-TRUTH VALIDATION (Phase 4) em CADA doc de `docs/flows/`
[ ] Re-executar CODE-TRUTH VALIDATION em `docs/design/TDD-*.md`
[ ] Divergências encontradas? → Docs atualizados com estado real pós-7B
[ ] Divergências registradas em LEGACY-PROGRESS.md
[ ] Se nenhuma divergência → Registrar: "✅ Docs validados — nenhuma atualização necessária"

❌ Se QUALQUER item desmarcado → NÃO PROSSEGUIR para Phase 8
✅ TODOS marcados → Prosseguir
```

> [!TIP]
> Se o Passo 4.5 (Doc Impact Check) foi executado corretamente para cada task,
> este gate será rápido — a maioria dos docs já estará atualizada.

---

### Phase 8: HANDOVER + PUBLICAÇÃO DE DOCUMENTAÇÃO TÉCNICA

> [!CAUTION]
> **REGRA BLOQUEANTE:** Esta fase tem **DUAS partes obrigatórias**:
> 1. **Passo 0:** Criar HANDOVER + TEST-GUIDE para o escopo atual
> 2. **Passos 1-4:** Publicar TODOS os docs (flow docs, TDD, DS, handover, test-guide)
>
> Uma sem a outra = **fase INCOMPLETA**. O agente NÃO PODE marcar Phase 8 como ✅
> sem completar AMBAS as partes.

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Passo 0 (criar HANDOVER + TEST-GUIDE) é executado normalmente.
> Passos 1-4 (publicação no Flyee) são **substituídos** por: registrar no `LEGACY-PROGRESS.md`
> que os documentos foram criados, incluindo caminhos dos arquivos gerados.

> [!CAUTION]
> 🔴 **FALHA HISTÓRICA (api/ e admin/):** O agente criou HANDOVER + TEST-GUIDE
> mas **PULOU a publicação dos flow docs/TDD/DS no Flyee** (Database "Documentação Técnica").
> Resultado: devs sem acesso à documentação completa. **Causa raiz:** Phase 8 no
> `LEGACY-PROGRESS.md` dizia "Documentação Final" sem mencionar publicação Flyee,
> e o agente interpretou como "só criar handover".

**Objetivo:** (1) Criar documentação de handover e (2) Publicar documentação completa (Flyee) ou registrar no LEGACY-PROGRESS.md (Local).

**Trigger:**

```
Gate 7B→8 (DOC FRESHNESS) concluído → Automático
```

**Agentes Envolvidos:**

- `orchestrator` - Integração Tracker (se modo Flyee)

> [!IMPORTANT]
> **SKILL:** Se modo Flyee, seguir Flyee API → seção "DOCUMENTATION DATABASES" OBRIGATORIAMENTE.

#### Passo 0: Criar Handover e Test Guide (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA BLOQUEANTE:** ANTES de publicar docs no Flyee, o agente DEVE criar
> os documentos de handover e guia de testes para o escopo atual. Estes documentos
> consolidam toda a informação gerada nas fases anteriores.

**0.1 - Criar HANDOVER-{escopo}.md:**

Caminho: `docs/handover/{escopo}/HANDOVER-{escopo}.md`

Conteúdo obrigatório (seguir formato dos escopos anteriores):

| Seção | Conteúdo |
|-------|----------|
| Visão Geral | Stack, arquitetura, dependências |
| Fluxos Críticos | Resumo dos flow docs (Phase 4) |
| Integrações | APIs externas, gateways, services |
| Débitos Resolvidos | Lista de melhorias implementadas (Phase 7B) |
| Débitos Pendentes | Itens não implementados do TDD |
| Decisões Técnicas | Decisões tomadas durante o projeto |
| Como Rodar | Setup local, env vars, comandos |
| Referências | Links para docs detalhados |

**0.2 - Criar TEST-GUIDE-{escopo}.md:**

Caminho: `docs/tests/{escopo}/TEST-GUIDE-{escopo}.md`

Conteúdo obrigatório:

| Seção | Conteúdo |
|-------|----------|
| Stack de Testes | Ferramentas, versões, config |
| Estrutura | Diretórios e organização |
| Mapa de Testes | Tests por domínio (cobertura atual) |
| Como Executar | Comandos para rodar testes |
| Patterns Usados | MSW, mocks, factories, etc |
| Troubleshooting | Problemas comuns e soluções |
| Expansão | Próximos testes prioritários |

**0.3 - Criar task e executar `/task-complete`:**

##### Se `Destino de Tasks = Flyee`:

1. Criar task: `Handover + Publicação: {escopo}` (Categoria: Documentação, Épico: {escopo} - Documentação)
2. Executar `/task-complete` após criar ambos os docs

##### Se `Destino de Tasks = Local`:

1. Registrar task `T-{seq}: Handover + Publicação: {escopo}` no `BREAKDOWN-{escopo}.md`
2. Executar `/task-complete` em modo local (atualizar BREAKDOWN + LEGACY-PROGRESS.md)

> [!WARNING]
> **SELF-CHECK antes de prosseguir para Passo 1:**
> - [ ] HANDOVER-{escopo}.md existe em `docs/handover/{escopo}/`?
> - [ ] TEST-GUIDE-{escopo}.md existe em `docs/tests/{escopo}/`?
> - [ ] Task criada e concluída? (Flyee ou LEGACY-PROGRESS.md conforme modo)
> → Se QUALQUER item = NÃO → PARAR e completar ANTES de publicar

#### Passo 1: Discovery e Validação da Database "Documentação Técnica" (APENAS MODO FLYEE)

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Pular Passos 1-4 inteiramente.
> Registrar no `LEGACY-PROGRESS.md` que os documentos foram criados, listando
> os caminhos dos arquivos gerados. Não fazer chamadas a APIs do Flyee.

> Seguir Flyee API → seção "DATABASE 1"

```json
// Tool: Flyee API: list_tasks()
{
  "query": "Documentação Técnica",
  "filter": { "property": "object", "value": "data_source" }
}
```

```json
// Tool: Flyee API: list_tasks()
{ "database_id": "{DOC_TECNICA_DATABASE_ID}" }
```

> Se database ausente ou propriedades faltando → PARAR e notificar usuário (ver skill para mensagem).

#### Passo 2: Coletar Artefatos Gerados

Listar todos os docs gerados nas fases anteriores:

| Fonte     | Tipo          | Arquivo Local                                        | Publicar?  |
| --------- | ------------- | ---------------------------------------------------- | ---------- |
| Phase 1   | Arquitetura   | `docs/CODEBASE-{projeto}.md`                         | ✅         |
| Phase 4   | Fluxo         | `docs/flows/{módulo}/{fluxo}.md` (cada)              | ✅         |
| Phase 5   | TDD           | `docs/design/TDD-{projeto}-{módulo}.md`              | ✅         |
| Phase 5.5 | Design System | `design-system/MASTER.md`                            | ✅ (se UI) |
| Phase 6   | Testes        | (relatório de cobertura)                             | ✅         |
| Phase 8   | Handover      | `docs/handover/{módulo}/HANDOVER-{módulo}.md`        | ✅         |
| Phase 8   | Test Guide    | `docs/tests/{módulo}/TEST-GUIDE-{módulo}.md`         | ✅         |

#### Passo 3: Para Cada Artefato — Publicar

> Seguir Flyee API → seção "Processo: Publicação de Documentação Técnica"

Para cada doc:

1. **Verificar upsert** — doc já existe na database? (query por Nome + Módulo)
2. **Ler conteúdo completo** do arquivo local
3. **Criar ou atualizar** página Flyee com template correto para o tipo
4. **Preencher propriedades:** Nome, Módulo, Tipo, Status, Última Atualização, Arquivo Local, Tasks Relacionadas
5. **Incluir histórico** de atualizações referenciando tasks da database "Tarefas"

#### Passo 4: Relatório de Publicação

```markdown
📚 **DOCUMENTAÇÃO TÉCNICA PUBLICADA - {módulo}**

| #   | Documento | Tipo  | Status    | Flyee |
| --- | --------- | ----- | --------- | ------ |
| 1   | {nome}    | Fluxo | Publicado | 🔗     |
| 2   | {nome}    | TDD   | Publicado | 🔗     |
| ... | ...       | ...   | ...       | ...    |

Total: {N} documentos publicados
✅ Devs podem consultar em: Flyee → Database "Documentação Técnica"
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

**Checkpoint salvo:** Documentação técnica publicada no Flyee

---

### Phase 8.5: PUBLICAÇÃO DO MANUAL DO USUÁRIO

> [!CAUTION]
> **REGRA BLOQUEANTE:** Para cada fluxo publicado na Phase 8, DEVE existir uma versão
> em linguagem acessível.
> Usuários finais e operadores leem estes guias — sem código, sem jargão técnico.

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Gerar os guias de usuário como arquivos locais
> em `docs/user-guides/{escopo}/` e registrar no `LEGACY-PROGRESS.md`.
> Pular discovery/publicação na database Flyee "Manual do Usuário".

**Objetivo:** Publicar guias em linguagem acessível (Flyee) ou gerar localmente (Local).

**Trigger:**

```
Phase 8 concluída → Automático
```

**Agentes Envolvidos:**

- `orchestrator` - Integração Tracker

> [!IMPORTANT]
> **SKILL:** Seguir Flyee API → seção "Processo: Publicação do Manual do Usuário" OBRIGATORIAMENTE.

#### Passo 1: Discovery e Validação da Database "Manual do Usuário" (APENAS MODO FLYEE)

> [!NOTE]
> **Se `Destino de Tasks = Local`:** Pular Passo 1 (discovery do Flyee).
> Gerar guias como arquivos `.md` em `docs/user-guides/{escopo}/`
> e registrar no `LEGACY-PROGRESS.md`.

> Seguir Flyee API → seção "DATABASE 2"

```json
// Tool: Flyee API: list_tasks()
{
  "query": "Manual do Usuário",
  "filter": { "property": "object", "value": "data_source" }
}
```

> Se database ausente → PARAR e notificar usuário (ver skill para mensagem).

#### Passo 2: Mapear Fluxos → Guias

> Seguir Flyee API → tabela "Mapear Fluxos Técnicos → Guias de Usuário"

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

| #   | Guia   | Público-alvo  | Seção   | Status    |
| --- | ------ | ------------- | ------- | --------- |
| 1   | {nome} | Usuário Final | {seção} | Publicado |
| ... | ...    | ...           | ...     | ...       |

Total: {N} guias publicados
✅ Usuários e operadores podem consultar em: Flyee → Database "Manual do Usuário"
```

**Gate de Saída:**

```
[ ] Database "Manual do Usuário" encontrado e validado
[ ] Todos os fluxos mapeados para guias
[ ] Upsert verificado (sem duplicatas)
[ ] Conteúdo sem jargão técnico
[ ] LEGACY-PROGRESS.md atualizado
```

**Checkpoint salvo:** Manual do usuário publicado no Flyee

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
3. Atualizar task master no Flyee (se houver)

**Se há escopos pendentes (OBRIGATÓRIO):**

```
✅ Módulo {módulo} concluído!

📊 Resumo:
- Fluxos documentados: X
- Tasks criadas no Flyee: Y
- Cobertura de testes: Z%
- 📚 Docs publicados para cliente: W

📚 Devs consultam: Flyee → Database "Documentação Técnica"
📖 Usuários consultam: Flyee → Database "Manual do Usuário"

⚠️ ATENÇÃO: Existem {N} escopos ainda NÃO analisados:

| Escopo | Criticidade | Status |
|--------|-------------|--------|
| {escopo} | {criticidade} | ⏳ Pendente |

🔴 O workflow NÃO está concluído até que todos os escopos sejam analisados.

Deseja:
1. Continuar com o próximo módulo agora
2. Pausar e retomar depois (/legacy-project --resume)
```

> [!CAUTION]
> **REGRA DE PROPOSTA:** Ao apresentar plano para o próximo escopo, o agente DEVE:
>
> 1. Incluir Phase 3.5 (Flyee Setup + Breakdown) como fase **DISTINTA** e **ANTERIOR** à documentação
> 2. NUNCA condensar criação de tasks junto com publicação de docs na última fase
> 3. A ordem obrigatória é: Análise → **Criar tasks no Tracker** → Documentação → TDD → Testes → Melhorias → Publicação
> 4. Se o plano apresentado ao usuário não tiver task creation antes de documentação, o plano é **INVÁLIDO**

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
  - Flyee → Database "Documentação Técnica" (devs)
  - Flyee → Database "Manual do Usuário" (usuários e operadores)
```

**Checkpoint salvo:** Módulo marcado como completo, escopos pendentes listados

---

## 📁 Estrutura de Arquivos Gerados

```
projeto/
├── docs/
│   ├── LEGACY-PROGRESS.md              # ⭐ Arquivo de controle (checklists + refs)
│   ├── CODEBASE-{projeto}.md           # Visão geral
│   ├── INDEX.md                         # Atualizado
│   ├── analysis/
│   │   └── {escopo}/                    # Por módulo
│   │       └── BREAKDOWN-{escopo}.md    # ⭐ Tasks locais (se modo Local)
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
| Destino de Tasks   | {Flyee / Local} |
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

→ BREAKDOWN: `docs/analysis/{módulo}/BREAKDOWN-{módulo}.md`

### Phase 7B: Execução de Melhorias ⏳

### Phase 8: Handover + Publicação ⏳
- [ ] HANDOVER-{escopo}.md criado
- [ ] TEST-GUIDE-{escopo}.md criado
- [ ] Task Flyee criada e concluída
- [ ] Docs publicados no Flyee (Database "Documentação Técnica")
- [ ] LEGACY-PROGRESS.md atualizado

### Phase 9: Próximo Escopo ⏳

---

## 📜 Histórico de Ações

| Data             | Fase | Ação                        |
| ---------------- | ---- | --------------------------- |
| 2025-01-15 10:30 | 1    | Overview concluído          |
| 2025-01-15 11:00 | 2    | Escopo src/auth selecionado |
| 2025-01-15 14:00 | 4    | Fluxo login documentado     |
| ...              | ...  | ...                         |

---

## 🔄 Para Retomar

\```bash
/legacy-project --resume
\```
````

---

## 🔗 INTEGRAÇÃO COM FLYEE (Automática na Phase 7A)

> [!IMPORTANT]
> A integração com Flyee é **automática** na Phase 7A.
> A flag `--flyee` agora é apenas para tracking do workflow em si.

### Tasks de Melhorias (Phase 7A/7B)

Para cada melhoria identificada, uma task é criada automaticamente:

| Propriedade | Valor                          |
| ----------- | ------------------------------ |
| Título      | `{descrição}`                  |
| ID          | `R.{seq}` ou `{módulo}.{seq}`  |
| Épico       | `{módulo}` (ex: auth, payment) |
| Status      | `A Fazer`                      |
| Categoria   | `Refatoração`                  |
| Prioridade  | `P0-P3`                        |
| Corpo       | Contexto + Problema + Solução  |

### View "Visão Cliente"

Para transparência, crie view filtrada no Flyee:

- Apenas: Nome, Status
- Ver instruções em `README.md` seção "Configuração > Flyee"

### Tracking do Workflow (Opcional com --flyee)

Se `--flyee` especificado, também cria:

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
7. **🔄 TASK TRACKING OBRIGATÓRIO** - Toda atividade pós-análise (Phase 4+) DEVE ter task registrada (Flyee ou Local conforme `Destino de Tasks` definido na Phase 3.5). Se Flyee: seguir Flyee API → "PHASE TASK TRACKING". Se Local: registrar no `BREAKDOWN-{escopo}.md` + checklist no `LEGACY-PROGRESS.md`. Trabalho sem task = falha de transparência
8. **🔀 PHASE 7A ≠ 7B** - Phase 7A (Breakdown) cria tasks no Tracker a partir do TDD. Phase 7B (Execução) implementa as melhorias aprovadas. NUNCA misturar planejamento com execução na mesma phase. O gate entre 7A→7B é OBRIGATÓRIO
9. **📚 HANDOVER + DOCUMENTAÇÃO PARA DEVS E USUÁRIOS** - Ao final de cada módulo (Phase 8 + 8.5): (a) criar HANDOVER-{escopo}.md e TEST-GUIDE-{escopo}.md, (b) se modo Flyee: publicar TODOS os docs nas databases "Documentação Técnica" e "Manual do Usuário"; se modo Local: registrar docs criados no LEGACY-PROGRESS.md. **AMBAS as partes são obrigatórias.** Se modo Flyee: seguir Flyee API → "DOCUMENTATION DATABASES"
10. **🛡️ ESCOPOS PENDENTES = WORKFLOW INCOMPLETO** - O workflow NÃO PODE ser considerado encerrado se existirem escopos com status `⏳ Pendente` no `LEGACY-PROGRESS.md`. Ao finalizar qualquer phase, o agente DEVE verificar escopos pendentes e informar o usuário. Ignorar escopos = falha de cobertura
11. **📋 SEQUÊNCIA DE PHASES/TASKS OBRIGATÓRIA** - O agente DEVE seguir a ordem numérica: Phase 4 → 5 → 5.5 → 6 → 7A → 7B → 8 → 9. Ao sugerir "próximos passos", DEVE consultar `LEGACY-PROGRESS.md` para identificar a próxima phase pendente. **PROIBIDO** sugerir tasks de phases posteriores enquanto a phase atual tiver tasks incompletas. Exemplo: NÃO sugerir Phase 7B (Execução) quando Phase 7A (Breakdown) ainda não foi aprovada
12. **📊 PROGRESS SYNC OBRIGATÓRIO** - Ao concluir QUALQUER phase, o `LEGACY-PROGRESS.md` DEVE ser atualizado IMEDIATAMENTE com: (a) checklist da phase marcado como ✅, (b) fase atual incrementada, (c) data de última atualização, (d) entrada no histórico de ações. Antes de sugerir "próximos passos", o agente DEVE verificar se o `LEGACY-PROGRESS.md` está atualizado
13. **📄 DOC REFRESH PÓS-CÓDIGO OBRIGATÓRIO** - Após QUALQUER phase que modifica código (7B), documentação gerada em phases anteriores (Phase 4 flow docs, Phase 5 TDD) DEVE ser revalidada via CODE-TRUTH VALIDATION ANTES de publicação (Phase 8). O Passo 4.5 (Doc Impact Check) na Phase 7B é por task; o Gate 7B→8 (DOC FRESHNESS GATE) é a verificação final consolidada. Publicar docs desatualizados = falha de transparência equivalente a trabalho sem task

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

# Com sincronização Flyee
/legacy-project --flyee c:\projetos\app

# Forçar re-análise
/legacy-project --scope src/auth --force c:\projetos\app
```

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
