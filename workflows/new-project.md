---
description: Workflow unificado para novo projeto. Orquestra PRD → TDD Técnico → Design System → Breakdown → TDD Metodologia → Implementação → Deploy. Fluxo completo com checkpointing.
skills: notion-task-patterns, checkpointing-patterns, project-tracking-patterns, ui-ux-discovery, local-verification, integration-completeness, content-strategy
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
Phase 1 (PRD) → Phase 2 (TDD) → Phase 3 (Breakdown) → Phase 4 (Tests) → Phase 5 (Code) → Phase 6 (Verify) → Phase 7 (Deploy)
```

### Modo BRAINSTORM (Ideia indefinida)
```
/new-project --brainstorm meu-app
```
```
Phase 0 (Brainstorm) → Phase 1 (PRD) → ... → Phase 7 (Deploy)
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
3. Continua execução

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
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  BRAINSTORM  │───▶│     PRD      │───▶│  TDD TÉCNICO │───▶│   BREAKDOWN  │───▶│    TESTS     │───▶│   IMPLEMENT  │───▶│   VERIFY     │───▶│   DEPLOY     │
│  (OPCIONAL)  │    │  (O QUE)     │    │   (COMO)     │    │   (TASKS)    │    │  (PRIMEIRO)  │    │   (CÓDIGO)   │    │  (COBERTURA) │    │  (PREVIEW)   │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
      🧠                   ✋                  ✋                  ✅                  ✅                  ✅                  ✅                  ✅
   Exploração          Aprovação           Aprovação           Automático          Automático          Automático          Gate 80%            Final
```

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
[ ] TDD aprovado pelo humano
```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir sem aprovação do TDD.

---

### Phase 2.5: DESIGN SYSTEM - UI/UX (Opcional para APIs)

> [!NOTE]
> **Pulado se:** Projeto é apenas API/Backend sem interface.
> **Skills de referência:** `frontend-design` ou `mobile-design`

> [!IMPORTANT]
> **SKILL OBRIGATÓRIA:** Seguir `ui-ux-discovery` para perguntas granulares ANTES de finalizar Design System.
> **WORKFLOW:** Executar `/ui-ux-pro-max` para obter recomendações profissionais.

**Objetivo:** Definir UI/UX e Design System com base em decisões do usuário + recomendações inteligentes.

**Trigger:**
```
TDD aprovado → Automático (exceto --no-design)
```

**Agentes Envolvidos:**
- `frontend-specialist` - Para projetos web
- `mobile-developer` - Para projetos mobile
- `design-specialist` - Para projetos complexos

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

---

**PASSO 1: Executar `/ui-ux-pro-max` (OBRIGATÓRIO)**

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

**PASSO 4: Documentar Design System**

1. Analisar TDD para componentes visuais
2. Combinar recomendações do `/ui-ux-pro-max` com requisitos do TDD
3. Definir:
   - Paleta de cores (do PASSO 1)
   - Tipografia (do PASSO 1)
   - Componentes reutilizáveis
   - Layout principal
4. Gerar `design-system/{nome}/MASTER.md`
5. **AGUARDAR** aprovação humana

**Template com dados do /ui-ux-pro-max:**
```markdown
## design-system/{nome}/MASTER.md

> Gerado via `/ui-ux-pro-max` em {data}

### Pattern
- Tipo: {pattern recomendado}
- Style: {style recomendado}

### Cores
- Primary: {cor do ui-ux-pro-max}
- Secondary: {cor}
- Accent: {cor}
- Background: {cor}
- Surface: {cor}
- Text: {cor}

### Tipografia
- Heading: {fonte recomendada}
- Body: {fonte recomendada}
- Mono: {fonte para código}

### Efeitos
- {efeitos recomendados: glassmorphism, gradients, etc.}

### Anti-Patterns (EVITAR)
- {lista do ui-ux-pro-max}

### Componentes
- [ ] Header/Navbar
- [ ] Footer
- [ ] Cards
- [ ] Forms
- [ ] Buttons
- [ ] Modals
- [ ] Tables

### Layouts
- [ ] Home/Landing
- [ ] Dashboard
- [ ] Detail Pages
- [ ] Auth Pages
```

---

**Gate de Saída:**
```
[ ] /ui-ux-pro-max executado
[ ] Perguntas granulares respondidas pelo usuário (skill: ui-ux-discovery)
[ ] Design System persistido (design-system/{nome}/MASTER.md)
[ ] Design System aprovado pelo humano
[ ] Design System aprovado pelo humano
```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir sem aprovação do Design System.

---

### Phase 2.75: CONTENT STRATEGY - Conteúdo e Copy

> [!NOTE]
> **Pulado se:** Projeto é apenas API/Backend sem interface pública.
> **Obrigatório para:** LPs, sites institucionais, SaaS com marketing pages.

> [!IMPORTANT]
> **SKILL:** Seguir `content-strategy` para definição de copy e conteúdo.
> **Documento:** `docs/content/CONTENT-STRATEGY-{nome}.md`

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
> **BLOQUEADOR:** Não prosseguir para Breakdown sem Content Strategy aprovado (exceto --no-content).

---

### Phase 3: BREAKDOWN - Tarefas

**Objetivo:** Quebrar TDD em tarefas executáveis.

**Trigger:**
```
TDD aprovado → Automático
```

**Agentes Envolvidos:**
- `project-planner` - Quebra em tarefas

> [!IMPORTANT]
> **SKILL OBRIGATÓRIA:** Seguir `notion-task-patterns` para criação de tasks.
> Ver seção "➕ CRIAR TASK (2 ETAPAS OBRIGATÓRIAS)" da skill.

> [!CAUTION]
> **REGRA BLOQUEANTE:** Cada task requer **2 ETAPAS**:
> 1. `API-post-page` → Criar task (propriedades)
> 2. `API-patch-block-children` → Adicionar corpo (OBRIGATÓRIO)
> 
> Task sem corpo = task INCOMPLETA. Ver templates na skill.

**Ações:**
1. Executar `/tdd breakdown docs/design/TDD-{nome}.md`
2. Gerar arquivo de plano `{nome}.md`
3. Para **CADA** task: seguir fluxo de 2 etapas da skill
4. Verificar gate de saída

**Gate de Saída (OBRIGATÓRIO):**
```
[ ] Todas as tasks criadas (ETAPA 1)
[ ] TODAS as tasks com corpo (ETAPA 2)
[ ] Skill notion-task-patterns seguido
```

**Output:**
```
Tasks criadas (com corpo):
- [x] Task 1: Setup Infraestrutura → (body: ✅)
- [x] Task 2: Entidades principais → (body: ✅)
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

**Ações para Projeto EXISTENTE (já tem código):**

1. Verificar se test runner existe
2. Se não existir, instalar (passo 2 acima)
3. Verificar estrutura de pastas
4. Prosseguir para Phase 4

**Gate de Saída:**
```
[ ] Projeto inicializado (package.json existe)
[ ] Test runner configurado (vitest/jest)
[ ] Estrutura de pastas criada
[ ] npm test roda sem erros
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

**Agentes Envolvidos:**
- `test-engineer` - Geração de testes
- Especialistas de domínio conforme task

**Ciclo para CADA Task:**

| Fase | Ação | Verificação |
|------|------|-------------|
| 🔴 RED | `/test [task]` - Escrever teste que falha | Teste falha corretamente |
| 🟢 GREEN | Implementar código mínimo **usando Design System** | Teste passa |
| 🔵 REFACTOR | Melhorar código | Testes continuam passando |

**Ações:**
1. Para cada task do breakdown:
   - Gerar testes baseados nos critérios de aceite
   - Verificar que testes falham (RED)
   - Implementar código mínimo (GREEN)
     - **Se tem UI:** Usar variáveis CSS do MASTER.md (skill: `design-system-enforcement`)
   - Refatorar mantendo verde (REFACTOR)
2. **Concluir task no Notion** (OBRIGATÓRIO - ver abaixo)

> [!CAUTION]
> **GATE DE CONCLUSÃO DE TASK (OBRIGATÓRIO):**
> Após cada task aprovada (testes passando), seguir **skill `notion-task-patterns`** → Seção "GATE DE SYNC NOTION".
> **Não prosseguir** para próxima task sem completar sync.

**Ações obrigatórias ao concluir cada task:**

1. **Atualizar propriedades:**
   - `Status` → "Concluído"
   - `Tempo Gasto` → tempo real (ex: "2h30m")
   - `% Progresso` → 100

2. **Adicionar Comentário Rico** (template na skill `notion-task-patterns`)

3. **Atualizar PROJECT-PROGRESS.md** local

**Gate de Saída (por task):**
```
[ ] Status = Concluído
[ ] Tempo Gasto preenchido
[ ] % Progresso = 100
[ ] Comentário rico adicionado
[ ] PROJECT-PROGRESS.md atualizado
```

---

### Phase 5: IMPLEMENTAÇÃO - Código

**Objetivo:** Implementar todas as features COM UI estilizada.

**Trigger:**
```
Testes escritos → Automático
```

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

#### Phase 5.2: UI COMPONENTS (Estrutura)

**Agentes Envolvidos:**
- `frontend-specialist` - Web
- `mobile-developer` - Mobile

**Ações:**
1. Criar estrutura de componentes
2. Implementar lógica dos componentes (estados, hooks)
3. Conectar com backend/APIs
4. Criar rotas do app

**Gate de Saída:**
```
[ ] Componentes criados com lógica funcional
[ ] Rotas do app funcionando
[ ] Componentes conectados ao backend
```

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

> [!WARNING]
> Ainda NÃO aplicar estilos visuais finais nesta fase.

---

#### Phase 5.3: UI STYLING VALIDATION (Design System) ⭐ OBRIGATÓRIO

> [!CAUTION]
> **REGRA BLOQUEANTE:** NÃO prosseguir para Phase 6 sem completar esta sub-fase.
> Componentes sem styling = projeto incompleto.

> [!NOTE]
> **Mudança:** Se você seguiu a skill `design-system-enforcement` durante Phase 4 (TDD GREEN),
> os componentes já estão estilizados. Esta fase é para **validação e ajustes finos**.

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
2. Atualizar `Status` → "Concluído"
3. Adicionar comentário de conclusão
4. **Exibir log de execução** (conforme `project-tracking-patterns` Seção 6)

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

**Gate de Saída:**

| Cobertura | Ação |
|-----------|------|
| >= 80% | ✅ Prosseguir para preview |
| < 80% | ❌ Adicionar testes faltantes |

> [!CAUTION]
> **BLOQUEADOR:** Não fazer deploy com cobertura < 80%.

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
| Socratic Gate | 12 perguntas | 12 perguntas | 5 perguntas |
| Documentação | PRD + TDD | PRD + TDD | TDD only |
| Tempo estimado | Maior | Maior | Menor |
| Recomendado para | Projetos formais | Ideias indefinidas | MVPs rápidos |
