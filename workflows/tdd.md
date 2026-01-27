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
1. **Copiar template** de `.agent/templates/tdd-template.md`
2. **Criar arquivo** em `docs/design/TDD-{nome-da-feature}.md`
3. **Iniciar brainstorming** usando skill `brainstorming`

### Agentes Envolvidos
- `project-planner` - Estruturação inicial
- `product-owner` - Definição de MVP

### Socratic Gate (OBRIGATÓRIO)
Antes de preencher o TDD, perguntar:

1. 🎯 **Qual problema estamos resolvendo?**
2. 👥 **Quem são os usuários afetados?**
3. 📦 **O que é MVP vs. nice-to-have?**
4. ⚠️ **Quais os riscos conhecidos?**
5. 🔗 **Quais integrações externas são necessárias?**

### Output Esperado
```
[OK] TDD criado: docs/design/TDD-{nome}.md
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

## Phase 5: IMPLEMENT

### Trigger
Após breakdown aprovado, usar:
```
/create
```
ou
```
/orchestrate
```

### Regras de Implementação
1. **Ler TDD** a cada nova task
2. **Não inventar** features não documentadas
3. **Seguir** exatamente o que está DEFINIDO
4. **Ignorar** o que está FORA DE ESCOPO

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
