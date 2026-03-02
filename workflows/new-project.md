---
description: Workflow unificado para novo projeto. Orquestra PRD → TDD Técnico → Design System → Breakdown → TDD Metodologia → Implementação → Deploy. Fluxo completo com checkpointing.
skills: notion-task-patterns, checkpointing-patterns, project-tracking-patterns, ui-ux-discovery, local-verification, integration-completeness, content-strategy, page-specifications, design-md, enhance-prompt, react-components, stitch-loop, remotion, shadcn-ui, component-library-discovery
---

# /new-project - Novo Projeto Completo

$ARGUMENTS

---

## 🎯 PROPÓSITO

Workflow **orquestrador** que guia a criação de um novo projeto do zero, garantindo:
- Exploração de ideias quando necessário (Brainstorm)
- Documentação completa (PRD + TDD)
- Testes antes do código (TDD Metodologia)
- Rastreabilidade entre documentos
- Cobertura mínima de 80%

---

## 📊 QUANDO USAR ESTE WORKFLOW?

> [!TIP]
> **Use este guia para escolher o workflow correto:**

| Situação | Workflow Recomendado | Por quê? |
|----------|---------------------|----------|
| Ideia vaga, preciso explorar opções | `/new-project --brainstorm` | Inclui fase de exploração |
| Ideia clara, quero documentação formal | `/new-project` | Fluxo completo com PRD + TDD |
| Projeto rápido, sem PRD formal | `/new-project --quick` | Direto para TDD + Tasks |
| Apenas explorar ideias técnicas | `/brainstorm` | Sem compromisso de implementar |
| Projeto legado, preciso documentar | `/document` → `/discovery --from-project` | Engenharia reversa |
| Nova feature em projeto existente | `/enhance` ou `/tdd new` | Contexto já existe |

---

## 🧩 SUBCOMMANDS

| Comando | Ação |
|---------|------|
| `/new-project [nome]` | Fluxo **completo** (PRD → TDD → Tests → Code) |
| `/new-project --brainstorm [nome]` | Inclui **Phase 0** para explorar ideias |
| `/new-project --quick [nome]` | Modo **ágil** (sem PRD formal, direto TDD) |
| `/new-project --resume` | **Retomar** de onde parou |
| `/new-project --from-prd [arquivo]` | Continua de PRD já aprovado |
| `/new-project --from-tdd [arquivo]` | Continua de TDD já aprovado |
| `/new-project --from-demand [nome]` | Importa de proposta comercial aprovada |
| `/new-project --from-figma [url]` | Importa Design System do Figma |
| `/new-project status` | Mostra status e progresso atual |

---

## 🔀 MODOS DE OPERAÇÃO

### Modo COMPLETO (Padrão)
```
/new-project meu-app
```
```
Phase 1 (PRD) → Phase 2 (TDD) → Phase 2.1 (Notion) → Phase 2.5+ (Design) → Phase 3 (Breakdown) → Phase 4 (Tests) → Phase 5 (Code) → Phase 6 (Verify) → Phase 7 (Deploy)
```

### Modo BRAINSTORM (Ideia indefinida)
```
/new-project --brainstorm meu-app
```
```
Phase 0 (Brainstorm) → Phase 1 (PRD) → Phase 2 (TDD) → Phase 2.1 (Notion) → ... → Phase 7 (Deploy)
```

### Modo QUICK (Ágil, sem PRD formal)
```
/new-project --quick meu-app
```
```
Phase 2 (TDD) → Phase 3 (Breakdown) → Phase 4 (Tests) → Phase 5 (Code) → Phase 6 (Verify) → Phase 7 (Deploy)
```
> Pula Phase 0 e Phase 1. Vai direto para TDD com Socratic Gate simplificado.

---

## 💾 SISTEMA DE CHECKPOINTING

> [!IMPORTANT]
> **Projetos podem ser interrompidos.** O workflow salva progresso em `docs/PROJECT-PROGRESS.md` a cada fase.

### Arquivo de Controle: `docs/PROJECT-PROGRESS.md`

Criado automaticamente ao iniciar o projeto, contém:

| Seção | Conteúdo |
|-------|----------|
| Status Geral | Nome, fases, última atualização |
| Fases | Checklist de cada phase com artefatos |
| Tasks | Lista de tasks pendentes/concluídas |
| Histórico | Log de ações |

### Retomada Automática

```bash
# Retomar de onde parou
/new-project --resume

# Ver status
/new-project status
```

**Ao executar `--resume`:**
1. Carrega `docs/PROJECT-PROGRESS.md`
2. Identifica fase pendente
3. **🚨 DESYNC DETECTOR (OBRIGATÓRIO):**
   - Comparar tasks marcadas como ✅ em PROJECT-PROGRESS.md
   - Com status real no Notion (query por ID)
   - Se LOCAL=✅ mas NOTION=Não iniciado → **PARAR e executar sync retroativo**
4. Continua execução (apenas se sem desync)

> [!CAUTION]
> **DESYNC DETECTOR:** Antes de continuar qualquer trabalho em --resume, o agente DEVE:
> 1. Buscar status de TODAS as tasks marcadas como completas localmente
> 2. Se encontrar desync (local ✅, Notion ≠ Concluído) → Executar sync retroativo PRIMEIRO
> 3. Só prosseguir após confirmar: "Nenhum desync detectado" ou "Desync corrigido"

### Template: PROJECT-PROGRESS.md

```markdown
# Project Progress - {nome}

> Arquivo de controle para retomar workflow de onde parou.
> ⚠️ NÃO EDITAR MANUALMENTE - Atualizado automaticamente.

## 📊 Status Geral

| Campo | Valor |
|-------|-------|
| Projeto | {nome} |
| Modo | completo / quick / brainstorm |
| Iniciado em | {data} |
| Última atualização | {data} |
| Status | 🟡 Em Progresso |
| Fase Atual | 4/7 - TDD Metodologia |

---

## 📋 Fases

| Fase | Status | Artefato |
|------|--------|----------|
| 0. Brainstorm | ⏭️ Pulado | - |
| 1. PRD | ✅ Aprovado | `docs/PRD-{nome}.md` |
| 2. TDD Técnico | ✅ Aprovado | `docs/design/TDD-{nome}.md` |
| 2.1 Notion Setup | ✅ Concluído | {N} tasks de planejamento |
| 3. Breakdown | ✅ Concluído | 12 tasks criadas |
| 4. TDD Metodologia | 🟡 Em Progresso | 5/12 testes escritos |
| 5. Implementação | ⏳ Pendente | - |
| 6. Verificação | ⏳ Pendente | - |
| 7. Deploy | ⏳ Pendente | - |

---

## 📝 Tasks (Phase 4-5)

| # | Task | Teste | Código | Status |
|---|------|-------|--------|--------|
| 1 | Setup inicial | ✅ | ✅ | ✅ Completo |
| 2 | Auth básica | ✅ | ✅ | ✅ Completo |
| 3 | CRUD usuários | ✅ | 🟡 | 🟡 Em Progresso |
| 4 | Integração API | ⏳ | ⏳ | ⏳ Pendente |
| ... | ... | ... | ... | ... |

---

## 📜 Histórico

| Data | Fase | Ação |
|------|------|------|
| 2025-01-15 10:00 | 1 | PRD criado |
| 2025-01-15 14:00 | 1 | PRD aprovado |
| 2025-01-16 09:00 | 2 | TDD técnico criado |
| ... | ... | ... |

---

## 🔄 Como Retomar

\```bash
/new-project --resume
\```
```

---

## 🔴 FLUXO COMPLETO

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  BRAINSTORM  │───▶│     PRD      │───▶│  TDD TÉCNICO │───▶│  REFERÊNCIAS │───▶│DESIGN SYSTEM │───▶│   CONTENT    │───▶│   STITCH     │───▶│  PAGE SPECS  │───▶│   BREAKDOWN  │───▶│    TESTS     │───▶│   IMPLEMENT  │───▶│   DEPLOY     │
│  (OPCIONAL)  │    │  (O QUE)     │    │   (COMO)     │    │  (COLETAR)   │    │   (TOKENS)   │    │  (O QUE DIZ) │    │ (PROTÓTIPO)  │    │ (BLUEPRINT)  │    │   (TASKS)    │    │  (PRIMEIRO)  │    │   (CÓDIGO)   │    │  (PREVIEW)   │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
      🧠                   ✋                  ✋                  ✋                  ✋                  ✋                  ✋                  ✋                  ✅                  ✅                  ✅                  ✅
   Exploração          Aprovação           Aprovação         Pergunta+Coleta      Aprovação           Aprovação       Aprovação+/stitch     Aprovação          Automático          Automático          Automático            Final
```

> **📋 Phase 2.1 (Notion Setup)** ocorre entre TDD TÉCNICO e REFERÊNCIAS, criando tasks de tracking para fases 2.5–2.9.
> **📋 Phase 2.45 (Referências)** pergunta como o usuário quer definir o Design System (recomendações, referências visuais, manual, ou combinação).

---

### Phase 0: BRAINSTORM (Opcional)

> [!NOTE]
> **Ativado com:** `/new-project --brainstorm [nome]`
> **Pule se:** A ideia já está clara e definida.

**Objetivo:** Explorar opções antes de se comprometer com uma direção.

**Trigger:**
```
/new-project --brainstorm [nome-do-projeto]
```

**Agentes Envolvidos:**
- `project-planner` - Estruturação de opções
- Especialistas de domínio conforme necessidade

**Ações:**
1. Executar `/brainstorm [nome]`
2. Gerar 3+ opções de abordagem
3. Comparar prós/contras de cada
4. **AGUARDAR** escolha do usuário

**Output Format:**
```markdown
## 🧠 Brainstorm: [Nome do Projeto]

### Option A: [Abordagem 1]
✅ Pros: ...
❌ Cons: ...
📊 Effort: Low | Medium | High

### Option B: [Abordagem 2]
...

### Option C: [Abordagem 3]
...

## 💡 Recommendation
Option [X] porque [razão].

Qual direção seguir?
```

**Gate de Saída:**
```
[ ] Usuário escolheu uma direção
```

---

### Phase 1: PRD - Product Requirements Document

> [!NOTE]
> **Pulado no modo --quick**

**Objetivo:** Definir O QUE será construído.

**Trigger:**
```
/new-project [nome-do-projeto]
ou
Brainstorm concluído → Automático
```

**Agentes Envolvidos:**
- `product-owner` - Lead do discovery
- `project-planner` - Estruturação

**Ações:**
1. Executar `/prd new [nome]`
2. Aplicar Socratic Gate completo (12 perguntas)
3. Gerar `docs/PRD-{nome}.md`
4. **AGUARDAR** aprovação humana

**Gate de Saída:**
```
[ ] PRD aprovado pelo humano
```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir sem aprovação do PRD.

---

### Phase 2: TDD TÉCNICO - Technical Design Document

**Objetivo:** Definir COMO será construído.

**Trigger:**
```
PRD aprovado → Automático
ou
/new-project --from-prd docs/PRD-{nome}.md
ou
/new-project --quick [nome] (Socratic Gate simplificado)
```

**Agentes Envolvidos:**
- `project-planner` - Arquitetura
- Backend/Frontend specialists conforme necessidade

**Ações (Modo Completo):**
1. Executar `/tdd new [nome]`
2. **Referenciar PRD:** `PRD Fonte: docs/PRD-{nome}.md`
3. Preencher com base nas respostas do PRD
4. Gerar `docs/design/TDD-{nome}.md`
5. Validar com `/tdd validate`
6. **AGUARDAR** aprovação humana

**Ações (Modo --quick):**
1. Aplicar Socratic Gate simplificado (5 perguntas):
   - 🎯 Qual problema estamos resolvendo?
   - 👥 Quem são os usuários?
   - 📦 O que é MVP?
   - 🔗 Integrações necessárias?
   - ⏰ Prazo esperado?
2. Gerar `docs/design/TDD-{nome}.md` diretamente
3. Validar e **AGUARDAR** aprovação

**Gate de Saída:**
```
[ ] TDD validado (>= 75% completo)
[ ] Nenhum item INDEFINIDO bloqueador
[ ] **Environment Strategy definida no TDD** (dev vs staging vs prod) ⭐
[ ] TDD aprovado pelo humano
```

> [!CAUTION]
> **ENVIRONMENT STRATEGY (OBRIGATÓRIO):** O TDD DEVE conter uma seção `## Environment Strategy`
> definindo separação de ambientes ANTES de ser aprovado. Esta seção deve incluir:
>
> | Item | Obrigatório | Exemplo |
> |------|-------------|---------|
> | Ambientes listados | ✅ | `development`, `staging`, `production` |
> | Serviços por ambiente | ✅ | Supabase dev vs prod, Stripe test vs live |
> | Arquivos `.env` mapeados | ✅ | `.env.local` (dev), `.env.production` (prod) |
> | Credentials separadas | ✅ | Cada ambiente com projeto/chaves próprias |
> | Variáveis de ambiente listadas | ✅ | Tabela com TODAS as vars necessárias |
>
> **FALHA QUE GEROU ESTA REGRA:** Projeto Flyee chegou à Sprint 10 com `.env.local`
> apontando para Supabase **production**. Nenhuma fase exigiu separação de ambientes.
> Resultado: risco de corrupção/perda de dados de produção durante desenvolvimento.
>
> **Template mínimo para o TDD:**
> ```markdown
> ## Environment Strategy
>
> | Ambiente | Propósito | Supabase | Stripe | Outros |
> |----------|-----------|----------|--------|--------|
> | development | Desenvolvimento local | {projeto}-dev | sk_test_ | ... |
> | staging | Testes pré-deploy | {projeto}-stg | sk_test_ | ... |
> | production | Produção | {projeto}-prod | sk_live_ | ... |
>
> ### Arquivos de Configuração
> | Arquivo | Ambiente | Onde usa |
> |---------|----------|----------|
> | `.env.local` | development | `npm run dev` |
> | `.env.production` | production | Vercel/Deploy |
> | `.env.example` | template | Referência para novos devs |
> ```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir sem aprovação do TDD.

---

### Phase 2.1: NOTION SETUP + TRACKING DE FASES

> [!IMPORTANT]
> **Equivalente ao Phase 3.5 do `/legacy-project`.**
> Garante que o cliente vê progresso desde o início do planejamento.

> [!NOTE]
> **Pulado no modo --quick** (não há fases 2.5–2.9 para rastrear).

**Objetivo:** Criar tasks no Notion para TODAS as fases de planejamento (2.5–2.9), permitindo ao cliente acompanhar o progresso antes do breakdown de implementação.

**Trigger:**
```
TDD aprovado → Automático
```

**Agentes Envolvidos:**
- `orchestrator` - Integração Notion

> [!CAUTION]
> **SKILL OBRIGATÓRIA:** Seguir `notion-task-patterns` para criação de tasks.
> Ver seção "➕ CRIAR TASK (2 ETAPAS OBRIGATÓRIAS)" da skill.

#### Passo 1: Discovery da Database

```json
// Tool: mcp_notion-mcp-server_API-post-search
{
  "query": "{nome-do-projeto}",
  "filter": { "property": "object", "value": "data_source" }
}
```

> Se database não encontrada, seguir skill `notion-task-patterns` → "DATABASE SETUP".

#### Passo 2: Criar Tasks de Planejamento

Para CADA fase de planejamento, criar task com 2 etapas (propriedades + corpo):

| # | Task | Fase | Categoria |
|---|------|------|-----------|
| N+1 | Design System: UI/UX Discovery + MASTER.md | 2.5 | Planejamento |
| N+2 | Content Strategy: Copy e Conteúdo | 2.65 | Planejamento |
| N+3 | Stitch: Prototipação com IA | 2.7 | Prototipação |
| N+4 | Page Specs: Blueprint Detalhado | 2.8 | Planejamento |
| N+5 | Analytics Strategy: Tracking & Measurement | 2.9 | Planejamento |

> [!WARNING]
> **Tasks de implementação (Phase 4–7)** são criadas no Phase 3 (BREAKDOWN), quando o TDD
> é decomposto em tarefas granulares. Não antecipar estas tasks aqui.

#### Passo 3: Atualizar Status ao Executar Fases

À medida que cada fase de planejamento for concluída, atualizar a task correspondente:

```json
// Tool: mcp_notion-mcp-server_API-patch-page
{
  "page_id": "{page_id}",
  "properties": {
    "Status": { "status": { "name": "Concluído" } },
    "% Progresso": { "number": 100 }
  }
}
```

#### Passo 4: Relatório de Tasks Criadas

```markdown
📋 **NOTION SETUP CONCLUÍDO**

| # | Task | Fase | Status |
|---|------|------|--------|
| {id} | Design System | 2.5 | Não Iniciado |
| {id} | Content Strategy | 2.65 | Não Iniciado |
| {id} | Stitch | 2.7 | Não Iniciado |
| {id} | Page Specs | 2.8 | Não Iniciado |
| {id} | Analytics | 2.9 | Não Iniciado |

Total: {N} tasks de planejamento criadas
```

**Gate de Saída:**
```
[ ] Database descoberta/criada
[ ] Tasks de planejamento criadas (com corpo)
[ ] PROJECT-PROGRESS.md atualizado
```

---

### Phase 2.45: VISUAL REFERENCE COLLECTION (Pergunta Obrigatória)

> [!IMPORTANT]
> **OBRIGATÓRIO:** Antes de iniciar Phase 2.5, perguntar ao usuário COMO quer definir o Design System.

**Objetivo:** Determinar a abordagem de definição do Design System e coletar materiais de referência se necessário.

**Trigger:**
```
Notion Setup concluído → Automático (exceto --no-design)
```

---

#### Pergunta ao Usuário (OBRIGATÓRIA)

```markdown
## 🎨 Como deseja definir o Design System?

Antes de definir os tokens visuais (cores, tipografia, efeitos), preciso saber como você quer conduzir:

| Opção | Descrição |
|-------|-----------|
| **A) Recomendações + Perguntas** | Eu gero recomendações baseadas no contexto do projeto e te faço perguntas granulares por aspecto (cores, tipografia, layout, efeitos, logo) |
| **B) Referências Visuais** | Você fornece screenshots, URLs ou imagens de sites/apps que gosta e eu extraio os tokens visuais |
| **C) Definir Manualmente** | Você me informa diretamente os valores (hex das cores, nomes das fontes, estilo) |
| **D) Combinação** | Referências visuais + perguntas granulares para ajustar |

Qual opção?
```

**AGUARDAR** resposta do usuário.

---

#### Se Opção B ou D (Referências Visuais)

**Passo 1: Criar pasta de referências**

```powershell
# PowerShell (Windows)
New-Item -ItemType Directory -Force -Path "design-system/{nome}/references/"
```

```bash
# Bash (macOS/Linux)
mkdir -p design-system/{nome}/references/
```

**Passo 2: Orientar o usuário**

```markdown
## 📂 Pasta de Referências Criada

A pasta `design-system/{nome}/references/` foi criada no projeto.

### Como adicionar referências:

| Tipo | Como fazer |
|------|-----------|
| **Screenshots** | Salve imagens (.png, .jpg, .webp) diretamente na pasta |
| **URLs de sites** | Me informe as URLs e eu faço screenshots ou analiso |
| **Imagens de inspiração** | Arraste para a pasta ou cole aqui no chat |
| **Figma/Dribbble** | Me envie o link e eu extraio os tokens |

### Dicas para boas referências:
- Pode ser de **concorrentes**, de **produtos que admira**, ou qualquer design que transmita o "feeling" desejado
- Pode ser **parcial**: "Gosto SÓ das cores desse site" ou "Só o layout"
- **Quanto mais referências, melhor** eu entendo a direção visual

### Quando terminar:
Quando tiver adicionado todas as referências, me avise e eu analiso para extrair os tokens.
```

**AGUARDAR** o usuário adicionar referências e confirmar.

**Passo 3: Analisar referências**

1. Ler todas as imagens/URLs fornecidas
2. Extrair para cada referência:
   - Cores dominantes (hex exatos)
   - Tipografia identificada
   - Estilo de layout e espaçamento
   - Efeitos visuais (glassmorphism, shadows, gradients)
   - Direção visual geral
3. Consolidar em uma análise comparativa
4. Apresentar ao usuário para validação

---

#### Se Opção A (Recomendações + Perguntas)

Prosseguir diretamente para Phase 2.5 com o fluxo de recomendações.

#### Se Opção C (Manual)

Prosseguir para Phase 2.5 com perguntas diretas sobre cada token.

---

**Gate de Saída:**
```
[ ] Usuário respondeu como quer definir o Design System
[ ] Se referências visuais: pasta criada e materiais adicionados
[ ] Se referências visuais: análise apresentada ao usuário
```

---

### Phase 2.5: DESIGN SYSTEM - Tokens Visuais (Opcional para APIs)

> [!NOTE]
> **Pulado se:** Projeto é apenas API/Backend sem interface.
> **Skills de referência:** `frontend-design` ou `mobile-design`

> [!IMPORTANT]
> **SKILL OBRIGATÓRIA:** Seguir `ui-ux-discovery` para perguntas granulares ANTES de finalizar Design System.
> **WORKFLOW:** Executar `/ui-ux-pro-max` para obter recomendações profissionais.
> **REFERÊNCIAS:** Se Phase 2.45 coletou referências visuais, usá-las como base para as recomendações.

**Objetivo:** Definir os **tokens visuais globais** (DNA do projeto) com base na abordagem escolhida na Phase 2.45.

> [!NOTE]
> **MASTER.md contém APENAS tokens** (cores, tipografia, espaçamento, radius, shadows, efeitos, direção visual).
> **Specs de componentes** (buttons, cards, sidebar, etc.) são definidos como **task no Phase 3 (Breakdown)**.
> Os tokens DEVEM ser definidos primeiro porque os componentes os consomem.

**Trigger:**
```
Phase 2.45 concluída → Automático
```

**Agentes Envolvidos:**
- `frontend-specialist` - Para projetos web
- `mobile-developer` - Para projetos mobile
- `design-specialist` - Para projetos complexos

---

#### Processo por Abordagem

##### Se Abordagem A (Recomendações + Perguntas) ou D (Combinação)

> [!CAUTION]
> **OBRIGATÓRIO:** Seguir skill `ui-ux-discovery`.
> **NÃO** gerar Design System final sem respostas do usuário.

| Passo | Ação | Detalhes |
|-------|------|----------|
| 1 | Executar `/ui-ux-pro-max` | Obter recomendações modernas |
| 1.5 | Incorporar referências visuais (se D) | Combinar com recomendações |
| 2 | **Perguntas Granulares ⭐** | Por aspecto: cores, tipografia, layout, efeitos, logo |
| 3 | Aguardar Respostas | **BLOQUEADOR** - Não prosseguir sem resposta |
| 4 | Consolidar Decisões | Combinar escolhas do usuário + recomendações |
| 5 | Validar e Aprovar | Aguardar aprovação humana |

##### Se Abordagem B (Referências Visuais)

| Passo | Ação | Detalhes |
|-------|------|----------|
| 1 | Analisar referências | Extrair tokens de cada referência |
| 2 | Apresentar extração | Mostrar tokens extraídos por referência |
| 3 | **Perguntas de Ajuste ⭐** | "Gostou das cores do site X ou Y?" |
| 4 | Consolidar | Combinar preferências do usuário |
| 5 | Validar e Aprovar | Aguardar aprovação humana |

##### Se Abordagem C (Manual)

| Passo | Ação | Detalhes |
|-------|------|----------|
| 1 | Solicitar tokens | Pedir cores, fontes, estilo diretamente |
| 2 | Validar acessibilidade | Verificar contraste WCAG |
| 3 | Consolidar | Organizar valores fornecidos |
| 4 | Validar e Aprovar | Aguardar aprovação humana |

---

**PASSO 1 (Abordagem A/D): Executar `/ui-ux-pro-max` (OBRIGATÓRIO)**

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "{produto} {indústria} {keywords}" --design-system -p "{Projeto}"
```

**Exemplo para SaaS:**
```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "saas startup professional" --design-system -p "MeuProjeto"
```

**Output esperado:**
- Pattern recomendado (landing, dashboard, etc.)
- Style (glassmorphism, minimalism, etc.)
- Paleta de cores completa
- Tipografia (Google Fonts)
- Efeitos visuais
- Anti-patterns a evitar

---

**PASSO 2: Persistir Design System**

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "{query}" --design-system --persist -p "{Projeto}"
```

Gera:
- `design-system/MASTER.md` - Source of Truth global
- `design-system/pages/` - Folder para overrides por página

---

**PASSO 3: Buscar Guidelines do Stack**

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack {stack}
```

Stacks disponíveis: `html-tailwind`, `react`, `nextjs`, `shadcn`, `vue`, `swiftui`, `react-native`, `flutter`, etc.

---

**PASSO 4: Documentar Design System (Tokens)**

1. Analisar TDD para requisitos visuais
2. Combinar recomendações / referências / manual com requisitos do TDD
3. Definir tokens:
   - Paleta de cores
   - Tipografia
   - Espaçamento (spacing scale)
   - Border radius
   - Shadows
   - Efeitos visuais
4. Gerar `design-system/{nome}/MASTER.md`
5. **AGUARDAR** aprovação humana

**Template MASTER.md (Tokens Only):**
```markdown
## design-system/{nome}/MASTER.md

> Gerado em {data}
> Abordagem: {A/B/C/D}
> Referências: {lista de referências se houver}

### Direção Visual
- Pattern: {landing, dashboard, etc.}
- Style: {estilo escolhido}

### Cores
- Primary: {hex}
- Secondary: {hex}
- Accent: {hex}
- Background: {hex}
- Surface: {hex}
- Text: {hex}
- Text Muted: {hex}
- Border: {hex}
- Error: {hex}
- Success: {hex}
- Warning: {hex}

### Tipografia
- Heading: {fonte} (Google Fonts)
- Body: {fonte} (Google Fonts)
- Mono: {fonte para código}
- Scale: {ratio, ex: 1.25}

### Espaçamento
- Base: {ex: 8px}
- Scale: {ex: 4, 8, 12, 16, 24, 32, 48, 64, 96}

### Border Radius
- Small: {ex: 4px}
- Medium: {ex: 8px}
- Large: {ex: 12px}
- Full: {ex: 9999px}

### Shadows
- Level 1: {ex: 0 1px 3px rgba(0,0,0,0.12)}
- Level 2: {value}
- Level 3: {value}

### Efeitos Visuais
- {lista de efeitos: glassmorphism, gradients, dark mode, etc.}

### Anti-Patterns (EVITAR)
- {lista}

### Referências Visuais (se houver)
- ![ref_001](./references/{arquivo})
- {descrição do que foi extraído de cada referência}
```

> [!NOTE]
> **Specs de componentes** (Buttons, Cards, Sidebar, Forms, etc.) serão definidos
> como **task dedicada no Phase 3 (Breakdown)**, consumindo estes tokens.
> O workflow `/atomic` será usado na Phase 5 para implementar cada componente.

---

**Gate de Saída:**
```
[ ] Abordagem escolhida na Phase 2.45 seguida
[ ] Perguntas granulares respondidas pelo usuário (skill: ui-ux-discovery)
[ ] Se referências: analisadas e incorporadas
[ ] Design System (tokens) persistido (design-system/{nome}/MASTER.md)
[ ] Design System aprovado pelo humano
```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir sem aprovação do Design System.

---

### Phase 2.65: CONTENT STRATEGY - Conteúdo e Copy

> [!NOTE]
> **Pulado se:** Projeto é apenas API/Backend sem interface pública.
> **Obrigatório para:** LPs, sites institucionais, SaaS com marketing pages.

> [!IMPORTANT]
> **SKILL:** Seguir `content-strategy` para definição de copy e conteúdo.
> **Documento:** `docs/content/CONTENT-STRATEGY-{nome}.md`

**Objetivo:** Definir copy e conteúdo ANTES de prototipar, para que Stitch use textos reais.

**Trigger:**
```
Design System aprovado → Automático (exceto --no-content)
```

**Agentes Envolvidos:**
- `frontend-specialist` - Estrutura de páginas
- `product-owner` - Messaging e posicionamento

---

#### Processo (Skill: content-strategy)

> [!CAUTION]
> **OBRIGATÓRIO:** Seguir TODOS os 4 passos definidos na skill `content-strategy`.
> **NÃO** prosseguir sem respostas do usuário sobre tom de voz e proposta de valor.

| Passo | Ação | Detalhes |
|-------|------|----------|
| 1 | Identificar Páginas | Listar todas as páginas que precisam de conteúdo |
| 2 | **Perguntas ao Usuário ⭐** | Tom de voz, público, USP, pricing |
| 3 | Gerar Documento | Hero, Features, FAQ, SEO metadata |
| 4 | Validar e Aprovar | Aguardar aprovação humana |

**Gate de Saída:**
```
[ ] CONTENT-STRATEGY-{nome}.md gerado
[ ] Copy da LP definido (Hero, Features, CTA)
[ ] Pricing/FAQ definidos (se aplicável)
[ ] Metadados SEO definidos
[ ] Conteúdo aprovado pelo humano
```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir para Phase 2.7 (Stitch) sem Content Strategy aprovado (exceto --no-content).

---

### Phase 2.7: STITCH GENERATION - UI com IA (Opcional)

> [!NOTE]
> **Ativado com:** `/new-project --stitch` OU quando usuário responder "Sim" na pergunta abaixo.
> **Pulado se:** UI será desenhada manualmente (Figma) ou projeto não visual.

> [!TIP]
> **Workflow relacionado:** `/stitch` (contém todas as flags e skills)
> **Skills usadas:** `design-md`, `enhance-prompt`, `react-components`, `stitch-loop`

**Objetivo:** Usar IA (Stitch) para gerar screens e componentes base, usando o copy real do Content Strategy.

**Trigger:**
```
Content Strategy aprovado → Perguntar ao usuário
```

**Agentes Envolvidos:**
- `stitch-designer` - Especialista em geração de UI com Stitch
- `frontend-specialist` - Validação e integração

---

#### Pergunta ao Usuário (OBRIGATÓRIA)

```markdown
## 🎨 Geração de UI com IA

O Content Strategy está definido. Deseja usar **Stitch AI** para acelerar a criação da UI?

| Opção | Descrição |
|-------|-----------|
| **Sim, completo** | Gerar todas as telas principais com Stitch loop |
| **Sim, parcial** | Apenas otimizar prompts e gerar DESIGN.md semântico |
| **Não** | Implementar manualmente (pular para Phase 2.8) |

Qual opção?
```

---

#### Processo Completo (Se "Sim, completo")

| Passo | Skill | Ação | Output |
|-------|-------|------|--------|
| 1 | `enhance-prompt` | Otimizar descrições de cada tela | Prompts otimizados |
| 2 | `design-md` | Gerar DESIGN.md semântico | `DESIGN.md` |
| 3 | `stitch-loop` | Gerar screens com Stitch MCP | HTML + Screenshots |
| 4 | `react-components` | Converter para React | Componentes prontos |

**PASSO 1: Otimizar Prompts (`/stitch --prompt`)**

```markdown
# Para cada tela principal do TDD:

## Tela: {nome}

**Descrição original:** {descrição do TDD}

**Prompt otimizado:** {gerado pela skill enhance-prompt}
- Adicionados: keywords de UI/UX, contexto de design system
- Estrutura: layout, componentes, estados
```

**PASSO 2: Gerar DESIGN.md Semântico (`/stitch --design`)**

Converte `design-system/MASTER.md` (humano) → `DESIGN.md` (otimizado para IA):

```bash
# A skill design-md lê o MASTER.md e gera versão semântica
# Output: DESIGN.md na raiz do projeto
```

**PASSO 3: Gerar Screens com Stitch (Se Stitch MCP disponível)**

> [!IMPORTANT]
> **VERIFICAÇÃO OBRIGATÓRIA:** Antes de prosseguir, verificar se Stitch MCP está configurado.

#### 3.1 Verificar Stitch MCP

```bash
# Verificar se stitch-mcp está nos MCP servers configurados
# O agente deve verificar os MCP Servers disponíveis
```

**Se Stitch MCP NÃO estiver disponível, perguntar:**

```markdown
## ⚠️ Stitch MCP não detectado

O Stitch MCP Server não está configurado. Para usar a geração de UI com IA:

### Opções:

| Opção | Ação |
|-------|------|
| **A. Configurar agora** | Vou guiar a instalação do Stitch MCP |
| **B. Pular** | Continuar sem Stitch (usar apenas skills offline) |
| **C. Já configurei** | Tentar detectar novamente |

Qual opção?
```

#### 3.2 Se Opção A (Configurar Stitch MCP)

```markdown
## 🔧 Configuração do Stitch MCP

### Passo 1: Conta no Stitch
1. Acesse: https://stitch.withgoogle.com/
2. Faça login com sua conta Google
3. Crie um projeto (ou use existente)

### Passo 2: Obter Token
1. No Stitch, vá em Settings → API
2. Gere um token de API
3. Copie o token

### Passo 3: Configurar MCP Server
Adicione ao seu arquivo de configuração MCP:

**Claude Desktop (~/.claude/claude_desktop_config.json):**
\`\`\`json
{
  "mcpServers": {
    "stitch": {
      "command": "npx",
      "args": ["-y", "@anthropic/stitch-mcp"],
      "env": {
        "STITCH_API_KEY": "seu-token-aqui"
      }
    }
  }
}
\`\`\`

### Passo 4: Reiniciar
1. Feche completamente o Claude Desktop
2. Reabra
3. Responda "C. Já configurei" para verificar

**Precisa de ajuda?** Responda "ajuda stitch" para mais detalhes.
```

#### 3.3 Se Stitch MCP disponível (ou Opção C confirmada)

```markdown
# Seguir skill stitch-loop:
1. Criar SITE.md com visão do projeto
2. Criar next-prompt.md (baton) com primeira tela
3. Executar loop de geração
4. Integrar screens ao projeto
```

#### 3.4 Se Opção B (Pular)

> [!NOTE]
> Stitch MCP pulado. Usar apenas skills offline (`design-md`, `enhance-prompt`, `react-components`).
> Screens serão implementadas manualmente na Phase 5.

**PASSO 4: Converter para React (`/stitch --components`)**

```bash
# Usar skill react-components para converter HTML gerado
# Aplicar design tokens do MASTER.md
# Validar com scripts da skill
```

---

#### Processo Parcial (Se "Sim, parcial")

Apenas executar PASSO 1 e PASSO 2 (otimizar prompts e gerar DESIGN.md).
Screens serão implementadas manualmente na Phase 5.

---

**Gate de Saída:**
```
[ ] Usuário escolheu opção (completo/parcial/não)
[ ] Se completo/parcial: Prompts otimizados para telas principais
[ ] Se completo/parcial: DESIGN.md gerado
[ ] Se completo: Screens geradas (ou justificativa para pular)
[ ] Se completo: Componentes React extraídos
```

---

#### 🚨 GATE DE VALIDAÇÃO DO CLIENTE (OBRIGATÓRIO) ⭐

> [!CAUTION]
> **REGRA BLOQUEANTE:** Após gerar protótipos, o CLIENTE deve validar CADA tela via Notion.
> NÃO prosseguir para Phase 2.8 (Page Specs) sem TODAS as tasks de prototipação com Status = "Concluído".

> [!IMPORTANT]
> **REGRA:** 1 TASK POR TELA. Não criar task única para múltiplas telas.
> Seguir skill `notion-task-patterns` seção "Template: PROTOTIPAÇÃO".

**Processo (para CADA tela gerada):**

| Passo | Ação | Detalhes |
|-------|------|----------|
| 1 | Criar Task no Notion | Categoria: `Prototipação`, Status: `Em andamento` |
| 2 | Adicionar Preview | Screenshot/link do protótipo no corpo da task |
| 3 | Mudar Status | `Aguardando Aprovação` |
| 4 | Notificar Cliente | Comentário no Notion (template na skill) |
| 5 | Aguardar | Cliente revisa e marca `Concluído` ou deixa feedback |

**Fluxo de Status:**
```
Não iniciado → Em andamento → Aguardando Aprovação → Concluído
                                    ↑                    ↓
                            CLIENTE VALIDA          → Dev
```

**Checklists para cada tela:**

```markdown
## Tasks de Prototipação (1 por tela)
- [ ] Task #X: Header (Desktop) → Status: Aguardando Aprovação
- [ ] Task #Y: Header (Mobile) → Status: Aguardando Aprovação
- [ ] Task #Z: Hero Section → Status: Aguardando Aprovação
- [ ] Task #W: Footer → Status: Aguardando Aprovação
...
```

**Query para verificar aprovações pendentes:**

```json
// Tool: mcp_notion-mcp-server_API-query-data-source
{
  "data_source_id": "{DATABASE_ID}",
  "filter": {
    "and": [
      { "property": "Categoria", "multi_select": { "contains": "Prototipação" } },
      { "property": "Status", "status": { "does_not_equal": "Concluído" } }
    ]
  }
}
```

**Se houver tasks não concluídas → PARAR e aguardar:**

```markdown
⏳ **AGUARDANDO VALIDAÇÃO DO CLIENTE**

📋 {N} protótipo(s) pendente(s) de aprovação:

| ID | Tela | Status |
|----|------|--------|
| #{id} | {nome} | Aguardando Aprovação |

👤 **Ação do Cliente:** 
- 🟢 **Aprovar:** Marcar status como "Concluído"
- 🔴 **Recusar:** Marcar status como "Recusado" + comentário com feedback
```

---

#### Tratamento de Recusa

> [!IMPORTANT]
> **Se Status = "Recusado":** Agente deve analisar comentários e ajustar.

**Processo de Ajuste:**

| Passo | Ação |
|-------|------|
| 1 | Buscar comentários da task recusada |
| 2 | Analisar feedback do cliente |
| 3 | Ajustar protótipo conforme solicitado |
| 4 | Atualizar preview na task |
| 5 | Mudar Status → "Aguardando Aprovação" |
| 6 | Adicionar comentário notificando cliente |

**Query para detectar tasks recusadas:**

```json
// Tool: mcp_notion-mcp-server_API-query-data-source
{
  "data_source_id": "{DATABASE_ID}",
  "filter": {
    "and": [
      { "property": "Categoria", "multi_select": { "contains": "Prototipação" } },
      { "property": "Status", "status": { "equals": "Recusado" } }
    ]
  }
}
```

**Buscar comentários para entender feedback:**

```json
// Tool: mcp_notion-mcp-server_API-retrieve-a-comment
{
  "block_id": "{page_id}"
}
```

**Após ajustar, notificar cliente:**

```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{page_id}" },
  "rich_text": [{
    "text": {
      "content": "🔄 **Protótipo ajustado conforme feedback**\n\n📋 Alterações realizadas:\n- {item 1}\n- {item 2}\n\n📸 Novo preview atualizado acima.\n\n👤 Por favor, revise novamente."
    }
  }]
}

---

### Phase 2.8: PAGE SPECIFICATIONS - Blueprint Detalhado

> [!NOTE]
> **Pulado se:** Projeto é apenas API/Backend sem interface.
> **Obrigatório para:** Qualquer projeto com UI (Web, Mobile, Dashboard).

> [!IMPORTANT]
> **SKILL:** Seguir `page-specifications` para detalhamento de páginas.
> **Documento Principal:** `design-system/{nome}/layout/SHARED-LAYOUT.md`
> **Docs por Página:** `design-system/{nome}/pages/PAGE-SPEC-*.md`

**Objetivo:** Criar blueprint detalhado de CADA página antes do Breakdown.

**Trigger:**
```
Content Strategy aprovado → Automático (exceto --no-specs)
```

**Agentes Envolvidos:**
- `frontend-specialist` - Layout e componentes
- `design-specialist` - Visual specs
- `product-owner` - Validação de fluxos

---

#### Processo (Skill: page-specifications)

> [!CAUTION]
> **OBRIGATÓRIO:** Seguir TODOS os 5 passos definidos na skill `page-specifications`.
> **NÃO** prosseguir sem PAGE-SPECs aprovados pelo usuário.

| Passo | Ação | Detalhes |
|-------|------|----------|
| 1 | Identificar Páginas | Listar todas baseado em PRD/TDD/Content |
| 2 | Criar SHARED-LAYOUT.md | Header, Footer, Mobile Menu |
| 3 | **Perguntar Priorização ⭐** | Quais páginas detalhar agora vs V2 |
| 4 | Gerar PAGE-SPECs | Para cada página priorizada |
| 5 | Validar e Aprovar | Aguardar aprovação humana |

---

#### PASSO 1: Identificar Páginas

Categorizar por prioridade:

```markdown
## Páginas Identificadas

### Alta Prioridade (MVP)
- [ ] Landing Page (/)
- [ ] Pricing (/pricing)
- [ ] Start/Wizard (/start)
- [ ] Dashboard (/dashboard)

### Média Prioridade
- [ ] How it Works (/how-it-works)
- [ ] Workflows Library (/workflows)
- [ ] Video Pages (/videos/[slug])

### Baixa Prioridade (V2)
- [ ] Community (/community)
- [ ] Blog (/blog)

### Interna
- [ ] Admin (/admin)
```

---

#### PASSO 2: Criar SHARED-LAYOUT.md

> [!IMPORTANT]
> **CRIAR PRIMEIRO:** Antes de qualquer PAGE-SPEC individual.
> Define elementos compartilhados (Header, Footer, Mobile Menu).

**Output:** `design-system/{nome}/layout/SHARED-LAYOUT.md`

**Conteúdo mínimo:**
- Header (Navbar): Position, elementos, estados
- Footer: Links, social, visual
- Mobile Menu: Overlay, animação

---

#### PASSO 3-4: Gerar PAGE-SPECs

Para cada página priorizada, criar `PAGE-SPEC-{Página}.md` com:

| Seção | Conteúdo |
|-------|----------|
| **Layout & Estrutura** | Sections, referência ao SHARED-LAYOUT |
| **Conteúdo por Seção** | Copy, Visual, Estados (loading, empty, error) |
| **Responsividade** | Desktop, Tablet, Mobile adaptations |
| **Integrações** | Auth, CMS, Analytics, Payments |
| **SEO & Performance** | Title, Meta, OG Image, Loading strategy |

---

**Gate de Saída:**
```
[ ] SHARED-LAYOUT.md criado (Header, Footer, Mobile Menu)
[ ] Priorização de páginas confirmada com usuário
[ ] PAGE-SPEC criado para cada página priorizada
[ ] Cada PAGE-SPEC referencia MASTER.md e CONTENT-STRATEGY
[ ] Estados (loading, empty, error) documentados
[ ] Responsividade descrita para cada página
[ ] Todas as PAGE-SPECs aprovadas pelo humano
```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir para Breakdown sem PAGE-SPECs aprovados.

---

### Phase 2.9: ANALYTICS STRATEGY - Tracking & Measurement

> [!NOTE]
> **Pulado se:** Projeto é apenas POC interno sem necessidade de métricas.
> **Obrigatório para:** Qualquer produto que precisa medir conversão, engajamento ou retenção.

> [!IMPORTANT]
> **Output:** Seção `## 📊 Analytics` em cada PAGE-SPEC + config no TDD.
> **Ferramentas:** PostHog (padrão), Google Search Console, UTM Tracking.

**Objetivo:** Definir O QUE medir, ONDE medir, e COMO medir antes de implementar.

**Trigger:**
```
PAGE-SPECs aprovados → Automático (exceto --no-analytics)
```

**Agentes Envolvidos:**
- `frontend-specialist` - Eventos de UI
- `product-owner` - Métricas de negócio
- `growth-specialist` - Funnels e conversão

---

#### Processo (5 Passos)

| Passo | Ação | Detalhes |
|-------|------|----------|
| 1 | Definir Stack | PostHog + Search Console + UTMs (padrão) |
| 2 | Mapear Eventos por Página | Baseado nas PAGE-SPECs |
| 3 | Definir Funnels | Conversão principal + secundários |
| 4 | Definir Feature Flags | Para A/B testing |
| 5 | Documentar no TDD + PAGE-SPECs | Seção Analytics em cada doc |

---

#### PASSO 1: Definir Stack de Analytics

```markdown
## Stack de Analytics

| Ferramenta | Propósito | Fase |
|------------|-----------|------|
| **PostHog** | Product Analytics, Session Replay, Feature Flags, Funnels | MVP |
| **Google Search Console** | SEO: indexação, keywords, CTR | MVP |
| **UTM Tracking** | Atribuição de campanhas (capturado pelo PostHog) | MVP |
| **Google Tag Manager** | Gerenciamento centralizado de tags | Growth |
| **Meta Pixel** | Facebook/Instagram Ads, Remarketing | Quando anunciar |
| **Google Ads Tag** | Google Ads conversions | Quando anunciar |
```

---

#### PASSO 2: Mapear Eventos por Página

Para **CADA** PAGE-SPEC, adicionar seção:

```markdown
## 📊 Analytics (PostHog)

### Eventos Customizados
| Evento | Trigger | Properties |
|--------|---------|------------|
| `page_name_viewed` | Pageview | `referrer`, `utm_*` |
| `cta_clicked` | Click CTA | `cta_type`, `section` |
| ... | ... | ... |

### Funis a Medir
- Funnel 1: ...
- Funnel 2: ...

### Feature Flags (A/B)
- `flag_name`: Descrição do teste
```

---

#### PASSO 3: Perguntar ao Usuário (OBRIGATÓRIO)

```markdown
## 📊 Estratégia de Analytics

Para definir o tracking do projeto, preciso saber:

### 1. Métricas de Sucesso
Quais são as **3 principais métricas** que você quer acompanhar?
- [ ] Conversão de visitante → signup
- [ ] Conversão de free → pago
- [ ] Engajamento (tempo na plataforma)
- [ ] Retenção (retorno em 7 dias)
- [ ] Feature adoption (uso de funcionalidades)
- [ ] Outra: ___

### 2. Paid Acquisition
Você planeja fazer **ads pagos** (Meta, Google)?
- [ ] Sim, em breve → Configurar pixels
- [ ] Não por agora → Pular pixels
- [ ] Não sei ainda → Deixar preparado mas não ativar

### 3. A/B Testing
Quais elementos você quer testar?
- [ ] CTAs (texto, cor)
- [ ] Pricing page (ordem dos planos)
- [ ] Onboarding flow
- [ ] Nenhum por agora
```

---

#### PASSO 4: Atualizar TDD

Adicionar/atualizar seção `## 📈 Analytics & Tracking Strategy` no TDD com:
- Stack de ferramentas
- Eventos por página
- Variáveis de ambiente necessárias

---

#### PASSO 5: Atualizar PAGE-SPECs

Para cada PAGE-SPEC priorizada, adicionar seção `## 📊 Analytics (PostHog)` com:
- Eventos customizados
- Funis a medir
- Feature flags para A/B

---

**Gate de Saída:**
```
[ ] Stack de Analytics definida no TDD
[ ] Eventos mapeados para cada PAGE-SPEC
[ ] Variáveis de ambiente listadas no TDD
[ ] Usuário confirmou métricas de sucesso
[ ] PAGE-SPECs atualizadas com seção Analytics
```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir para Breakdown sem Analytics Strategy definida.

---

### Phase 3: BREAKDOWN - Tarefas

**Objetivo:** Quebrar TDD **E PAGE-SPECs** em tarefas de **implementação** executáveis.

> [!NOTE]
> **Tasks de planejamento** (Design System, Content, Stitch, Page Specs, Analytics)
> já foram criadas na Phase 2.1. Esta fase cria tasks de **implementação** granulares.

**Trigger:**
```
TDD aprovado → Automático
```

**Agentes Envolvidos:**
- `project-planner` - Quebra em tarefas

> [!IMPORTANT]
> **GATE PRÉ-BREAKDOWN: ESCOLHA DE TRACKING**
> 
> Antes de criar qualquer task, o agente DEVE verificar em `PROJECT-PROGRESS.md`
> se a configuração `Tracker de Tasks` está definida.
> Se não estiver, **NÃO PROSSEGUIR** sem perguntar:
> 
> *“Como você deseja registrar e acompanhar as tarefas de implementação?”*
> 1. *Notion (Padrão, dashboard visual)*
> 2. *Local (Arquivo `docs/TASKS.md` com checkboxes)*
> 
> Salvar a escolha em `PROJECT-PROGRESS.md` na seção Configurações.

> [!CAUTION]
> **REGRAS POR MODO DE TRACKING:**
> 
> **Se Modo = Notion:**
> - SKILL OBRIGATÓRIA: Seguir `notion-task-patterns`.
> - Cada task requer 2 etapas API: `API-post-page` + `API-patch-block-children` com template.
> - Task sem corpo = task INCOMPLETA.
> 
> **Se Modo = Local (`docs/TASKS.md`):**
> - Criar/editar o arquivo `docs/TASKS.md`
> - Agrupar tasks por Épico ou Página, usando Markdown com checkboxes (`- [ ]`)
> - Exemplo: `## Landing Page\n- [ ] Criar Hero com Video BG`

**Ações:**
1. Verificar configuração `Tracker de Tasks` (Perguntar se não existir).
2. Executar `/tdd breakdown docs/design/TDD-{nome}.md`
3. Gerar planejamento de tasks em memória.
4. **Verificar Cobertura PAGE-SPEC (OBRIGATÓRIO):**
   - Listar todos `design-system/{projeto}/pages/PAGE-SPEC-*.md`
   - Para CADA PAGE-SPEC, garantir pelo menos 1 task correspondente
5. Executar a gravação das tasks baseada no Tracker escolhido:
   - **Caso Notion**: seguir fluxo de 2 etapas da skill `notion-task-patterns`.
   - **Caso Local**: usar `write_to_file` ou `multi_replace_file_content` para popular `docs/TASKS.md`.
6. Verificar gate de saída.

**Gate de Saída (OBRIGATÓRIO):**
```
[ ] Escolha do Tracker de Tasks feita e salva
[ ] Se Notion: Todas tasks com propriedades + corpo criados
[ ] Se Local: Arquivo docs/TASKS.md gerado com checkboxes
[ ] **CADA PAGE-SPEC tem pelo menos 1 task correspondente** ⭐
```

**Output:**
```
Tasks criadas ({Modo Escolhido}):
- [x] Task 1: Setup Infraestrutura → (Registrada)
- [x] Task 2: Entidades principais → (Registrada)
...
```


---

### Phase 3.5: SETUP BASE - Infraestrutura

> [!CAUTION]
> **REGRA BLOQUEANTE:** NÃO iniciar Phase 4 (TDD) sem infraestrutura configurada.
> Não é possível escrever testes sem projeto inicializado.

**Objetivo:** Preparar infraestrutura base antes de escrever testes.

**Trigger:**
```
Breakdown concluído → Automático
```

**Agentes Envolvidos:**
- `devops-engineer` - Setup inicial
- `app-builder` - Inicialização do projeto

**Ações para Projeto NOVO (sem código):**

1. **Inicializar Projeto:**
   ```bash
   # Web (Next.js)
   npx -y create-next-app@latest ./ --typescript --tailwind --app --src-dir --import-alias "@/*"
   
   # Mobile (React Native)
   npx react-native init {NomeProjeto} --template react-native-template-typescript
   ```

2. **Configurar Test Runner:**
   ```bash
   # Next.js / React
   npm install -D vitest @testing-library/react @testing-library/dom jsdom @vitejs/plugin-react
   ```

3. **Criar Estrutura Base:**
   ```
   src/
   ├── app/           # Rotas (Next.js)
   ├── components/    # Componentes UI
   ├── lib/           # Lógica de negócio
   ├── tests/         # Testes
   └── types/         # TypeScript types
   ```

4. **Configurar vitest.config.ts:**
   ```typescript
   import { defineConfig } from 'vitest/config';
   import react from '@vitejs/plugin-react';
   
   export default defineConfig({
     plugins: [react()],
     test: {
       environment: 'jsdom',
       globals: true,
     },
   });
   ```

5. **Verificar Setup:**
   ```bash
   npm test -- --run  # Deve rodar sem erros (0 tests ok)
   ```

6. **🔴 Configurar Separação de Ambientes (OBRIGATÓRIO):**

   > [!CAUTION]
   > **REGRA BLOQUEANTE:** NÃO prosseguir sem ambientes separados.
   > `.env.local` NUNCA deve conter credenciais de produção.
   >
   > **FALHA QUE GEROU ESTA REGRA:** Projeto Flyee desenvolvido por 10 sprints
   > com `.env.local` apontando para Supabase production. Risco de corrupção de dados reais.

   **6.1 Criar projetos separados para cada serviço externo:**

   | Serviço | Ambiente Dev | Ambiente Prod |
   |---------|-------------|---------------|
   | Supabase | `{nome}-dev` (novo projeto) | `{nome}` (existente) |
   | Stripe | `sk_test_` / `pk_test_` | `sk_live_` / `pk_live_` |
   | PostHog | Mesmo projeto, flag `DEV` | Mesmo projeto |
   | Sanity | `development` dataset | `production` dataset |
   | Resend | Mesmo (test mode) | Mesmo (prod mode) |

   **6.2 Criar arquivos `.env`:**

   ```bash
   # .env.example — Template com placeholders (commitado no git)
   # .env.local — Credenciais DEV (gitignored)
   # .env.production — Credenciais PROD (definidas na plataforma de deploy, NÃO no repo)
   ```

   **6.3 Validar que `.env.local` NÃO contém credenciais de produção:**

   ```markdown
   ⚠️ ENVIRONMENT VALIDATION GATE

   [ ] `.env.example` existe com placeholders genéricos
   [ ] `.env.local` existe com credenciais de DEVELOPMENT
   [ ] `.env.local` NÃO aponta para projetos de produção
   [ ] `.gitignore` inclui `.env.local` e `.env.production`
   [ ] Variáveis de produção serão configuradas APENAS na plataforma de deploy (Vercel)

   ❌ Se `.env.local` tiver URLs/keys de produção → PARAR e corrigir
   ✅ Todos OK → Prosseguir
   ```

   **6.4 Perguntar ao usuário (se projetos dev não existem):**

   ```markdown
   ## 🔐 Separação de Ambientes

   Para garantir segurança, preciso de credenciais de **DESENVOLVIMENTO** (não produção).

   | Serviço | Ação Necessária |
   |---------|----------------|
   | **Supabase** | Criar projeto `{nome}-dev` no dashboard Supabase |
   | **Stripe** | Usar chaves `test` (já disponíveis no dashboard) |
   | **Sanity** | Criar dataset `development` (Settings → Datasets) |

   Quando tiver as credenciais dev, me informe para configurar o `.env.local`.
   ```

**Ações para Projeto EXISTENTE (já tem código):**

1. Verificar se test runner existe
2. Se não existir, instalar (passo 2 acima)
3. Verificar estrutura de pastas
4. **🔴 Verificar separação de ambientes (passo 6 acima)**
5. Prosseguir para Phase 4

#### 🚨 SYNC DE SETUP (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA DE OURO:** O agente **não pode** concluir esta fase sem sincronizar cada task técnica no Notion (Status="Concluído", Progresso=100%).
>
> **Protocolo:**
> 1. Buscar ID da task (ex: #1, #2, #3, #4)
> 2. Atualizar Notion (Status=Concluído, %100, Tempo)
> 3. Adicionar comentário e atualizar arquivos locais

**Gate de Saída:**
```
[ ] Projeto inicializado (package.json existe)
[ ] Test runner configurado (vitest/jest)
[ ] Estrutura de pastas criada
[ ] npm test roda sem erros
[ ] **Ambientes separados (dev ≠ prod)** ⭐
[ ] **`.env.local` com credenciais de DEVELOPMENT apenas** ⭐
[ ] **`.env.example` com placeholders genéricos** ⭐
```

> [!TIP]
> Se projeto já existe e tem tests configurados, esta fase é automática (verificação apenas).

---

### Phase 4: TDD METODOLOGIA - Testes Primeiro

**Objetivo:** Escrever testes ANTES do código.

**Trigger:**
```
Breakdown concluído → Automático
```

**Skill de Referência:** `tdd-workflow`

> [!IMPORTANT]
> **Para componentes com UI:** Seguir skill `design-system-enforcement` durante GREEN.
> Componentes devem usar MASTER.md desde a criação, não apenas na fase de styling.

> [!CAUTION]
> **REGRA DE STYLING INLINE (OBRIGATÓRIO):**
> Todo componente UI criado na fase GREEN **DEVE já sair com o styling premium final**
> (glassmorphism, gradientes, glows, backdrop-blur, micro-animações) conforme MASTER.md.
> **NÃO é aceitável** criar um "esqueleto funcional" para estilizar depois.
> Phase 5.3 é apenas para **validação e ajustes finos**, não para aplicar estilo do zero.
>
> **FALHA QUE GEROU ESTA REGRA:** Pricing Page foi criada com estilos básicos (cores
> sólidas, sem glassmorphism, sem animações) durante TDD GREEN. Resultado: retrabalho
> completo de 5 arquivos CSS na Phase 5.3 para atingir o nível premium da Landing Page.

**Agentes Envolvidos:**
- `test-engineer` - Geração de testes
- Especialistas de domínio conforme task

**Ciclo para CADA Task:**

| Fase | Ação | Verificação |
|------|------|-------------|
| 🔴 RED | `/test [task]` - Escrever teste que falha | Teste falha corretamente |
| 📖 SPEC | **Ler specs de UI** (ver gate abaixo) | Checklist preenchido |
| 🟢 GREEN | Implementar código **com styling premium final** (Design System + efeitos visuais) | Teste passa + visual premium |
| 🔵 REFACTOR | Melhorar código | Testes continuam passando |

#### 🚨 UI SPEC READING GATE (OBRIGATÓRIO para tasks com UI)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de escrever código UI (GREEN phase), o agente DEVE ler
> TODAS as specs aplicáveis. NÃO implementar com base em inferência ou memória.
>
> **FALHA QUE GEROU ESTA REGRA:** Landing Page desenvolvida sem consultar SHARED-LAYOUT.md.
> Header implementado sem scroll shadow, search, github, language, theme e login icons.
> Footer implementado com 3 colunas em vez de 4.
> Mobile menu implementado como dropdown inline em vez de slide-in sheet.
> Resultado: retrabalho completo de Header e Footer.

**Checklist OBRIGATÓRIO antes do GREEN (se task envolve UI):**

```markdown
⚠️ UI SPEC READING GATE — Task: {título}

[ ] MASTER.md lido — seção Cores (tokens CSS)
[ ] MASTER.md lido — seção Tipografia
[ ] MASTER.md lido — seção Efeitos Visuais (glassmorphism, shadows, micro-animations) ⭐
[ ] MASTER.md lido — seção Componentes (se criando button, input, card, etc.)
[ ] SHARED-LAYOUT.md lido (se componente é Header, Footer, Mobile Menu, ou layout compartilhado)
[ ] PAGE-SPEC-{página}.md lido (se implementando seção de uma página específica)
[ ] Elementos obrigatórios identificados (lista extraída do spec)
[ ] Responsividade/breakpoints anotados

❌ Se QUALQUER item aplicável desmarcado → NÃO IMPLEMENTAR
✅ TODOS marcados → Prosseguir com GREEN
```

> [!CAUTION]
> **FALHA QUE GEROU ESTA EXPANSÃO (v2):** Dashboard UI foi criado com cores sólidas
> (`var(--color-bg-secondary)`) sem aplicar glassmorphism (`backdrop-filter: blur(16px)`,
> `var(--color-overlay-*)`) definido na seção "Efeitos Visuais" do MASTER.md.
> O agente leu MASTER.md mas focou apenas nos tokens (cores, tipografia), ignorando
> a seção de efeitos visuais. Resultado: dashboard visualmente plano, sem a estética
> premium "Technical Glassmorphism" das referências SphereUI.
>
> **FIX:** O checklist agora lista CADA seção do MASTER.md separadamente,
> com destaque ⭐ para Efeitos Visuais que é o mais esquecido.

#### 🖼️ REFERENCE ANALYSIS GATE (Se referências visuais existem)

> [!CAUTION]
> **FALHA QUE GEROU ESTA REGRA (v3):** Dashboard Sidebar e TopBar foram implementados
> como "floating pills" com `border-radius: 32px` descolados das bordas da viewport,
> quando as referências SphereUI (`sphereui_13.jpg`, `sphereui_15.jpg`) mostravam
> claramente componentes **edge-to-edge** (sidebar colada à borda esquerda, topbar como
> faixa horizontal contínua no topo do conteúdo).
> O agente "olhou" as referências mas não fez análise estrutural — inferiu layout
> "premium" baseado em suposições genéricas em vez de observar a anatomia real.
>
> **FIX:** Antes de implementar qualquer componente de layout, o agente DEVE produzir
> uma análise textual da anatomia espacial vista nas referências.

**ANTES de escrever CSS para layout (sidebar, topbar, shell, drawer), produzir:**

```markdown
## 📐 Análise Espacial — {Componente} (ref: {arquivo_referencia})

### O que eu VEJO na referência:
- Sidebar: [edge-to-edge left/top/bottom | floating pill com gap]
- Sidebar border-radius: [0 nas bordas da viewport | radius interno apenas | radius em todos os lados]
- TopBar: [faixa contínua acima do conteúdo, NÃO sobrepõe sidebar | full-width sobre tudo | pill flutuante]
- Toggle collapse: [no header da sidebar | no topbar | botão inline]
- Padding externo (gap entre sidebar/topbar e viewport): [0px — colado | Npx — descolado]

### Implementação proposta:
- sidebar { width: Xpx; height: 100vh; border-radius: 0; position: sticky }
- topbar { height: Xpx; border-radius: 0; width: 100% do main }

❌ NÃO INFERIR. Descrever APENAS o que está VISÍVEL na imagem.
```

**Se NÃO houver referência visual:** Usar PAGE-SPEC-{página}.md → Spatial Anatomy table.

**Mapeamento de Specs por Componente:**

| Componente | Specs Obrigatórias |
|------------|-------------------|
| Header / Navbar | `SHARED-LAYOUT.md` §1 |
| Footer | `SHARED-LAYOUT.md` §2 |
| Mobile Menu | `SHARED-LAYOUT.md` §3 |
| Dashboard Layout | `SHARED-LAYOUT.md` §4 + `PAGE-SPEC-Dashboard.md` |
| Dashboard Sections (KPIs, Cards) | `PAGE-SPEC-Dashboard.md` + `MASTER.md` §Efeitos Visuais |
| Seções de LP | `PAGE-SPEC-Landing.md` + `SHARED-LAYOUT.md` §1-§2 |
| Seções de Pricing | `PAGE-SPEC-Pricing.md` |
| Componentes UI (Button, Input) | `MASTER.md` apenas |
| Docs Search | `SHARED-LAYOUT.md` §1.1 |

**Ações:**
1. Para cada task do breakdown:
   - Gerar testes baseados nos critérios de aceite
   - Verificar que testes falham (RED)
   - **Se tem UI:** Passar pelo UI Spec Reading Gate (📖 SPEC)
   - Implementar código mínimo (GREEN)
     - **Se tem UI:** Usar variáveis CSS do MASTER.md (skill: `design-system-enforcement`)
   - Refatorar mantendo verde (REFACTOR)
2. **Concluir task no Notion** (OBRIGATÓRIO - ver abaixo)

#### 🚫 ANTI-MOCK TEST GATE (OBRIGATÓRIO — Phase 4) 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** Testes que testam MOCK DATA de pages/routes de produção são
> INVÁLIDOS. Um teste que passa com `const mockProject = {...}` hardcoded na page.
> NÃO garante que a page funciona com dados reais do Supabase.
>
> **FALHA QUE GEROU ESTA REGRA:** Projeto Flyee criou 140+ testes em ~2h.
> TODOS passavam porque testavam renderização de props mock, não integração.
> Resultado: 7 páginas com mock data marcadas como "implementadas".

**Regras para testes válidos:**

| Tipo de Teste | O que DEVE validar | O que NÃO é válido |
|--------------|-------------------|--------------------|
| **Page (server component)** | Query Supabase retorna dados → renderiza | Props mock passadas manualmente |
| **API route** | Request → INSERT/UPDATE no DB → Response real | `return NextResponse.json(mockData)` |
| **Client component** | onClick → chama função → efeito colateral | `onSubmit={() => {}}` como handler |
| **Form** | Submit → API call → feedback ao user | Form que renderiza mas não envia |

**Na Phase GREEN (implementação):**

```markdown
⚠️ ANTI-MOCK TEST CHECK — Task: {título}

[ ] Page/route queries banco de dados REAL (não hardcoded)?
[ ] API route persiste dados (INSERT/UPDATE), não retorna mock?
[ ] Handlers de click/submit executam ação REAL, não noop?
[ ] Teste valida COMPORTAMENTO end-to-end, não apenas renderização?

❌ Se mock detectado em produção → Reescrever para usar dados reais
✅ Todos OK → GREEN válido
```

> [!CAUTION]
> **GATE DE CONCLUSÃO DE TASK (OBRIGATÓRIO):**
> Após cada task aprovada (testes passando), seguir **skill `notion-task-patterns`** → Seção "GATE DE SYNC NOTION".
> **Não prosseguir** para próxima task sem completar sync.

---

#### 🚨 SYNC OBRIGATÓRIO - EXECUTAR APÓS CADA TASK CONCLUÍDA ⭐

> [!CAUTION]
> **HARD BLOCKER:** O agente NÃO PODE prosseguir para próxima task sem executar TODAS as chamadas abaixo.
> Se pular este sync, o workflow está QUEBRADO e perde transparência com cliente.

**PASSO 1 - Buscar page_id da task (se não tiver):**

```json
// Tool: mcp_notion-mcp-server_API-query-data-source
{
  "data_source_id": "{DATABASE_ID}",
  "filter": {
    "property": "ID",
    "unique_id": { "equals": {TASK_NUMBER} }
  }
}
```

**PASSO 2 - Atualizar propriedades (OBRIGATÓRIO):**

```json
// Tool: mcp_notion-mcp-server_API-patch-page
{
  "page_id": "{page_id}",
  "properties": {
    "Status": { "status": { "name": "Concluído" } },
    "Tempo Gasto": { "rich_text": [{ "text": { "content": "{Xh Ym}" } }] },
    "% Progresso": { "number": 100 }
  }
}
```

**PASSO 3 - Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

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

**PASSO 4 - Adicionar comentário de conclusão (OBRIGATÓRIO):**

```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{page_id}" },
  "rich_text": [{
    "text": {
      "content": "✅ **Task Concluída**\n\n📋 **O que foi feito:**\n• {descrição}\n\n📁 **Arquivos:**\n• {arquivo1}\n• {arquivo2}\n\n🧪 **Testes:** {X} passando"
    }
  }]
}
```

**PASSO 5 - Atualizar arquivos locais:**

1. `task.md` → Marcar `[x]` para esta task
2. `PROJECT-PROGRESS.md` → Adicionar entrada no histórico

---

> [!WARNING]
> **VERIFICAÇÃO DE ENFORCEMENT:**
> Antes de iniciar próxima task, o agente DEVE confirmar:
> - "Sync Notion executado para Task #X: ✅"
> 
> Se não conseguir confirmar, PARAR e executar sync primeiro.

---

**Gate de Saída (por task):**
```
[ ] PASSO 1: page_id obtido
[ ] PASSO 2: API-patch-page executado (Status, Tempo Gasto, % Progresso)
[ ] PASSO 3: API-patch-block-children executado (nota de conclusão no corpo)
[ ] PASSO 4: API-create-a-comment executado
[ ] PASSO 5: task.md e PROJECT-PROGRESS.md atualizados
[ ] CONFIRMAÇÃO: "Sync Notion executado para Task #X: ✅"
```

---

### Phase 5: IMPLEMENTAÇÃO - Código

**Objetivo:** Implementar todas as features COM UI estilizada.

**Trigger:**
```
Testes escritos → Automático
```

> [!CAUTION]
> **GATE OBRIGATÓRIO POR TASK:** Seguir skill `context-gathering-patterns` → seção "PROCESSO DE CONTEXT GATHERING"
> ANTES de implementar cada task. Ler TDD + docs de fluxo + persistir checklist em `PROJECT-PROGRESS.md`.

> [!IMPORTANT]
> **Phase 5 tem 3 SUB-FASES OBRIGATÓRIAS:**
> 1. Backend/Lógica
> 2. UI Components (estrutura)
> 3. UI Styling (Design System)

---

#### Phase 5.1: BACKEND E LÓGICA

**Agentes Envolvidos:**
- `app-builder` - Orquestração
- `database-architect` - Schema
- `backend-specialist` - API

**Ações:**
1. Implementar lib modules (auth, db, api, etc.)
2. Criar endpoints/rotas de API
3. Rodar testes a cada mudança
4. Atualizar progresso no `PROJECT-PROGRESS.md`

**Gate de Saída:**
```
[ ] Todos os lib modules implementados
[ ] Testes do backend passando
```

---

#### Phase 5.2: UI COMPONENTS (Estrutura + Styling Premium)

> [!CAUTION]
> **STYLING INLINE OBRIGATÓRIO:** Componentes DEVEM ser criados já com o styling
> premium final (glassmorphism, gradientes, glows, backdrop-blur, micro-animações).
> **NÃO** criar estrutura primeiro para estilizar depois — isso gera retrabalho.

**Agentes Envolvidos:**
- `frontend-specialist` - Web
- `mobile-developer` - Mobile

**Ações:**
1. **Classificar cada componente antes de criar** (🔴 OBRIGATÓRIO):

   | Tipo | Critério | Pasta |
   |------|----------|-------|
   | **Reutilizável** | Pode ser usado em 2+ páginas/features diferentes | `src/components/ui/` |
   | **Feature-specific** | Só faz sentido em 1 contexto (ex: Step3Audience) | `src/components/{feature}/` |
   | **Layout compartilhado** | Usado no shell da aplicação (topbar, sidebar) | `src/components/dashboard/` ou `src/components/layout/` |

   > [!CAUTION]
   > **REGRA BLOQUEANTE:** Um componente que pode ser reutilizado em outro contexto
   > DEVE ser criado em `src/components/ui/` desde o início, com CSS Module próprio.
   > Criar em pasta de feature e mover depois = retrabalho de import.
   >
   > **FALHA QUE GEROU ESTA REGRA:** `ReviewCard` e `IconButton` foram criados
   > em `src/components/wizard/steps/` e na TopBar respectivamente,
   > sem CSS Module, com Tailwind inline. Precisaram ser movidos, refatorados
   > e conectados ao Design System em uma sessão separada.

   **Perguntas para classificar:**
   - "Este botão/card/input pode ser usado na dashboard E no wizard?" → `ui/`
   - "Este componente tem lógica/visual genérico suficiente para outro dev reutilizar?" → `ui/`
   - "Este componente só faz sentido dentro de 1 passo do wizard?" → `wizard/steps/`

2. Criar estrutura de componentes **com styling premium desde o início**
3. Aplicar tokens do MASTER.md + efeitos visuais (glassmorphism, gradientes, glows)
4. Implementar lógica dos componentes (estados, hooks)
5. Conectar com backend/APIs
6. Criar rotas do app

**Gate de Saída:**
```
[ ] **Componentes classificados (ui/ vs feature-specific) antes de criar** ⭐
[ ] **Componentes reutilizáveis em src/components/ui/ com CSS Module próprio** ⭐
[ ] Componentes criados com lógica funcional
[ ] Componentes com styling premium aplicado — NÃO apenas CSS variables, mas:
    [ ] Glassmorphism (backdrop-filter + overlay) onde MASTER.md define ⭐
    [ ] Shadows (var(--shadow-*)) com níveis de elevação corretos
    [ ] Micro-animações em hover/focus (transition, transform)
    [ ] Borders usando overlay variables (var(--color-overlay-*))
[ ] Rotas do app funcionando
[ ] Componentes conectados ao backend
[ ] 🔴 **DATA INTEGRATION VERIFICADO** (ver gate abaixo)
```

#### 🔌 DATA INTEGRATION GATE (OBRIGATÓRIO — Phase 5.2) 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de marcar Phase 5.2 como concluída, o agente DEVE
> verificar que NENHUMA page/route de produção contém mock data.
>
> **FALHA QUE GEROU ESTA REGRA:** Phase 5.2 tinha o gate "Componentes conectados ao backend"
> mas sem mecanismo de verificação. O agente marcou como ✅ sem checar. 7 arquivos tinham
> `mockData`, `// MVP: mock response`, e `onApprove={() => {}}` em produção.

**Verificação OBRIGATÓRIA (executar para cada page/route):**

```markdown
⚠️ DATA INTEGRATION SCAN — Phase 5.2 Completa?

Para CADA arquivo em src/app/ (pages e routes de produção):
[ ] Buscar padrão: `mock` (case insensitive) — ZERO ocorrências?
[ ] Buscar padrão: `() => {}` ou `() => { }` — ZERO callbacks noop?
[ ] Buscar padrão: `// TODO` em lógica de negócio — ZERO placeholders?
[ ] Buscar padrão: `// MVP:` — ZERO flags de MVP?

Se QUALQUER padrão encontrado:
→ LISTAR arquivos afetados
→ CORRIGIR antes de marcar Phase 5.2 como concluída
→ Conectar ao banco de dados / implementar lógica real

✅ ZERO mock patterns em produção → Phase 5.2 LIBERADA
```

**Comandos de scan sugeridos:**

```bash
# Buscar mock data em pages de produção
grep -rn "mock" src/app/ --include="*.tsx" --include="*.ts" -l
grep -rn "() => {}" src/app/ --include="*.tsx" --include="*.ts" -l
grep -rn "// TODO" src/app/ --include="*.tsx" --include="*.ts" -l
grep -rn "// MVP" src/app/ --include="*.tsx" --include="*.ts" -l
```

> [!CAUTION]
> **FALHA QUE GEROU ESTA EXPANSÃO:** O gate anterior apenas checava
> "styling premium aplicado (não esqueleto)" — vago demais. O agente
> interpretou como "usar CSS variables" e passou o gate sem aplicar
> glassmorphism, shadows ou animações. Agora cada sub-item é explícito.

> [!CAUTION]
> **VALIDAÇÃO OBRIGATÓRIA:** Antes de prosseguir, verificar conexões UI→Função.
> **Skill:** `integration-completeness`

**Checklist de Integração (OBRIGATÓRIO):**
```markdown
Para CADA componente interativo:
[ ] onClick/onSubmit definido?
[ ] Handler chama função correta (não é vazio)?
[ ] Função está importada?
[ ] Teste verifica clique → ação (não só existência)?
```

---

#### Phase 5.3: UI STYLING VALIDATION (Verificação + Ajustes Finos) ⭐ OBRIGATÓRIO

> [!CAUTION]
> **REGRA BLOQUEANTE:** NÃO prosseguir para Phase 6 sem completar esta sub-fase.
> Componentes sem styling = projeto incompleto.

> [!IMPORTANT]
> **Esta fase é APENAS para VALIDAÇÃO e AJUSTES FINOS.**
> Se o styling inline foi seguido corretamente durante Phase 4 (TDD GREEN) e Phase 5.2,
> os componentes já possuem styling premium. Esta fase verifica se a qualidade visual
> está uniforme entre todas as páginas e faz ajustes de polimento se necessário.
> **NÃO é para aplicar styling do zero** — se isso for necessário, significa que as
> phases anteriores não foram executadas corretamente.

> [!IMPORTANT]
> **EXECUTAR WORKFLOW:** `/ui-ux-pro-max` se Design System ainda não existe.
> Este workflow contém 50+ estilos, 97 paletas de cores e checklist profissional.

**Agentes Envolvidos:**
- `frontend-specialist` - Web
- `mobile-developer` - Mobile

---

**PASSO 1: Executar `/ui-ux-pro-max` (OBRIGATÓRIO)**

```bash
# Gerar Design System completo com recomendações
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "{produto} {indústria} {keywords}" --design-system -p "{Nome do Projeto}"
```

**Exemplo para SaaS:**
```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "saas startup professional" --design-system -p "Flyeelab"
```

**Output esperado:**
- Pattern recomendado
- Style (glassmorphism, minimalism, etc.)
- Paleta de cores
- Tipografia
- Efeitos visuais
- Anti-patterns a evitar

---

**PASSO 2: Persistir Design System (se não existir)**

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "{query}" --design-system --persist -p "{Projeto}"
```

Gera:
- `design-system/MASTER.md` - Source of Truth
- `design-system/pages/` - Overrides por página

---

**PASSO 2.5: Instalar CSS Variables (OBRIGATÓRIO) 🔴**

> [!CAUTION]
> **REGRA BLOQUEANTE:** Antes de estilizar componentes, garantir que as variáveis CSS
> do Design System estão instaladas no `globals.css` (ou equivalente).

**Ações:**
1. Abrir `design-system/{projeto}/MASTER.md`
2. Copiar seção "CSS Variables" ou "Tokens"
3. Colar em `src/app/globals.css` (Next.js) ou arquivo CSS global equivalente
4. Verificar que variáveis incluem:
   - Cores primárias (--lime, --bg-primary, etc.)
   - Backgrounds (--bg-card, --bg-elevated)
   - Texto (--text-primary, --text-secondary, --text-muted)
   - Espaçamentos (--radius-sm, --radius-md, etc.)
5. Definir body styling base:
   ```css
   body {
     background: var(--bg-primary);
     color: var(--text-primary);
     font-family: 'Plus Jakarta Sans', sans-serif; /* ou font do MASTER.md */
   }
   ```
6. Reiniciar dev server (`npm run dev`)

**Gate de Saída PASSO 2.5:**
```
[ ] CSS variables do MASTER.md copiadas para globals.css
[ ] Body styling definido (background, color, font)
[ ] Dev server reiniciado
[ ] Página renderiza com cores corretas (verificar no browser)
```

---

**PASSO 3: Buscar Guidelines do Stack**

```bash
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "layout responsive form" --stack html-tailwind
```

Stacks disponíveis: `html-tailwind`, `react`, `nextjs`, `shadcn`, etc.

---

**PASSO 4: Aplicar para CADA componente**

1. Carregar `design-system/{nome}/MASTER.md`
2. Aplicar cores, tipografia, espaçamento
3. Verificar regras do `/ui-ux-pro-max`:
   - ❌ Sem emojis como ícones (usar SVG)
   - ✅ `cursor-pointer` em clicáveis
   - ✅ Hover states com feedback visual
   - ✅ Contraste adequado (4.5:1 mínimo)
   - ✅ Responsivo em 375px, 768px, 1024px, 1440px

---

**PASSO 4.5: Usar shadcn/ui Components (Opcional - /stitch --shadcn)**

> [!TIP]
> Para acelerar desenvolvimento, use componentes prontos do shadcn/ui.
> **Workflow:** `/stitch --shadcn [componente]`
> **Skill:** `shadcn-ui`

```bash
# Instalar componente
npx shadcn-ui@latest add button
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add form

# Ver todos disponíveis
npx shadcn-ui@latest add --help
```

**Quando usar:**
- Formulários complexos → `form`, `input`, `select`
- Modais/Dialogs → `dialog`, `alert-dialog`
- Navegação → `navigation-menu`, `dropdown-menu`
- Feedback → `toast`, `alert`

---

**PASSO 4.6: Componentes Premium de Bibliotecas Externas (Opcional)**

> [!TIP]
> **Skill:** `component-library-discovery`
> Use bibliotecas externas compatíveis com shadcn para componentes premium.

**Bibliotecas Disponíveis:**

| Biblioteca | Foco | Comando Base |
|------------|------|--------------|
| **badtz-ui** | LPs, conversão | `npx shadcn@latest add https://badtz-ui.com/r/<comp>.json` |
| **uselayouts** | Micro-interações | `npx shadcn@latest add https://uselayouts.com/r/<comp>` |
| **lucide-animated** | Ícones animados | Copy-paste de lucide-animated.com |

**Componentes Comuns:**

| Necessidade | Biblioteca | Componente |
|-------------|------------|------------|
| Hero Section | badtz-ui | `hero-section` |
| CTA com destaque | badtz-ui | `glowing-button` |
| Cards 3D | uselayouts | `3d-book` |
| Loading animado | lucide-animated | `loader-pinwheel` |
| Success feedback | lucide-animated | `check`, `circle-check` |

**Se não souber qual componente usar:**
> Seguir skill `component-library-discovery` → PASSO 2 (Perguntas Interativas)

**Catálogos completos:**
- [badtz-ui.com/docs](https://badtz-ui.com/docs)
- [uselayouts.com/docs](https://uselayouts.com/docs/introduction)
- [lucide-animated.com](https://lucide-animated.com)

---

**PASSO 5: Pre-Delivery Checklist (OBRIGATÓRIO)**

Verificar ANTES de marcar Phase 5.3 como concluída:

```markdown
### Visual Quality
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] Hover states don't cause layout shift
- [ ] Theme colors applied correctly

### Interaction
- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation

### Light/Dark Mode
- [ ] Light mode text has sufficient contrast
- [ ] Glass/transparent elements visible in light mode
- [ ] Test both modes before delivery

### Layout
- [ ] Floating elements have proper spacing from edges
- [ ] No content hidden behind fixed navbars
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile
```

---

**PASSO 6: Validação Automatizada (OBRIGATÓRIO)**

> [!CAUTION]
> **EXECUTE ANTES DE MARCAR COMPLETO:**

> **Skill:** `ui-validation`

```bash
python .agent/skills/ui-validation/scripts/ui_antipattern_check.py .
```

**Resultado:**
- ❌ Errors → CORRIGIR antes de prosseguir
- ⚠️ Warnings → Considerar correção
- ✅ Passed → Pode prosseguir

---

**Gate de Saída Phase 5.3:**
```
[ ] /ui-ux-pro-max executado
[ ] Design System persistido
[ ] TODOS os componentes estilizados
[ ] Pre-Delivery Checklist 100% ✅
[ ] 🔴 ui-validation script PASSOU
[ ] Verificação visual (screenshot ou preview)
[ ] Responsivo verificado
```

---

#### Phase 5.4: NOTION SYNC (OBRIGATÓRIO) 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** Após completar cada épico, sincronizar Notion.
> NÃO prosseguir para Phase 6 sem todas as tasks sincronizadas.

**Ações para CADA épico:**
1. Listar tasks do épico no Notion
2. Atualizar propriedades:

```json
// Tool: mcp_notion-mcp-server_API-patch-page
{
  "page_id": "{page_id}",
  "properties": {
    "Status": { "status": { "name": "Concluído" } },
    "Tempo Gasto": { "rich_text": [{ "text": { "content": "{tempo}" } }] },
    "% Progresso": { "number": 100 }
  }
}
```

3. **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

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

4. Adicionar comentário de conclusão
5. **Exibir log de execução** (conforme `project-tracking-patterns` Seção 6)

**Gate de Saída Phase 5:**
```
[ ] Todas as sub-fases (5.1, 5.2, 5.3, 5.4) concluídas
[ ] PROJECT-PROGRESS.md atualizado
[ ] 🔴 NOTION SINCRONIZADO - Todas as tasks do projeto
```

**Template de verificação:**
```markdown
📊 **Notion Sync - Phase 5**

| Épico | Tasks | Sync |
|-------|-------|------|
| 1. Setup | 5/5 | ✅ |
| 2. Auth | 4/4 | ✅ |
| 3. Landing | 4/4 | ✅ |
| ... | ... | ... |

✅ Notion 100% sincronizado. Liberado para Phase 6.
```

---

**Regras Gerais Phase 5:**
- ✅ Ler TDD a cada nova task
- ✅ Rodar testes antes de cada commit
- ✅ Aplicar Design System em 100% dos componentes
- ❌ Não inventar features não documentadas
- ❌ Não deixar componentes sem styling
- ❌ Não prosseguir para Phase 6 com UI incompleta

---

### 🛑 GATE OBRIGATÓRIO: Phase 5 → Phase 6

> [!CAUTION]
> **BLOQUEADOR ABSOLUTO:** Você NÃO PODE iniciar Phase 6 sem completar TODAS as sub-fases de Phase 5.

**Checklist de Verificação (OBRIGATÓRIO):**

```markdown
⚠️ VERIFICAÇÃO OBRIGATÓRIA ANTES DE PHASE 6

## Sub-Fases Obrigatórias
[ ] 5.1 Backend/Lógica - Todos os épicos implementados
[ ] 5.2 UI Components - Todos os componentes criados
[ ] 5.3 UI STYLING - Design System aplicado
    [ ] /ui-ux-pro-max executado
    [ ] Pre-Delivery Checklist 100%
    [ ] Verificação visual feita
[ ] 5.4 Notion Sync - Todas tasks sincronizadas
    [ ] Épico 1 → 100%
    [ ] Épico 2 → 100%
    [ ] ... → 100%

## Regra de Decisão
❌ QUALQUER item desmarcado → EXECUTE a sub-fase faltante
✅ TODOS marcados → Pode prosseguir para Phase 6

## Ação se Incompleto
Se 5.3 faltando: /new-project --phase 5.3
Se 5.4 faltando: /new-project --phase 5.4
```

> [!IMPORTANT]
> **Se você chegou aqui sem completar 5.3 ou 5.4:**
> PARE imediatamente e execute as sub-fases faltantes.

---

### Phase 6: VERIFICAÇÃO - Gate de Cobertura

**Objetivo:** Garantir qualidade mínima.

**Trigger:**
```
Implementação concluída
```

**Ações:**
1. Executar `/test coverage`
2. Verificar cobertura >= 80%
3. 🔴 **Executar E2E SMOKE TEST do Core Loop** (ver abaixo)

**Gate de Saída:**

| Verificação | Ação |
|-------------|------|
| Cobertura >= 80% | ✅ Prosseguir |
| Cobertura < 80% | ❌ Adicionar testes faltantes |
| **E2E Smoke Test FALHOU** | ❌ **CORRIGIR — fluxo principal não funciona** |

> [!CAUTION]
> **BLOQUEADOR:** Não fazer deploy com cobertura < 80%.

#### 🔄 E2E CORE LOOP SMOKE TEST (OBRIGATÓRIO — Phase 6) 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** Phase 6 NÃO é apenas cobertura de testes.
> O agente DEVE verificar que o **CORE LOOP do produto funciona de ponta a ponta**
> com DADOS REAIS, não apenas que os testes unitários passam.
>
> **FALHA QUE GEROU ESTA REGRA:** Projeto Flyee tinha 140+ testes passando e
> cobertura >80%, mas o core loop (criar projeto → criar decisão → portal → aprovar)
> estava 100% broken porque nenhum teste verificava integração real.

**O que é o Core Loop?**

Consultar o PRD seção "Core Flow" ou "Jornada Principal" para identificar
o fluxo principal do produto. Exemplo:

```
[Ação 1] → [Ação 2] → [Ação 3] → [Resultado Final]
```

**Verificação OBRIGATÓRIA para cada etapa do Core Loop:**

```markdown
⚠️ E2E CORE LOOP SMOKE TEST — {nome do projeto}

Core Loop identificado no PRD: {descrever fluxo}

| # | Etapa | Page/Route | Mock? | DB Query? | Funcional? |
|---|-------|-----------|-------|-----------|------------|
| 1 | {ação 1} | {arquivo} | [ ] | [ ] | [ ] |
| 2 | {ação 2} | {arquivo} | [ ] | [ ] | [ ] |
| 3 | {ação 3} | {arquivo} | [ ] | [ ] | [ ] |
| ... | ... | ... | ... | ... | ... |

Para CADA etapa:
[ ] Nenhum mock data em produção?
[ ] Queries ao banco reais (supabase.from() / prisma)?
[ ] Handlers conectados a ações reais (não noop)?
[ ] Fluxo anterior → etapa atual funciona?

❌ Se QUALQUER etapa falhar → PARAR e corrigir ANTES de Phase 7
✅ Core Loop 100% funcional → Liberado para deploy
```

> [!TIP]
> Se possível, rodar o smoke test no browser (dev server) e não apenas via testes unitários.
> Isso detecta problemas que testes de componente isolado não capturam.

---

### Phase 7: PREVIEW e DEPLOY

**Objetivo:** Visualizar e publicar.

**Agentes Envolvidos:**
- `devops-engineer` - Definição de infra e deploy
- `security-auditor` - Validação pré-deploy

---

#### Phase 7.1: ENVIRONMENT DISCOVERY (OBRIGATÓRIO) ⭐

> [!CAUTION]
> **BLOQUEADOR:** ANTES de qualquer deploy, DEVE-SE definir ambientes.
> Esta pergunta é OBRIGATÓRIA mesmo para projetos simples.

**Verificar se ambientes já estão definidos:**
1. Checar `docs/design/TDD-{nome}.md` seção "Infraestrutura"
2. Checar `docs/PROJECT-PROGRESS.md`

**Se NÃO estão definidos, PERGUNTAR:**

```markdown
## 🌍 Definição de Ambientes

Preciso entender sua estratégia de ambientes antes do deploy:

1. **Quais ambientes você precisa?**
   - [ ] Development (local)
   - [ ] Staging (testes/validação)
   - [ ] Production (usuários finais)

2. **Onde será hospedado cada ambiente?**
   - Ex: Vercel, Railway, VPS, Docker, etc.

3. **Variáveis de ambiente diferem por ambiente?**
   - Ex: API keys de teste vs produção
```

**Template de Ambientes:**

| Ambiente | URL | Propósito |
|----------|-----|-----------|
| Development | `localhost:3000` | Desenvolvimento local |
| Staging | `staging.{app}.com` | Testes e validação |
| Production | `{app}.com` | Usuários finais |

**Template de Variáveis por Ambiente:**

| Variável | Dev | Staging | Prod |
|----------|-----|---------|------|
| `DATABASE_URL` | local | staging-db | prod-db |
| `API_KEY` | test-key | test-key | prod-key |
| `DEBUG` | true | true | false |

**Gate de Saída Phase 7.1:**
```
[ ] Ambientes definidos (dev/staging/prod ou subset)
[ ] Plataforma escolhida para cada ambiente
[ ] Variáveis de ambiente mapeadas
[ ] AGUARDAR confirmação do usuário
```

> [!TIP]
> Se usuário confirmar "só preciso de prod", prosseguir. Mas a pergunta DEVE ser feita.

---

#### Phase 7.2: PRE-FLIGHT CHECKS

**Ações:**
1. Rodar checklist final: `python .agent/scripts/checklist.py .`
2. Verificar todos os gates anteriores (5.3 UI, 5.4 Notion, 6 Coverage)
3. Validar variáveis de ambiente

**Gate de Saída:**
```
[ ] Checklist passou
[ ] Variáveis de ambiente documentadas
[ ] Rollback plan definido
```

---

#### Phase 7.3: PREVIEW e DEPLOY

**Ações:**
1. Iniciar preview: `auto_preview.py`
2. Apresentar URL ao usuário
3. Se aprovado, executar deploy para ambiente escolhido

**Para cada ambiente (se staging + prod):**
1. Deploy staging primeiro
2. Validar em staging
3. Deploy production

---

### Phase 7.5: PUBLICAÇÃO DE DOCUMENTAÇÃO TÉCNICA NO NOTION

> [!CAUTION]
> **REGRA BLOQUEANTE:** Toda documentação gerada nas fases anteriores DEVE ser publicada
> na database "Documentação Técnica" do Notion para **acesso da equipe de desenvolvimento**.
> Os devs leem no Notion — NÃO acessam o repositório.

**Objetivo:** Publicar documentação completa na database Notion "Documentação Técnica" para acesso dos devs.

**Trigger:**
```
Phase 7.3 concluída (deploy feito) → Automático
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

> Se database ausente → PARAR e notificar usuário (ver skill para mensagem).

#### Passo 2: Coletar Artefatos Gerados

| Fonte | Tipo | Arquivo Local | Publicar? |
|---|---|---|---|
| Phase 1 | PRD | `docs/PRD-{nome}.md` | ✅ |
| Phase 2 | TDD | `docs/design/TDD-{nome}.md` | ✅ |
| Phase 2.5 | Design System | `design-system/{nome}/MASTER.md` | ✅ (se UI) |
| Phase 4 | Testes | (relatório de cobertura) | ✅ |

#### Passo 3: Publicar

> Seguir skill `notion-task-patterns` → seção "Processo: Publicação de Documentação Técnica"

Para cada doc:
1. Verificar upsert (doc já existe?)
2. Ler conteúdo completo do arquivo local
3. Criar/atualizar página Notion com template correto
4. Preencher propriedades + histórico + tasks relacionadas

#### Passo 4: Relatório de Publicação

```markdown
📚 **DOCUMENTAÇÃO TÉCNICA PUBLICADA - {projeto}**

| # | Documento | Tipo | Status |
|---|-----------|------|--------|
| 1 | {nome} | PRD | Publicado |
| 2 | {nome} | TDD | Publicado |
| ... | ... | ... | ... |

Total: {N} documentos publicados
✅ Devs podem consultar em: Notion → Database "Documentação Técnica"
```

**Gate de Saída:**
```
[ ] Database "Documentação Técnica" encontrado e validado
[ ] Todos os artefatos publicados
[ ] Upsert verificado (sem duplicatas)
[ ] Histórico e tasks referenciadas em cada doc
[ ] PROJECT-PROGRESS.md atualizado
```

---

### Phase 7.6: PUBLICAÇÃO DO MANUAL DO USUÁRIO NO NOTION

> [!CAUTION]
> **REGRA BLOQUEANTE:** Para cada fluxo publicado na Phase 7.5, DEVE existir uma versão
> em linguagem acessível na database "Manual do Usuário" do Notion.
> Usuários finais e operadores leem estes guias — sem código, sem jargão técnico.

**Objetivo:** Publicar guias em linguagem acessível na database Notion "Manual do Usuário".

**Trigger:**
```
Phase 7.5 concluída → Automático
```

**Agentes Envolvidos:**
- `orchestrator` - Integração Notion

> [!IMPORTANT]
> **SKILL:** Seguir `notion-task-patterns` → seção "Processo: Publicação do Manual do Usuário" OBRIGATORIAMENTE.

#### Passo 1: Discovery e Validação

> Seguir skill `notion-task-patterns` → seção "DATABASE 2"

```json
// Tool: mcp_notion-mcp-server_API-post-search
{
  "query": "Manual do Usuário",
  "filter": { "property": "object", "value": "data_source" }
}
```

> Se database ausente → PARAR e notificar usuário (ver skill para mensagem).

#### Passo 2: Mapear e Publicar Guias

> Seguir skill `notion-task-patterns` → tabela "Mapear Fluxos Técnicos → Guias de Usuário"

Para cada guia:
1. **Verificar upsert** — guia já existe? (query por Nome)
2. **Gerar conteúdo** em linguagem simples (sem código)
3. **Criar ou atualizar** página com template de guia do usuário
4. **Definir propriedades:** Nome, Seção, Status, Público-alvo

#### Passo 3: Relatório de Publicação

```markdown
📖 **MANUAL DO USUÁRIO PUBLICADO - {projeto}**

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
[ ] PROJECT-PROGRESS.md atualizado
```

---

## 📁 Estrutura de Arquivos Gerados

### Modo Completo
```
projeto/
├── docs/
│   ├── PRD-{nome}.md                 # Phase 1
│   └── design/
│       └── TDD-{nome}.md             # Phase 2
├── {nome}.md                         # Plan file (Phase 3)
├── tests/                            # Phase 4
│   ├── unit/
│   └── integration/
└── src/                              # Phase 5
```

### Modo --quick
```
projeto/
├── docs/
│   └── design/
│       └── TDD-{nome}.md             # Phase 2 (sem PRD)
├── {nome}.md                         # Plan file
├── tests/
└── src/
```

---

## 🔗 INTEGRAÇÃO COM OUTROS WORKFLOWS

| Este workflow chama | Propósito |
|---------------------|-----------|
| `/brainstorm` | Phase 0 (opcional) |
| `/prd new` | Phase 1 |
| `/tdd new` + `/tdd validate` + `/tdd breakdown` | Phase 2-3 |
| `/test [feature]` | Phase 4 |
| `/create` ou `/orchestrate` | Phase 5 |
| `/test coverage` | Phase 6 |
| `notion-task-patterns` → "DOCUMENTATION DATABASE" | Phase 7.5 |

| Workflows Relacionados | Quando Usar |
|------------------------|-------------|
| `/discovery` | Alternativa ágil (equivale a `--quick` + Notion) |
| `/brainstorm` | Exploração standalone sem projeto |
| `/enhance` | Nova feature em projeto existente |
| `/document` | Documentar projeto legado |

---

## 🔴 REGRAS CRÍTICAS

1. **Aprovação humana obrigatória** em PRD e TDD
2. **Testes ANTES do código** (TDD Metodologia)
3. **Cobertura >= 80%** antes de deploy
4. **Rastreabilidade:** TDD referencia PRD, Tasks referenciam TDD
5. **Um projeto = Um PRD = Um TDD principal**
6. **Ambientes obrigatórios:** SEMPRE perguntar sobre dev/staging/prod antes de deploy (Phase 7.1)
7. **📚 DOCUMENTAÇÃO PARA DEVS E USUÁRIOS** - Ao final do projeto (Phase 7.5 + 7.6), publicar docs completos nas databases "Documentação Técnica" e "Manual do Usuário" do Notion. Seguir skill `notion-task-patterns` → "DOCUMENTATION DATABASES"
8. **📋 NOTION DESDE O INÍCIO** - Tasks de planejamento (Phase 2.5–2.9) são criadas na Phase 2.1, garantindo tracking completo desde o início do projeto. Pulado no modo `--quick`

---

## Usage Examples

```bash
# Novo projeto com ideia indefinida (inclui brainstorm)
/new-project --brainstorm meu-app-fitness

# Novo projeto com ideia clara (fluxo completo)
/new-project meu-app-fitness

# Projeto rápido sem PRD formal (modo ágil)
/new-project --quick meu-app-fitness

# Continuar de PRD já aprovado
/new-project --from-prd docs/PRD-meu-app.md

# Continuar de TDD já aprovado
/new-project --from-tdd docs/design/TDD-meu-app.md

# Importar de proposta comercial aprovada
/new-project --from-demand "Proposta App Fitness"

# Ver status do projeto
/new-project status
```

---

## 📋 Comparativo de Modos

| Aspecto | Completo | --brainstorm | --quick |
|---------|----------|--------------|---------|
| Phase 0 (Brainstorm) | ❌ | ✅ | ❌ |
| Phase 1 (PRD) | ✅ | ✅ | ❌ |
| Phase 2 (TDD) | ✅ | ✅ | ✅ |
| Phase 2.1 (Notion Setup) | ✅ | ✅ | ❌ |
| Socratic Gate | 12 perguntas | 12 perguntas | 5 perguntas |
| Documentação | PRD + TDD | PRD + TDD | TDD only |
| Tempo estimado | Maior | Maior | Menor |
| Recomendado para | Projetos formais | Ideias indefinidas | MVPs rápidos |
