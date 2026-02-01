---
description: Workflow unificado para novo projeto. Orquestra PRD → TDD Técnico → TDD Metodologia → Implementação → Deploy. Fluxo completo com checkpointing.
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

### Phase 3: BREAKDOWN - Tarefas

**Objetivo:** Quebrar TDD em tarefas executáveis.

**Trigger:**
```
TDD aprovado → Automático
```

**Agentes Envolvidos:**
- `project-planner` - Quebra em tarefas

**Ações:**
1. Executar `/tdd breakdown docs/design/TDD-{nome}.md`
2. Gerar arquivo de plano `{nome}.md`
3. Criar tasks no Notion (se disponível)

**Output:**
```
Tasks criadas:
- [ ] Task 1: Setup Infraestrutura → devops-engineer
- [ ] Task 2: Entidades principais → backend-specialist
- [ ] Task 3: UI/Componentes → frontend-specialist
...
```

---

### Phase 4: TDD METODOLOGIA - Testes Primeiro

**Objetivo:** Escrever testes ANTES do código.

**Trigger:**
```
Breakdown concluído → Automático
```

**Skill de Referência:** `tdd-workflow`

**Agentes Envolvidos:**
- `test-engineer` - Geração de testes
- Especialistas de domínio conforme task

**Ciclo para CADA Task:**

| Fase | Ação | Verificação |
|------|------|-------------|
| 🔴 RED | `/test [task]` - Escrever teste que falha | Teste falha corretamente |
| 🟢 GREEN | Implementar código mínimo | Teste passa |
| 🔵 REFACTOR | Melhorar código | Testes continuam passando |

**Ações:**
1. Para cada task do breakdown:
   - Gerar testes baseados nos critérios de aceite
   - Verificar que testes falham (RED)
   - Implementar código mínimo (GREEN)
   - Refatorar mantendo verde (REFACTOR)
2. Registrar progresso no Notion (se aplicável)

---

### Phase 5: IMPLEMENTAÇÃO - Código

**Objetivo:** Implementar todas as features.

**Trigger:**
```
Testes escritos → Automático
```

**Agentes Envolvidos:**
- `app-builder` - Orquestração
- `database-architect` - Schema
- `backend-specialist` - API
- `frontend-specialist` - UI

**Ações:**
1. Executar `/create` ou `/orchestrate`
2. Seguir estritamente o TDD
3. Rodar testes a cada mudança
4. Atualizar progresso

**Regras:**
- ✅ Ler TDD a cada nova task
- ✅ Rodar testes antes de cada commit
- ❌ Não inventar features não documentadas
- ❌ Não implementar itens FORA DE ESCOPO

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

**Ações:**
1. Rodar checklist final: `python .agent/scripts/checklist.py .`
2. Iniciar preview: `auto_preview.py`
3. Apresentar URL ao usuário
4. Se aprovado, deploy

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
