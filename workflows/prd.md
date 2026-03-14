---
description: Create Product Requirements Document (PRD). Captures problem, personas, requirements, MVP scope, and roadmap in structured format.
---

# /prd - Product Requirements Document Workflow

$ARGUMENTS

---

## 🎯 PROPÓSITO

Workflow para criação de **PRD (Product Requirements Document)** - documento de requisitos de produto que:
1. Define o problema e contexto de negócio
2. Identifica personas e stakeholders
3. Captura requisitos funcionais e não-funcionais
4. Estabelece escopo do MVP
5. Cria roadmap de features

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   DISCOVERY  │───▶│   DOCUMENT   │───▶│   VALIDATE   │───▶│   APPROVE    │
│  (Socratic)  │    │    (PRD)     │    │  (Checklist) │    │   (Human)    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

---

## 🧩 SUBCOMMANDS

| Comando | Ação |
|---------|------|
| `/prd new [nome]` | Cria novo PRD a partir do template |
| `/prd validate [arquivo]` | Valida completude do PRD |
| `/prd status` | Mostra status dos PRDs do projeto |

---

## 🔴 FLUXO

### Phase 1: DISCOVERY (`/prd new`)

#### Trigger
```
/prd new [nome-do-projeto]
```

#### Agentes Envolvidos
- `product-owner` - Lead do discovery
- `project-planner` - Estruturação

#### Skill
- `brainstorming` - Socratic Gate obrigatório

#### Socratic Gate (3 NÍVEIS - OBRIGATÓRIO)

**Nível 1: Problema e Contexto**
| # | Pergunta | Campo PRD |
|---|----------|-----------|
| 1 | 🎯 Qual problema estamos resolvendo? | Problem Statement |
| 2 | 🌍 Qual o contexto de mercado/negócio? | Market Context |
| 3 | 💡 Qual a visão de sucesso? | Vision |
| 4 | 📊 Como mediremos o sucesso? | Success Metrics |

**Nível 2: Usuários e Jornadas**
| # | Pergunta | Campo PRD |
|---|----------|-----------|
| 5 | 👥 Quem são os principais usuários? (personas) | Target Users |
| 6 | 🎭 Quais os perfis de cada persona? | User Personas |
| 7 | 🗺️ Qual a jornada atual do usuário? | Current Journey |
| 8 | ⚠️ Quais são as principais frustrações? | Pain Points |

**Nível 3: Requisitos e Escopo**
| # | Pergunta | Campo PRD |
|---|----------|-----------|
| 9 | 📦 Quais funcionalidades são essenciais (MVP)? | MVP Features |
| 10 | 🚀 O que pode ficar para fases futuras? | Future Features |
| 11 | 🔐 Requisitos de segurança/compliance? | Non-Functional |
| 12 | ⏰ Qual o prazo esperado para MVP? | Timeline |

#### Ações
1. **Executar Socratic Gate** completo (todas as perguntas)
2. **Copiar template** de `.agent/templates/prd-template.md`
3. **Criar arquivo** em `docs/PRD-{nome-do-projeto}.md`
4. **Preencher PRD** com respostas coletadas

#### Output Esperado
```
[OK] PRD criado: docs/PRD-{nome}.md
[OK] Status: Rascunho
[NEXT] Execute /prd validate docs/PRD-{nome}.md
```

---

### Phase 2: VALIDATE (`/prd validate`)

#### Trigger
```
/prd validate docs/PRD-{nome}.md
```

#### Agente Envolvido
- `product-owner` - Validação de completude

#### Validações Realizadas

| Categoria | Verificação |
|-----------|-------------|
| **Problema** | Problem Statement está claro e específico? |
| **Personas** | Pelo menos 2 personas definidas? |
| **MVP** | Features do MVP claramente delimitadas? |
| **Métricas** | KPIs de sucesso definidos? |
| **Riscos** | Riscos identificados com mitigações? |

#### Output Esperado
```markdown
## PRD Validation Report

### ✅ Seções Completas
- [x] Problem Statement
- [x] User Personas
- [x] MVP Features

### ⚠️ Itens Incompletos
- [ ] Success Metrics não quantificados
- [ ] Timeline sem datas específicas

### ❌ Seções Faltando
- [ ] Competitive Analysis

### 📊 Score: 80% Completo

### Recomendação
[Próximos passos para completar]
```

---

### Phase 3: APPROVE (Humano)

#### Trigger
Após validação, o **humano** deve:

1. **Revisar** o PRD completo
2. **Ajustar** itens incompletos
3. **Aprovar** marcando no documento:
   ```markdown
   - [x] **Aprovado para Discovery Técnico**
   ```

#### 🔴 REGRA DE OURO
> A IA **NÃO** pode prosseguir para `/tdd` ou `/discovery` sem aprovação humana do PRD.

---

### Phase 4: NEXT STEPS

Após aprovação do PRD, sugerir:

```
🎉 PRD APROVADO!

Próximos passos disponíveis:

1. /tdd new → Technical Design Document (RECOMENDADO - define arquitetura)
2. /discovery → Brainstorm técnico + User Stories + Tasks no Flyee
3. /demand → Gerar proposta comercial (se for projeto cliente)
4. /new-project → Fluxo completo automatizado (PRD já aprovado → TDD → Testes → Código)
```

### Phase 4.1: RASTREABILIDADE (Obrigatório)

> [!IMPORTANT]
> **Após criar o TDD**, o documento deve referenciar este PRD:
> ```markdown
> PRD Fonte: docs/PRD-{nome}.md
> ```

**Regra de Ouro:** Todo TDD DEVE ter um PRD aprovado como fonte.

---

## 📁 Estrutura de Arquivos

```
projeto/
├── docs/
│   ├── PRD-meu-produto.md          # PRD do projeto
│   └── design/
│       └── TDD-meu-produto.md      # TDD (gerado após PRD)
```

---

## 🔄 Status Lifecycle

```
[Rascunho] → [Em Revisão] → [Aprovado] → [Em Discovery] → [Concluído]
```

| Status | Significado |
|--------|-------------|
| Rascunho | Sendo escrito, discovery em andamento |
| Em Revisão | Validação e ajustes finais |
| Aprovado | Pronto para próximas fases |
| Em Discovery | Gerando TDD/Discovery técnico |
| Concluído | Projeto iniciado |

---

## 🔗 INTEGRAÇÃO COM OUTROS WORKFLOWS

| De | Para | Como |
|----|------|------|
| `/prd` | `/discovery` | PRD alimenta brainstorm com contexto |
| `/prd` | `/tdd` | Seções de MVP → Fluxos técnicos |
| `/prd` | `/demand` | Escopo → Estimativa comercial |

---

## 🔴 REGRAS CRÍTICAS

1. **Socratic Gate é OBRIGATÓRIO** - Não pular perguntas
2. **Humano aprova PRD** - Nunca auto-aprovar
3. **PRD antes de TDD** - PRD define O QUE, TDD define COMO
4. **Um produto = Um PRD** - Não misturar produtos/projetos

---

## Usage Examples

```bash
# Criar PRD para novo produto
/prd new meu-app-fitness

# Validar PRD existente
/prd validate docs/PRD-meu-app-fitness.md

# Ver status de todos os PRDs
/prd status

# Fluxo completo
/prd new ecommerce-platform
# [Responder perguntas do Socratic Gate]
# [Revisar PRD gerado]
/prd validate docs/PRD-ecommerce-platform.md
# [Ajustar conforme necessário]
# [Aprovar manualmente no documento]
/discovery  # Continua para discovery técnico
```
