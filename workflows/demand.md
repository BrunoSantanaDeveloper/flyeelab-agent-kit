---
description: Levantamento de demanda comercial. Analisa projeto, estima esforço/valor, gera proposta no Flyee. Após aprovação, alimenta /discovery.
skills: document-registry
---

# /demand - Levantamento de Demanda Comercial

$ARGUMENTS

---

## 🎯 PROPÓSITO

Workflow para **levantamento de demanda comercial** que:
1. Analisa projeto existente (se houver)
2. Estima esforço, tempo e valor
3. Gera proposta estruturada no Flyee
4. Após aprovação, alimenta automaticamente o `/discovery`

```
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│  ANÁLISE   │───▶│ LEVANTAMENTO│───▶│  PROPOSTA  │───▶│  APROVAÇÃO │───▶│ /discovery │
│  (Projeto) │    │  (Esforço) │    │  (Flyee)  │    │  (Humana)  │    │ (Técnico)  │
└────────────┘    └────────────┘    └────────────┘    └────────────┘    └────────────┘
```

---

## 🔴 FLUXO

### Fase 0: PRE-FLIGHT CHECK (Obrigatório)

**Trigger:** Início do comando

**Ações:**
1. Buscar database "Propostas Comerciais" no Flyee via MCP
2. Se **NÃO existir**:
   ```
   ⚠️ DATABASE NÃO ENCONTRADO
   
   Crie manualmente o database "Propostas Comerciais" no Flyee com as propriedades:
   
   | Propriedade | Tipo | Opções |
   |-------------|------|--------|
   | Nome | Title | - |
   | Status | Status | Rascunho, Em Análise, Aprovado, Rejeitado |
   | Cliente | Text | - |
   | Prazo Desejado | Date | - |
   | Faixa Investimento | Select | Até 5k, 5k-15k, 15k-50k, 50k+ |
   | Valor Proposta | Number | - |
   | Horas Estimadas | Number | - |
   | Complexidade | Select | Baixa, Média, Alta, Muito Alta |
   | Qtd Features | Number | - |
   | Qtd Telas | Number | - |
   | Stack | Multi-select | - |
   | Risco | Select | Baixo, Médio, Alto |
   | Tipo Projeto | Select | Novo, Evolução, Correção |
   | Link Projeto | URL | - |
   | Responsável | People | - |
   
   Após criar, execute /demand novamente.
   ```
3. Se **existir mas faltar propriedades**, listar quais faltam e solicitar criação manual
4. Se **OK**, prosseguir para Fase 1

> ℹ️ **Nota Técnica:** Os scripts de automação (`parse_user_stories.py`, `prepare_tracker_updates.py`) agora são genéricos e exigem argumentos (`--input`, `--database-id`, `--epic`) quando executados manualmente.

---

### Fase 1: COLETA DE INFORMAÇÕES

**Trigger:** Pre-flight OK

**Agente Lead:** `product-owner`

**Perguntas Obrigatórias:**

| # | Pergunta | Campo Flyee |
|---|----------|--------------|
| 1 | Qual o nome do cliente/projeto? | Cliente |
| 2 | Qual o tipo de projeto? (Novo/Evolução/Correção) | Tipo Projeto |
| 3 | Existe código ou documentação existente? (link) | Link Projeto |
| 4 | Qual o prazo desejado pelo cliente? | Prazo Desejado |
| 5 | Qual a faixa de investimento disponível? | Faixa Investimento |
| 6 | Descreva brevemente o que precisa ser feito | (corpo) |

---

### Fase 2: ANÁLISE DO PROJETO (Se houver código/docs existentes)

**Trigger:** Link de projeto fornecido OU projeto local identificado

**Agentes:**

| Agente | Responsabilidade |
|--------|------------------|
| `backend-specialist` | Analisar código backend, APIs, banco |
| `frontend-specialist` | Analisar código frontend, componentes, telas |
| `security-auditor` | Identificar riscos e débitos técnicos |
| `orchestrator` | Consolidar análise |

**Ações:**
1. Ler SDD existente (se houver em `docs/design/SDD-*.md`)
2. Analisar estrutura do projeto:
   - Identificar stack tecnológica
   - Contar telas/páginas existentes
   - Contar endpoints/features
   - Avaliar complexidade do código
3. Identificar impactos da nova demanda:
   - O que precisa ser criado do zero?
   - O que precisa ser modificado?
   - Quais integrações são afetadas?
4. Avaliar riscos:
   - Débitos técnicos existentes
   - Dependências desatualizadas
   - Complexidade de integração

**Output:** Relatório de análise técnica

---

### Fase 3: ESTIMATIVA DE ESFORÇO

**Trigger:** Após análise (ou após Fase 1 se projeto novo)

**Agente Lead:** `project-planner`

**Skill:** `plan-writing`

**Metodologia:**

1. **Quebrar em Tasks:**
   - Listar todas as funcionalidades necessárias
   - Agrupar por área (Backend, Frontend, Infra, etc.)

2. **Estimar por Task (T-shirt sizing):**

   | Size | Horas | Descrição |
   |------|-------|-----------|
   | XS | 2h | Ajuste simples, config |
   | S | 4h | Feature pequena, CRUD simples |
   | M | 8h | Feature média, integração |
   | L | 16h | Feature complexa, múltiplos componentes |
   | XL | 32h+ | Epic, requer quebra |

3. **Calcular Totais:**
   - Horas totais = Soma de todas as tasks
   - Aplicar fator de risco:
     - Risco Baixo: x1.1
     - Risco Médio: x1.3
     - Risco Alto: x1.5

4. **Classificar Complexidade:**

   | Horas Totais | Complexidade |
   |--------------|--------------|
   | < 20h | Baixa |
   | 20-60h | Média |
   | 60-150h | Alta |
   | > 150h | Muito Alta |

---

### Fase 4: CÁLCULO DE VALOR

**Trigger:** Após estimativa de esforço

**Agente Lead:** `orchestrator`

**Fórmula Base:**

```
Valor = Horas Estimadas × Valor Hora Base × Fator Complexidade × Fator Urgência
```

**Parâmetros:**

| Parâmetro | Valores |
|-----------|---------|
| Valor Hora Base | R$ 150 (ajustável) |
| Fator Complexidade | Baixa: 1.0, Média: 1.2, Alta: 1.4, Muito Alta: 1.6 |
| Fator Urgência | Normal: 1.0, Urgente (<30d): 1.3, Crítico (<15d): 1.5 |

**Output:**
```
💰 ESTIMATIVA DE VALOR

Horas Base: XX horas
Fator Risco: x1.X
Horas Ajustadas: XX horas

Valor Base: R$ XX.XXX
Fator Complexidade: x1.X
Fator Urgência: x1.X

━━━━━━━━━━━━━━━━━━━━━━
VALOR PROPOSTA: R$ XX.XXX
━━━━━━━━━━━━━━━━━━━━━━

Faixa do Cliente: [comparar com disponível]
```

---

### Fase 5: GERAÇÃO DA PROPOSTA NO FLYEE

**Trigger:** Após cálculo de valor

**Agente:** `orchestrator`

**MCP:** `Flyee API`

**Ações:**

1. Criar página no database "Propostas Comerciais" via `API-post-page`:
   - Preencher todas as propriedades do schema
   - Status inicial: "Rascunho"

2. Adicionar conteúdo estruturado via `API-patch-block-children`:

```markdown
## 📌 Contexto do Cliente
[Resumo do cliente e situação]

## 🎯 Problema a Ser Resolvido
[Descrição do problema/necessidade]

## 📦 Funcionalidades Solicitadas

### Must-have (MVP)
- [ ] Feature 1
- [ ] Feature 2

### Nice-to-have (Fase 2)
- [ ] Feature 3

## 📊 Análise Técnica

### Stack Identificada
[Tecnologias]

### Impactos no Sistema Existente
[Descrição de modificações necessárias]

### Riscos Identificados
[Lista de riscos e mitigações]

## 📈 Breakdown de Esforço

| Área | Features | Horas |
|------|----------|-------|
| Backend | X | Xh |
| Frontend | X | Xh |
| Infra | X | Xh |
| **Total** | **X** | **Xh** |

## 💰 Composição do Valor

| Item | Valor |
|------|-------|
| Horas Base | Xh |
| Fator Risco | xX.X |
| Horas Ajustadas | Xh |
| Valor/Hora | R$ XXX |
| Fator Complexidade | xX.X |
| Fator Urgência | xX.X |
| **TOTAL** | **R$ XX.XXX** |

## ⏰ Timeline Estimado
[Prazo de entrega estimado]

## ✅ Próximos Passos
1. Aprovação da proposta
2. Assinatura do contrato
3. Início do discovery técnico (/discovery)
```

3. Notificar usuário com link da proposta

---

### Fase 6: APROVAÇÃO E ENCAMINHAMENTO

**Trigger:** Proposta criada no Flyee

**Gate:**
```
🛑 PROPOSTA GERADA

📄 Proposta: [Link Flyee]
💰 Valor: R$ XX.XXX
⏰ Prazo: XX dias

Envie para o cliente e aguarde aprovação.

Quando APROVADO, altere o Status no Tracker para "Aprovado" e execute:

/discovery --from-demand "[Nome da Proposta]"
```

---

## 📋 SCHEMA FLYEE (Referência)

### Propriedades

| Propriedade | Tipo | Preenchido por |
|-------------|------|----------------|
| Nome | Title | Usuário |
| Status | Status | Manual |
| Cliente | Text | Usuário |
| Prazo Desejado | Date | Usuário |
| Faixa Investimento | Select | Usuário |
| Valor Proposta | Number | IA |
| Horas Estimadas | Number | IA |
| Complexidade | Select | IA |
| Qtd Features | Number | IA |
| Qtd Telas | Number | IA |
| Stack | Multi-select | IA |
| Risco | Select | IA |
| Tipo Projeto | Select | Usuário |
| Link Projeto | URL | Usuário |
| Responsável | People | Usuário |

---

## 🔗 INTEGRAÇÃO COM /discovery

Quando executado com `--from-demand`:

1. Buscar proposta aprovada no Flyee
2. Extrair informações já coletadas
3. Pré-preencher respostas do Brainstorm (Fase 1):
   - Problema → do campo "Problema a Ser Resolvido"
   - MVP → do campo "Must-have"
   - Stack → do campo "Stack"
   - Prazo → do campo "Prazo Desejado"
4. Pular perguntas já respondidas
5. Continuar fluxo normal do /discovery

---

## 🚀 USAGE

```bash
# Levantamento completo
/demand

# Com projeto existente
/demand --project ./path/to/project

# Com SDD existente
/demand --tdd docs/design/SDD-projeto.md
```

---

## 📊 EXEMPLO

```
Usuário: /demand

IA: 🧠 Iniciando Levantamento de Demanda...

───────────────────────────────────
✅ PRE-FLIGHT CHECK
───────────────────────────────────
Database "Propostas Comerciais" encontrado. ✓

───────────────────────────────────
📋 FASE 1: COLETA
───────────────────────────────────

1️⃣ Qual o nome do cliente/projeto?
> TaNaVitrine

2️⃣ Qual o tipo de projeto?
> Evolução

3️⃣ Existe código ou docs existentes?
> Sim, c:\mobile-apps\Tanavitrine-refactor

4️⃣ Qual o prazo desejado?
> 60 dias

5️⃣ Qual a faixa de investimento?
> 15k-50k

6️⃣ Descreva o que precisa ser feito:
> Implementar vitrine completa com dashboard...

───────────────────────────────────
🔍 FASE 2: ANÁLISE
───────────────────────────────────

Analisando projeto existente...
✓ Stack: Next.js, Supabase, React
✓ Telas existentes: 5
✓ API endpoints: 12
✓ SDD encontrado: SDD-tanavitrine-platform.md

───────────────────────────────────
📈 FASE 3: ESTIMATIVA
───────────────────────────────────

| Área | Tasks | Horas |
|------|-------|-------|
| Backend | 8 | 45h |
| Frontend | 12 | 68h |
| Infra | 3 | 12h |
| **Total** | 23 | 125h |

Fator Risco (Médio): x1.3
Horas Ajustadas: 162h

───────────────────────────────────
💰 FASE 4: VALOR
───────────────────────────────────

162h × R$ 150 = R$ 24.300
× Complexidade Alta (1.4) = R$ 34.020
× Urgência Normal (1.0) = R$ 34.020

━━━━━━━━━━━━━━━━━━━━━━
VALOR PROPOSTA: R$ 34.020
━━━━━━━━━━━━━━━━━━━━━━

✓ Dentro da faixa do cliente (15k-50k)

───────────────────────────────────
📄 FASE 5: FLYEE
───────────────────────────────────

✅ Proposta criada no Flyee!
🔗 Link: [Proposta TaNaVitrine]

───────────────────────────────────
🛑 AGUARDANDO APROVAÇÃO
───────────────────────────────────

Quando aprovado, execute:
/discovery --from-demand "Proposta TaNaVitrine"
```
