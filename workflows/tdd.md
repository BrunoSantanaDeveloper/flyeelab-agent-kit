---
description: Workflow completo de TDD (Technical Design Document). Cria, valida e transforma TDD em tarefas executáveis.
---

# /tdd - Technical Design Document Workflow

$ARGUMENTS

---

## 🔴 WORKFLOW OVERVIEW

O fluxo TDD segue o padrão **RPI (Research, Plan, Implement)** com validação humana obrigatória.

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   DISCOVERY  │───▶│   VALIDATE   │───▶│   APPROVE    │───▶│  IMPLEMENT   │
│  (IA + Human)│    │ (IA Review)  │    │   (Human)    │    │  (IA Code)   │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

---

## 🧩 SUBCOMMANDS

| Comando | Ação |
|---------|------|
| `/tdd new [nome]` | Cria novo TDD a partir do template |
| `/tdd validate [arquivo]` | Valida completude do TDD |
| `/tdd breakdown [arquivo]` | Transforma TDD em tarefas |
| `/tdd status` | Mostra status dos TDDs do projeto |

---

## Phase 1: DISCOVERY (`/tdd new`)

### Trigger
```
/tdd new [nome-da-feature]
```

### Ações
1. **Verificar PRD existente** - Buscar `docs/PRD-*.md` relacionado
2. **Copiar template** de `.agent/templates/tdd-template.md`
3. **Criar arquivo** em `docs/design/TDD-{nome-da-feature}.md`
4. **Preencher campo obrigatório:**
   ```markdown
   PRD Fonte: docs/PRD-{nome}.md
   ```
5. **Iniciar brainstorming** usando skill `brainstorming`

### Agentes Envolvidos
- `project-planner` - Estruturação inicial
- `product-owner` - Definição de MVP

### Socratic Gate (OBRIGATÓRIO)
Antes de preencher o TDD, perguntar:

1. 🎯 **Qual problema estamos resolvendo?** (referência: PRD seção 2.1)
2. 👥 **Quem são os usuários afetados?** (referência: PRD seção 3)
3. 📦 **O que é MVP vs. nice-to-have?** (referência: PRD seção 6.1)
4. ⚠️ **Quais os riscos conhecidos?** (referência: PRD seção 8)
5. 🔗 **Quais integrações externas são necessárias?**

> [!TIP]
> Se o PRD já foi aprovado, use-o como base para responder as perguntas.

### Output Esperado
```
[OK] TDD criado: docs/design/TDD-{nome}.md
[OK] PRD Fonte: docs/PRD-{nome}.md
[OK] Status: Rascunho
[NEXT] Execute /tdd validate docs/design/TDD-{nome}.md
```

---

## Phase 2: VALIDATE (`/tdd validate`)

### Trigger
```
/tdd validate docs/design/TDD-{nome}.md
```

### Ações
1. **Ler TDD** completo
2. **Verificar completude** usando skill `tdd-validation`
3. **Reportar gaps** e itens INDEFINIDOS

### Agente Envolvido
- `tdd-reviewer` - Análise de completude

### Validações Realizadas

| Categoria | Verificação |
|-----------|-------------|
| **Estrutura** | Todas as seções obrigatórias existem? |
| **MVP** | Há itens DEFINIDO suficientes para MVP? |
| **Bloqueadores** | Há itens INDEFINIDO que bloqueiam? |
| **Arquitetura** | TDD alinha com ARCHITECTURE.md? |
| **Riscos** | Riscos identificados têm mitigação? |

### Output Esperado
```markdown
## TDD Validation Report

### ✅ Seções Completas
- [x] Contexto e Motivação
- [x] Glossário
- [x] Fluxo Técnico

### ⚠️ Itens Indefinidos
- [ ] Tratamento de Erros (Fase 3)
- [ ] Estratégia de Retry

### ❌ Seções Faltando
- [ ] Webhooks não documentados

### 📊 Score: 75% Completo

### 🔴 BLOQUEADORES
1. Definir estratégia de retry antes de implementar

### Recomendação
Resolver bloqueadores antes de aprovar.
```

---

## Phase 3: APPROVE (Humano)

### Trigger
Após validação, o **humano** deve:

1. **Revisar** o relatório de validação
2. **Resolver** itens INDEFINIDOS (ou movê-los para futuro)
3. **Aprovar** marcando o checkbox no TDD:
   ```markdown
   - [x] **Aprovado para Implementação**
   ```

### 🔴 REGRA DE OURO
> A IA **NÃO** pode prosseguir para implementação sem aprovação humana explícita.

---

## Phase 4: BREAKDOWN (`/tdd breakdown`)

### Trigger
```
/tdd breakdown docs/design/TDD-{nome}.md
```

### Pré-condição
- TDD deve estar marcado como `Aprovado`
- Nenhum item INDEFINIDO bloqueando MVP

### Ações
1. **Ler TDD aprovado**
2. **Extrair tarefas** da seção "Detalhamento da Solução"
3. **Criar plan file** `{feature-name}.md` no root
4. **Atribuir agentes** a cada tarefa

### Agente Envolvido
- `project-planner` - Quebra em tarefas

### Output Esperado
```markdown
## Task Breakdown: {Feature Name}

**Source of Truth:** docs/design/TDD-{nome}.md
**Status:** Ready for Implementation

### Tasks

- [ ] **Task 1: Setup Credenciais** → `devops-engineer`
  - Ref: TDD Fase 1
  - Verify: `.env.example` atualizado

- [ ] **Task 2: Criar Entidade** → `backend-specialist`
  - Ref: TDD Fase 2
  - Verify: Endpoint POST funcionando

[PARALLELIZABLE]
- [ ] **Task 3: Frontend Form** → `frontend-specialist`
- [ ] **Task 4: Testes Unitários** → `test-engineer`
```

---

## Phase 5: TDD METODOLOGIA (Testes Primeiro)

> [!IMPORTANT]
> **Antes de implementar código, escrever testes.**
> Skill de referência: `tdd-workflow`

### Trigger
Após breakdown aprovado e antes do `/create`:
```
/test [task]
```

### Ciclo RED-GREEN-REFACTOR

| Fase | Ação | Verificação |
|------|------|-------------|
| 🔴 RED | Escrever teste que falha | Teste falha corretamente |
| 🟢 GREEN | Implementar código mínimo | Teste passa |
| 🔵 REFACTOR | Melhorar código | Testes continuam passando |

### Para CADA Task do Breakdown:
1. **Escrever testes** baseados nos critérios de aceite do TDD
2. **Implementar** código mínimo para passar
3. **Refatorar** mantendo testes verdes
4. **Verificar cobertura** >= 80%

---

## Phase 6: IMPLEMENT

### Trigger
Após testes escritos (Phase 5 concluída):
```
/create
```
ou
```
/orchestrate
```

### Regras de Implementação
1. **Ler TDD** a cada nova task
2. **Rodar testes** antes de cada commit
3. **Não inventar** features não documentadas
4. **Seguir** exatamente o que está DEFINIDO
5. **Ignorar** o que está FORA DE ESCOPO

### Verificação de Cobertura (GATE)

> [!CAUTION]
> **Cobertura mínima:** 80% antes de considerar task completa.

```bash
/test coverage
```

Se cobertura < 80%:
1. Identificar áreas não cobertas
2. Adicionar testes faltantes
3. Repetir verificação

---

## 📁 Estrutura de Arquivos

```
projeto/
├── docs/
│   └── design/
│       ├── TDD-payment-integration.md
│       └── TDD-user-authentication.md
├── payment-integration.md        # Plan file (após breakdown)
└── user-authentication.md        # Plan file (após breakdown)
```

---

## 🔄 Status Lifecycle

```
[Rascunho] → [Em Revisão] → [Aprovado] → [Em Implementação] → [Concluído]
```

| Status | Significado |
|--------|-------------|
| Rascunho | Sendo escrito, não validado |
| Em Revisão | Validação em andamento |
| Aprovado | Pronto para implementação |
| Em Implementação | Tasks sendo executadas |
| Concluído | Todas as tasks finalizadas |

---

## 🔴 REGRAS CRÍTICAS

1. **TDD é Imutável após aprovação** - Não modificar sem nova revisão
2. **Humano aprova, IA executa** - Nunca auto-aprovar
3. **INDEFINIDO = BLOQUEADOR** - Resolver antes de implementar
4. **Uma feature = Um TDD** - Não misturar features

---

## Usage Examples

```bash
# Criar novo TDD para integração de pagamentos
/tdd new payment-integration

# Validar o TDD criado
/tdd validate docs/design/TDD-payment-integration.md

# Após aprovação humana, quebrar em tarefas
/tdd breakdown docs/design/TDD-payment-integration.md

# Ver status de todos os TDDs
/tdd status
```
