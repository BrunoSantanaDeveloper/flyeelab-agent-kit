---
description: Workflow unificado para novo projeto. Orquestra PRD → SDD → Project Foundation → Design System → Breakdown → Tests → Impl → Security Review → Verify (a11y+perf) → Staging → Deploy. Fluxo completo com checkpointing.
skills: checkpointing-patterns, project-tracking-patterns
---

# /new-project - Novo Projeto Completo

$ARGUMENTS

---

## 🎯 PROPÓSITO

Workflow **orquestrador** que guia a criação de um novo projeto do zero, garantindo:
- Exploração de ideias quando necessário (Brainstorm)
- Documentação completa (PRD + SDD)
- Project Foundation gerado automaticamente (README, SECURITY, INDEX, ADR, .env, openapi)
- Testes antes do código (TDD Metodologia)
- Security Review + Code Review antes do deploy
- Verificação de acessibilidade (WCAG AA) e performance baseline
- Rastreabilidade entre documentos via `docs/INDEX.md`
- Cobertura mínima de 80%

> [!IMPORTANT]
> **Nomenclatura:** Neste workflow, `SDD` = Software Design Document (documento de design técnico).
> **`TDD`** refere-se exclusivamente à **metodologia Test-Driven Development** (Phase 4).

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
| Nova feature em projeto existente | `/new-task` ou `/tdd new` | Contexto já existe |

---

## 🧩 SUBCOMMANDS

| Comando | Ação |
|---------|------|
| `/new-project [nome]` | Fluxo **completo** (PRD → SDD → Tests → Code → Security → Deploy) |
| `/new-project --brainstorm [nome]` | Inclui **Phase 0** para explorar ideias |
| `/new-project --quick [nome]` | Modo **ágil** (sem PRD formal, direto SDD) |
| `/new-project --resume` | **Retomar** de onde parou |
| `/new-project --from-prd [arquivo]` | Continua de PRD já aprovado |
| `/new-project --from-sdd [arquivo]` | Continua de SDD já aprovado |
| `/new-project --from-demand [nome]` | Importa de proposta comercial aprovada |
| `/new-project --from-figma [url]` | Importa Design System do Figma |
| `/new-project status` | Mostra status e progresso atual |

---

## 🔀 MODOS DE OPERAÇÃO

### Modo COMPLETO (Padrão)
```
/new-project meu-app
Ph1 (PRD) → Ph2 (SDD) → Ph2.05 (Foundation) → Ph2.1 (Task Setup) → Ph2.5+ (Design) → Ph3 (Breakdown) → Ph4 (Tests) → Ph5 (Code) → Ph5.5 (Security) → Ph5.6 (Code Review) → Ph6 (Verify+a11y+perf) → Ph6.5 (Staging) → Ph7 (Deploy+Retro)
```

### Modo BRAINSTORM (Ideia indefinida)
```
/new-project --brainstorm meu-app
Phase 0 (Brainstorm) → Phase 1 (PRD) → ... → Phase 7 (Deploy)
```

### Modo QUICK (Ágil, sem PRD formal)
```
/new-project --quick meu-app
Ph2 (SDD) → Ph2.05 (Foundation) → Ph3 (Breakdown) → Ph4 (Tests) → Ph5 (Code) → Ph5.5 (Security) → Ph6 (Verify) → Ph7 (Deploy)
```
> Pula Phase 0, Phase 1, Phase 2.1. Direto para SDD com Socratic Gate simplificado.

---

## 💾 SISTEMA DE CHECKPOINTING

> [!IMPORTANT]
> **Projetos podem ser interrompidos.** O workflow salva progresso em `docs/PROJECT-PROGRESS.md` a cada fase.
> Seguir skill `checkpointing-patterns` para detalhes de persistência e resume.

### Arquivo de Controle: `docs/PROJECT-PROGRESS.md`

Criado automaticamente ao iniciar o projeto. Contém:

| Seção | Conteúdo |
|-------|----------|
| Status Geral | Nome, fases, última atualização |
| Project Profile | Tipo, stack, agent, design approach |
| Fases | Checklist de cada phase com artefatos |
| Tasks | Lista de tasks pendentes/concluídas |
| Histórico | Log de ações |

### Retomada: `--resume`

```bash
/new-project --resume
```

**Ao executar `--resume`:**
1. Carrega `docs/PROJECT-PROGRESS.md`
2. Identifica fase pendente
3. **🚨 DESYNC DETECTOR (OBRIGATÓRIO):**
   - Comparar tasks marcadas ✅ em PROJECT-PROGRESS.md com status real no Tracker
   - Se LOCAL=✅ mas TRACKER=Não iniciado → **PARAR e executar sync retroativo**
   - Se TRACKER retorna **0 tasks** mas LOCAL tem tasks ✅ → **DESYNC TOTAL. Executar sync retroativo de TODAS as tasks**
4. **🔗 FLYEE BRIDGE CHECK (OBRIGATÓRIO):**
   - Ler `flyee.json`
   - Se `enabled: true` OU `opted_out: true` → Prosseguir silenciosamente
   - Se `enabled: false` E `opted_out: false` → Perguntar usando skill `project-type-discovery` seção "Flyee Integration"
5. **🎯 OKR GAP DETECTOR (se Flyee habilitado):**
   - Executar `python3 .agent/flyee-bridge/bridge.py --list-okrs`
   - Se 0 OKRs: extrair do PRD/TDD, gerar 1-3 OKRs com bridge.py, validar com usuário
   - Se >= 1 OKR: skip silencioso
6. Continua execução (apenas se sem desync)

> [!CAUTION]
> **DESYNC DETECTOR:** Antes de continuar qualquer trabalho em --resume, o agente DEVE:
> 1. Buscar status de TODAS as tasks marcadas como completas localmente
> 2. Se encontrar desync (local ✅, Tracker ≠ completed) → sync retroativo PRIMEIRO
> 3. Se Tracker retorna **0 tasks** mas projeto tem fases completas → isto é **DESYNC TOTAL**, não "sem desync"
> 4. Só prosseguir após: "Nenhum desync detectado" ou "Desync corrigido"

> [!CAUTION]
> **FLYEE API ERROR HANDLING:**
> - Erro 500/502/503 na API Flyee → **RETRY 1x após 5s**
> - Se retry falhar → **INFORMAR USUÁRIO** com mensagem explícita, não pular silenciosamente
> - 🚫 **PROIBIDO** tratar erro de API como "não bloqueante" e continuar sem sync

> [!IMPORTANT]
> **OKR GAP DETECTOR:** Template de key results deve incluir:
> - **KR de entrega:** Features implementadas vs. planejadas
> - **KR de qualidade:** Cobertura de testes, performance
> - **KR de impacto:** Métricas de negócio do PRD

---

## 🔴 FLUXO COMPLETO

```
DISCOVERY → BRAINSTORM → PRD → SDD → FOUNDATION → REFERÊNCIAS → DESIGN SYSTEM → CONTENT → STITCH → PAGE SPECS → BREAKDOWN → TESTS → IMPLEMENT → SECURITY → CODE REVIEW → VERIFY → STAGING → DEPLOY+RETRO
(TIPO+STACK)  (OPCIONAL) (O QUÊ) (COMO) (README+.env)  (COLETAR)   (TOKENS)   (O QUE DIZ) (PROTÓTIPO) (BLUEPRINT)  (TASKS) (PRIMEIRO) (CÓDIGO)  (OWASP) (CHECKLIST)  (a11y+perf) (HUMANO)  (PROD+RETRO)
```

> **🚦 GATE 0 (Discovery)** é OBRIGATÓRIO e roda ANTES de tudo.
> **📋 Phase 2.05 (Foundation)** gera README, SECURITY, .env.example, INDEX.md, ADR-000 (e openapi.yaml se API).
> **📋 Phase 2.1 (Task Setup)** ocorre entre SDD e REFERÊNCIAS.
> **📋 Phase 5.5/5.6 (Security + Code Review)** obrigatórias antes de Phase 6.

---

## 📋 FASES — Skill Routing

> [!IMPORTANT]
> **PRINCÍPIO:** Cada fase carrega APENAS o skill necessário sob demanda.
> NÃO carregar todos os skills de antemão. Ler o skill ao iniciar cada fase.

### 🚦 Gate 0: PROJECT TYPE DISCOVERY (Obrigatório)

> **Skill:** `project-type-discovery`
> Carregar skill e executar todas as 4 perguntas. AGUARDAR respostas.
>
> **Gate de Saída:** Project Profile salvo em PROJECT-PROGRESS.md
> **Exceção:** `--resume` (já tem profile)

---

### Phase 0: BRAINSTORM (Opcional)

> **Workflow:** `/brainstorm`
> Apenas se `/new-project --brainstorm`.
> Gate de Saída: direção escolhida e validada

---

### Phase 1: PRD (Product Requirements Document)

> **Workflow:** `/prd new`
> Executa workflow completo de PRD com Socratic Gate (12 perguntas).
> Gera `docs/PRD-{nome}.md` usando `prd-template.md` (com YAML frontmatter + Agent Context).
> Registra entry em `docs/INDEX.md` após aprovação.
> Gate de Saída: PRD aprovado pelo humano + entry no INDEX.md

---

### Phase 2: SDD (Software Design Document)

> **Atenção:** `SDD` = Software Design Document. **Não confundir** com `TDD` (Test-Driven Development — Phase 4).
>
> **Workflow:** `/tdd new` + `/tdd validate`  → outputs salvo como `SDD-{nome}.md`
> **Skill extra:** `deployment-procedures` (seção "Environment Strategy")
>
> SDD DEVE incluir:
> - Seção `## 0. Agent Context` preenchida
> - Seção `## Environment Strategy` com tabela dev/staging/prod
> - Se projeto tem API: confirmar se é necessário gerar `docs/api/openapi.yaml` na Phase 2.05
>
> Gera `docs/design/SDD-{nome}.md` usando `sdd-template.md`.
> **Registry:** `document-registry` — registrar entry `SDD-{nome}` no INDEX.md após aprovação.
> Gate de Saída: SDD aprovado + Environment Strategy definida + ADR inicial registrado se houver decisão arquitetural significativa

---

### Phase 2.05: PROJECT FOUNDATION (Auto-gerado)

> **Skill:** `project-foundation` (modo: `new`)
> **Registry:** `document-registry`
>
> Executar o skill `project-foundation` em modo `new`. O skill gerará automaticamente:
> - `README.md`, `.env.example`, `SECURITY.md`, `docs/INDEX.md`, `docs/adr/ADR-000-initial-setup.md`
> - `docs/api/openapi.yaml` — **se projeto tem API** (skill pergunta ao usuário)
>
> Cada artefato gerado é registrado no `docs/INDEX.md` pelo skill `document-registry`.
>
> Gate de Saída: checklist do `project-foundation` 100% marcado

---

### Phase 2.1: TASK SETUP (Tracking desde o início)

> **Skill:** `project-tracking-patterns`
> Criar tasks de tracking para fases 2.45→2.9 no tracker configurado.
>
> **Ações:** Para cada fase de design (2.45, 2.5, 2.65, 2.7, 2.8, 2.9), criar task no tracker.
> **Pulado no modo:** `--quick`
> Gate de Saída: tasks de planejamento criadas no tracker

---

### Phase 2.45: VISUAL REFERENCE COLLECTION

> **Skill:** `ui-ux-discovery`
> Se Gate 0 Pergunta 3 já respondida → usar essa resposta.
> Se não → executar descoberta de referências visuais.
>
> Gate de Saída: abordagem de design definida (referências coletadas OU recomendações aceitas)

---

### Phase 2.5: DESIGN SYSTEM (Tokens)

> **Skills:** `ui-ux-discovery` + `frontend-design`
> Gerar `docs/design/DESIGN-SYSTEM.md` com tokens CSS, tipografia, efeitos visuais.
> Usar `design-system-template.md` como base (já inclui YAML frontmatter + Agent Context).
> **Registry:** `document-registry` — registrar entry `DS-{nome}` no INDEX.md após aprovação.
>
> Gate de Saída: `DESIGN-SYSTEM.md` aprovado pelo usuário + entry atualizada em `docs/INDEX.md`

---

### Phase 2.65: CONTENT STRATEGY

> **Skill:** `content-strategy`
> Definir conteúdo textual para cada página.
>
> Gate de Saída: CONTENT-STRATEGY-{nome}.md aprovado

---

### Phase 2.7: STITCH GENERATION (Opcional)

> **Workflow:** `/stitch`
> Se projeto tem UI e design approach permite geração AI.
>
> Gate de Saída: protótipos validados pelo cliente/usuário

---

### Phase 2.8: PAGE SPECIFICATIONS

> **Skill:** `page-specifications`
> Detalhar cada página: layout, seções, componentes, estados, responsividade.
>
> Gate de Saída: PAGE-SPECs aprovados

---

### Phase 2.9: ANALYTICS STRATEGY

> **Skill:** `analytics-strategy`
> Definir stack, eventos por página, funnels, feature flags.
>
> **Pulado se:** POC interno sem necessidade de métricas
> Gate de Saída: eventos mapeados, SDD + PAGE-SPECs atualizados

---

### Phase 3: BREAKDOWN (Tasks)

> **Workflow:** `/tdd breakdown`
> **Skill:** `project-tracking-patterns`
>
> Gerar tasks a partir do SDD e criar no tracker.
> Gate de Saída: tasks criadas no tracker

### Phase 3.1: OKR AUTO-CREATION (se Flyee habilitado)

> **Executa automaticamente após Phase 3.**
> Extrai 1-3 OKRs do PRD/SDD e cria via bridge.
>
> 1. Executar `python3 .agent/flyee-bridge/bridge.py --list-okrs`
> 2. Se 0 OKRs: extrair objetivos do PRD/TDD, gerar com `--create-okr`
>    - **KR de entrega:** Features implementadas vs. planejadas
>    - **KR de qualidade:** Cobertura de testes, performance
>    - **KR de impacto:** Métricas de negócio do PRD
> 3. Se >= 1 OKR: skip silencioso
> 4. Validar com usuário
>
> Gate de Saída: OKRs criados ou confirmado skip

---

### Phase 3.5: SETUP BASE (Infraestrutura)

> **Skill:** `project-setup`
> Inicializar projeto, configurar test runner, separar ambientes.
>
> Gate de Saída: projeto inicializado, `npm test` roda, ambientes separados

---

### Phase 4: TDD METODOLOGIA (Tests First)

> **Skill:** `tdd-workflow` (inclui Anti-Mock Validation + E2E Smoke Test)
> **Skill:** `design-system-enforcement` (para tasks com UI — inclui UI Spec Reading Gate)
>
> Ciclo por task: RED (teste falha) → SPEC READING → GREEN (código mínimo com styling premium) → REFACTOR
>
> **Gates obrigatórios por task:**
> - Anti-Mock Check (skill `tdd-workflow` §11)
> - UI Spec Reading Gate (skill `design-system-enforcement` §UI Spec Reading Gate)
> - Sync tracker após cada task (skill `project-tracking-patterns`)
>
> Gate de Saída: todos testes passando, sync concluído

---

### Phase 5: IMPLEMENTAÇÃO (5.0 → 5.4)

> **Sub-fases obrigatórias:**

| Sub-fase | Skill | O que |
|----------|-------|-------|
| 🔴 **5.0 Context Gathering** | `context-gathering-patterns` | Ler Task/PRD/TDD e consultar Resources |
| **5.1 Backend/Lógica** | `tdd-workflow` | Implementar lógica, DB queries, APIs |
| **5.2 UI Components** | `design-system-enforcement`, `integration-completeness` | Componentes com styling premium + Data Integration Scan |
| **5.3 Styling Validation** | `design-system-enforcement` (§Premium Styling), `ui-validation` | Verificar e ajustar styling. **Apenas fine-tuning** — styling principal foi aplicado no GREEN |
| **5.4 Task Completion** | `project-tracking-patterns` | Executar `/task-complete` para atualizar status das tasks no Flyee |

> [!CAUTION]
> **VERIFICAÇÃO OBRIGATÓRIA (antes de Phase 5.5):**
> ```
> [ ] 5.0 Context Gathering concluído (checklist preenchido)
> [ ] 5.1 Backend/Lógica implementado
> [ ] 5.2 UI Components criados + Data Integration Scan limpo
> [ ] 5.3 Styling validado (glassmorphism, shadows, animations verificados)
> [ ] 5.4 /task-complete executado
> ```
> ❌ Se QUALQUER sub-fase pendente → NÃO PROSSEGUIR

---

### Phase 5.5: SECURITY REVIEW

> **Skill:** `security-auditor` (consultar `.agent/agents/security-auditor.md`)
>
> | Verificação | Ação |
> |-------------|------|
> | OWASP Top 10 | Checklist item por item |
> | Dependências vulneráveis | `npm audit` / `pip-audit` / `trivy` |
> | Secrets em código | `grep -r "secret\|password\|key" src/` |
> | Auth/Authz | Endpoints protegidos verificados |
> | CORS/CSP | Headers configurados corretamente |
> | Input validation | Todos endpoints validam entrada |
>
> **Issues encontrados:** Registrar em `docs/adr/ADR-{NNN}-security-decision.md`
> Gate de Saída: relatório limpo OU issues documentados em ADR + aprovados pelo usuário

---

### Phase 5.6: CODE REVIEW GATE

> **Skill:** `code-review-checklist`
>
> ```
> [ ] Sem TODOs/FIXMEs pendentes na base de código
> [ ] Sem mock data ou stubs em rotas de produção
> [ ] Cobertura >= 80% confirmada
> [ ] Naming consistente com glossario do SDD
> [ ] Nenhum console.log / print debug no código de produção
> [ ] Imports limpos (sem módulos não utilizados)
> ```
>
> Gate de Saída: checklist 100% preenchido

---

### Phase 6: VERIFICAÇÃO (6.0 + 6.1 + 6.2)

> **Skills:** `tdd-workflow` (§E2E Core Loop Smoke Test), `web-design-guidelines` (§a11y), `performance-profiling`

| Sub-fase | O que verificar | Critério |
|----------|-----------------|----------|
| **6.0 Coverage + E2E** | Cobertura e fluxo principal | Coverage ≥ 80% + E2E passando |
| **6.1 Accessibility (a11y)** | WCAG AA audit | Zero critical violations |
| **6.2 Performance Baseline** | Lighthouse (web) ou equivalente (mobile) | Score ≥ 90 por categoria |

> | Resultado | Ação |
> |-----------|------|
> | Coverage ≥ 80% | ✅ Prosseguir |
> | Coverage < 80% | ❌ Adicionar testes |
> | E2E Smoke FALHOU | ❌ CORRIGIR — fluxo principal broken |
> | a11y critical violations | ❌ CORRIGIR antes de prosseguir |
> | Perf baseline < 90 | ⚠️ Documentar em ADR e validar com usuário |
>
> Gate de Saída: coverage ≥ 80% + E2E funcional + a11y sem critical violations + performance baseline documentado

---

### Phase 6.5: STAGING VALIDATION

> Fase separada do deploy em produção. **Obrigatória** antes de Phase 7.
>
> 1. Deploy em ambiente de staging
> 2. Executar smoke tests em staging
> 3. Validação com usuário / stakeholder chave
> 4. Documentação de issues encontrados
>
> Gate de Saída: aprovação explícita do usuário antes de prosseguir para produção

---

### Phase 7: DEPLOY (7.1 → 7.7)

> **Skill:** `deployment-procedures` (§Environment Separation, §Pre-Deploy)
> **Workflow:** `/deploy`

| Sub-fase | O que |
|----------|-------|
| 7.1 Environment Discovery | Perguntar ambientes ao usuário (dev/staging/prod) |
| 7.2 Pre-flight Checks | Build, testes, env vars verificados |
| 7.3 Deploy | Executar deploy na plataforma |
| 7.4 Verify | Health check, logs, key flows |
| 7.5 Tech Documentation | Publicar docs técnicos no Flyee (se habilitado) |
| 7.6 User Documentation | Publicar guias de uso no Flyee (se habilitado) |
| **7.7 Post-Deploy Retrospective** | **Registrar aprendizados em `docs/RETRO-{nome}-v1.md`** |

> Gate de Saída: deploy bem-sucedido + documentação publicada + retrospectiva registrada

---

## 🔴 REGRAS CRÍTICAS

1. **Aprovação humana obrigatória** em PRD e SDD
2. **Testes ANTES do código** (TDD Metodologia)
3. **Cobertura ≥ 80%** antes de deploy
4. **Rastreabilidade:** SDD referencia PRD, Tasks referenciam SDD, via `docs/INDEX.md`
5. **Um projeto = Um PRD = Um SDD principal**
6. **Ambientes obrigatórios:** SEMPRE perguntar sobre dev/staging/prod antes de deploy (Phase 7.1)
7. **📚 DOCUMENTAÇÃO PARA DEVS E USUÁRIOS** - Ao final do projeto (Phase 7.5 + 7.6), publicar docs
8. **📋 TRACKING DESDE O INÍCIO** - Tasks de planejamento (Phase 2.5–2.9) criadas na Phase 2.1
9. **🔒 SECURITY GATE** - Phase 5.5 e 5.6 obrigatórias antes de Phase 6, sem exceções
10. **♿ ACESSIBILIDADE** - Phase 6.1 obrigatória; WCAG AA mínimo para projetos com UI
11. **📊 RETROSPECTIVA** - Phase 7.7 obrigatória após cada deploy de versão

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
| `/deploy` | Phase 7 |

| Workflows Relacionados | Quando Usar |
|------------------------|-------------|
| `/discovery` | Alternativa ágil (equivale a `--quick` + Tracker) |
| `/brainstorm` | Exploração standalone sem projeto |
| `/new-task` | Nova feature em projeto existente |
| `/document` | Documentar projeto legado |

---

## 📁 Estrutura de Arquivos Gerados

### Modo Completo
```
projeto/
├── README.md                           # Phase 2.05
├── .env.example                        # Phase 2.05
├── SECURITY.md                         # Phase 2.05
├── CHANGELOG.md                        # Phase 7
├── docs/
│   ├── INDEX.md                        # Phase 2.05 (Document Registry)
│   ├── PRD-{nome}.md                   # Phase 1
│   ├── RETRO-{nome}-v1.md              # Phase 7.7
│   ├── adr/
│   │   └── ADR-000-initial-setup.md    # Phase 2.05
│   ├── api/
│   │   └── openapi.yaml                # Phase 2.05 (se projeto tem API)
│   └── design/
│       ├── SDD-{nome}.md               # Phase 2 (Software Design Document)
│       ├── DESIGN-SYSTEM.md            # Phase 2.5
│       ├── PAGE-SPEC-{pagina}.md       # Phase 2.8
│       └── CONTENT-{pagina}.md         # Phase 2.65
├── {nome}.md                           # Plan file (Phase 3)
├── tests/                              # Phase 4
│   ├── unit/
│   └── integration/
└── src/                                # Phase 5
```

### Modo --quick
```
projeto/
├── README.md                           # Phase 2.05
├── .env.example                        # Phase 2.05
├── SECURITY.md                         # Phase 2.05
├── docs/
│   ├── INDEX.md                        # Phase 2.05
│   ├── adr/
│   └── design/
│       └── SDD-{nome}.md               # Phase 2 (sem PRD)
├── {nome}.md
├── tests/
└── src/
```

---

## 📋 Comparativo de Modos

| Aspecto | Completo | --brainstorm | --quick |
|---------|----------|--------------| --------|
| Phase 0 (Brainstorm) | ❌ | ✅ | ❌ |
| Phase 1 (PRD) | ✅ | ✅ | ❌ |
| Phase 2 (SDD) | ✅ | ✅ | ✅ |
| Phase 2.05 (Foundation) | ✅ | ✅ | ✅ |
| Phase 2.1 (Task Setup) | ✅ | ✅ | ❌ |
| Phase 5.5 (Security Review) | ✅ | ✅ | ✅ |
| Phase 5.6 (Code Review) | ✅ | ✅ | ✅ |
| Phase 6.1 (a11y) | ✅ | ✅ | ✅ |
| Phase 6.2 (Performance) | ✅ | ✅ | ✅ |
| Phase 6.5 (Staging) | ✅ | ✅ | ❌ |
| Phase 7.7 (Retrospective) | ✅ | ✅ | ❌ |
| Socratic Gate | 12 perguntas | 12 perguntas | 5 perguntas |
| Documentação | PRD + SDD | PRD + SDD | SDD only |
| Tempo estimado | Maior | Maior | Menor |
| Recomendado para | Projetos formais | Ideias indefinidas | MVPs rápidos |

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

# Continuar de SDD já aprovado
/new-project --from-sdd docs/design/SDD-meu-app.md

# Importar de proposta comercial aprovada
/new-project --from-demand "Proposta App Fitness"

# Ver status do projeto
/new-project status
```
