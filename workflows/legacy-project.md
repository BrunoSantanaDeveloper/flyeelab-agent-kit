---
description: Workflow unificado para projeto legado. Análise → Documentação → TDD Reverso → Melhorias. Engenharia reversa e modernização. Suporta projetos grandes com checkpointing.
skills: notion-task-patterns, checkpointing-patterns, history-check-patterns
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
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   OVERVIEW   │───▶│   ESCOPO     │───▶│ DOCUMENTAÇÃO │───▶│  TDD REVERSO │───▶│   TESTES     │───▶│  MELHORIAS   │
│  (Mapear)    │    │  (Escolher)  │    │  (Fluxos)    │    │  (Técnico)   │    │  (Cobrir)    │    │ (Tasks)      │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       ✅                  ✋                  ✅                  ✋                  ✅                  ✅
   Automático          Seleção           Automático          Aprovação           Incremental         Priorizado
```

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

**Checkpoint salvo:** Estado inicial registrado

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

**Checkpoint salvo:** TDD gerado

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

**Checkpoint salvo:** Cobertura atual registrada

---

### Phase 7: BREAKDOWN DE MELHORIAS + NOTION

**Objetivo:** Criar tasks de refactoring priorizadas **e registrar no Notion**.

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

1. Executar `/tdd breakdown docs/design/TDD-{projeto}-{módulo}.md`
2. Criar tasks priorizadas:
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
- [ ] `Status` (status)
- [ ] `% Progresso` (number)
- [ ] `ID` (rich_text)
- [ ] `Categoria` (multi_select)
- [ ] `Prioridade` (select)
- [ ] `Épico` (select)

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

#### Passo 3: Criar Tasks no Notion

Para **CADA melhoria** identificada:

```
Use: mcp_notion-mcp-server_API-post-page

parent: { "database_id": "{DATABASE_ID}" }
properties: {
  "{Título}": { "title": [{ "text": { "content": "{descrição}" } }] },
  "ID": { "rich_text": [{ "text": { "content": "R.{seq}" } }] },
  "Épico": { "select": { "name": "{módulo}" } },
  "Status": { "status": { "name": "A Fazer" } },
  "% Progresso": { "number": 0 },
  "Categoria": { "multi_select": [{ "name": "Refatoração" }] },
  "Prioridade": { "select": { "name": "{P0/P1/P2/P3}" } },
  "Estimativa": { "rich_text": [{ "text": { "content": "{Xh}" } }] }
}
```

> **ID para Refatorações:** Usar `R.{seq}` (ex: `R.1`, `R.2`) ou `{módulo}.{seq}` (ex: `auth.1`)

#### Passo 4: Popular Corpo da Task

```
Use: mcp_notion-mcp-server_API-patch-block-children
block_id: {page_id}
children: [
  { "heading_2": { "rich_text": [{ "text": { "content": "📋 Contexto" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "Identificado durante análise de `/legacy-project`\nMódulo: {módulo}\nTDD Ref: docs/design/TDD-{projeto}-{módulo}.md" } }] } },
  { "heading_2": { "rich_text": [{ "text": { "content": "🎯 Problema" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "{descrição do débito/problema}" } }] } },
  { "heading_2": { "rich_text": [{ "text": { "content": "✅ Solução Proposta" } }] } },
  { "paragraph": { "rich_text": [{ "text": { "content": "{solução técnica}" } }] } }
]
```

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

**Checkpoint salvo:** Tasks criadas no Notion

---

### Phase 8: PRÓXIMO ESCOPO

**Objetivo:** Verificar se há mais módulos para analisar.

**Trigger:**
```
Phase 7 concluída
```

**Ações:**
1. Verificar `docs/LEGACY-PROGRESS.md`
2. Atualizar task master no Notion (se houver)
3. Se há escopos pendentes:
   ```
   ✅ Módulo src/auth concluído!
   
   📊 Resumo:
   - Fluxos documentados: X
   - Tasks criadas no Notion: Y
   - Cobertura de testes: Z%
   
   Próximos módulos pendentes:
   - src/payment (🔴 crítico)
   - src/users (🟡 médio)
   
   Deseja continuar com o próximo módulo?
   ```
4. Se todos concluídos: Gerar relatório final

**Checkpoint salvo:** Módulo marcado como completo

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
### Phase 7: Tasks ⏳

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

## 🔗 INTEGRAÇÃO COM NOTION (Automática na Phase 7)

> [!IMPORTANT]
> A integração com Notion é **automática** na Phase 7.
> A flag `--notion` agora é apenas para tracking do workflow em si.

### Tasks de Melhorias (Phase 7)

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
- Apenas: Nome, Status, % Progresso
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
