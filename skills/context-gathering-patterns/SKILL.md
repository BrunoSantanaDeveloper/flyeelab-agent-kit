---
name: context-gathering-patterns
description: Leitura obrigatória de documentação (Task Notion + docs/flows/ + TDD) antes de implementar código. Gate com checklist persistente para evitar inferências baseadas apenas no código.
---

# Context Gathering Patterns

> **Leia a documentação ANTES de tocar no código.**

---

## 🎯 PROPÓSITO

Garantir que antes de implementar qualquer mudança:
1. **Lemos** o corpo da task no Notion (critérios de aceite, referências)
2. **Consultamos** documentação de domínio em `docs/flows/`
3. **Sintetizamos** decisões de negócio, tipos/contratos e restrições
4. **Persistimos** a evidência no arquivo de progresso do workflow

---

## 🔍 QUANDO USAR

| Situação | Obrigatório? |
|----------|--------------|
| Implementar task de melhoria/refatoração | ✅ Sim |
| Executar task existente do Notion | ✅ Sim |
| Implementar feature nova (enhance) | ✅ Sim |
| Implementar código de TDD breakdown | ✅ Sim |
| Debug / investigação | ⚠️ Recomendado |

---

## 🚨 ANTI-PATTERNS

> [!WARNING]
> **Caso real (Task #21 — legacy-project):** Agente retomou conversa truncada e
> saltou Context Gathering. Inferiu tipos (`unavailable_products`) a partir do
> código, ignorando documentação de fluxo de checkout/pagamento. Resultado:
> decisão de tipo potencialmente incorreta que poderia causar bugs em runtime.

> [!WARNING]
> **Caso real (Lote 4 — Phase 6 Testing):** Agente criou testes para Cielo
> (gateway stub não utilizado) baseando-se no TDD Reverso (D-01, D-02, D-03),
> sem consultar `docs/flows/shop/checkout/payment-flow.md` que define
> "Pagar.me será o único gateway". Resultado: 5 test files irrelevantes criados,
> 5 com erros por falta de config, tempo desperdiçado. O erro começou na criação
> da Testing Strategy (Phase 6) e se propagou até a implementação (Lote 4).

| ❌ Anti-pattern | ✅ Correto |
|----------------|-----------|
| Ir direto ao código e inferir tipos | Ler docs primeiro, depois validar no código |
| "O código faz X então o tipo deve ser Y" | "A documentação diz Y, verificar se código está alinhado" |
| Retomar conversa truncada sem reler docs | Verificar checklist persistido, reler se ausente |
| Usar TDD debts como escopo sem filtrar por negócio | Cruzar débits do TDD com docs de negócio antes de planejar |
| Criar testes para código legacy/stub sem verificar uso | Confirmar se o componente é ativo no projeto via docs/flows/ |

---

## 📋 PROCESSO DE CONTEXT GATHERING

### Passo 1: Ler Task (Notion)

```
Use: mcp_notion-mcp-server_API-get-block-children
block_id: {page_id da task}
```

Extrair:
- **User Story** / objetivo da task
- **Critérios de Aceite** (checklist)
- **🔗 Referências** (TDD, docs)
- **Arquivos afetados** (se listados)

### Passo 2: Ler Documentação de Domínio

Buscar em `docs/flows/` usando keywords da task:

| Keyword na task | Diretório obrigatório |
|----------------|----------------------|
| pagamento, checkout, cart, pedido | `docs/flows/*/checkout/` |
| gateway, cielo, pagarme, stripe, payment | `docs/flows/*/checkout/` + `docs/flows/api/payment/` |
| auth, login, registro, sessão | `docs/flows/*/auth/` |
| produto, catálogo, busca | `docs/flows/*/catalog/` |
| perfil, conta, endereço | `docs/flows/*/profile/` |
| tipo, REST client, API | `docs/design/TDD-*` |
| TDD debt, edge case, D-XX | `docs/flows/` (filtrar débits por relevância de negócio) |
| header, footer, navbar, menu, layout | `design-system/*/layout/SHARED-LAYOUT.md` |
| LP, landing, hero, features, seção, section | `design-system/*/pages/PAGE-SPEC-Landing.md` + `SHARED-LAYOUT.md` |
| pricing, planos, plans | `design-system/*/pages/PAGE-SPEC-Pricing.md` |
| componente UI, button, input, card | `design-system/*/MASTER.md` |
| página, page, tela, screen | `design-system/*/pages/PAGE-SPEC-{página}.md` |

**Se referência TDD existir na task:** abrir seções específicas mencionadas.

**Se nenhum doc encontrado:** registrar como flag de risco (ver Passo 3).

### Passo 3: Sintetizar e Persistir

Preencher o checklist abaixo no **arquivo de progresso** do workflow ativo:

| Workflow | Arquivo de progresso |
|----------|---------------------|
| `/legacy-project` | `docs/LEGACY-PROGRESS.md` |
| `/enhance` | `docs/ENHANCE-PROGRESS.md` |
| `/execute` | (comentário na task Notion) |
| `/tdd` | `docs/design/TDD-*.md` (seção de notas) |
| `/new-project` | `docs/PROJECT-PROGRESS.md` |

---

## 📊 CHECKLIST DE EVIDÊNCIA (Template)

```markdown
📖 CONTEXT GATHERING — Task #{id}: {título}
[ ] Corpo da task lido no Notion (ID: {page_id})
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

---

## ✅ GATE DE SAÍDA

> [!CAUTION]
> **NÃO prossiga** para implementação sem completar este gate.

**Validação mínima:**
- PELO MENOS 1 item preenchido em cada seção (decisões, tipos, restrições)
- Se docs ausentes → registrar flag explícita:
  `"⚠️ Docs ausentes — decisões baseadas em análise do código (risco elevado)"`

---

## 🔄 RE-CHECK NO RESUME

Ao retomar uma conversa truncada (`--resume`):

1. Verificar se existe checklist `📖 CONTEXT GATHERING` para a task em andamento
2. **Se existe e está preenchida** → prosseguir
3. **Se NÃO existe ou está incompleta** → re-executar Context Gathering completo

> [!TIP]
> Isso garante que mesmo após truncamento de conversa, o agente releia
> a documentação antes de tomar decisões de implementação.

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Fase | Referência |
|----------|------|------------|
| `/legacy-project` | Phase 7B Passo 0 | Gate obrigatório por task |
| `/execute` | Fase 4 (EXECUTE) | Antes de implementar |
| `/enhance` | Fase 3 (EXECUTION) | Antes de implementar |
| `/tdd` | Phase 6 (IMPLEMENT) | Antes de cada task |
| `/new-project` | Phase 5 (CODE) | Antes de implementar |
