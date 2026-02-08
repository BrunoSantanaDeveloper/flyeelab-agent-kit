---
description: Revisar UI/UX e conteúdo de páginas existentes
---

# Review Page Workflow

> **Objetivo:** Auditar página existente em UI/UX e Conteúdo com **validação visual real**, gerando recomendações acionáveis.

---

## Sintaxe

```bash
/review-page {caminho_da_página}
# Exemplo: /review-page src/app/page.tsx
```

**Flags Opcionais:**
- `--ui-only` - Apenas revisão de UI/UX
- `--content-only` - Apenas revisão de conteúdo
- `--quick` - Auditoria rápida sem perguntas (usa padrões)
- `--no-browser` - Pular validação visual (não recomendado)

---

## ⚠️ REGRA CRÍTICA

> [!CAUTION]
> **NUNCA** aprovar UI apenas lendo código. 
> **SEMPRE** capturar screenshots e analisar visualmente no browser.
> Confiar apenas no código leva a erros de layout, espaçamento e alinhamento.

---

## Processo (5 Fases)

### FASE 1: Análise da Página Atual

1. **Ler arquivo da página** e identificar:
   - Estrutura de componentes
   - Seções existentes (Hero, Features, etc.)
   - Imports de estilos e assets

2. **Verificar Design System:**
   - Existe `design-system/{projeto}/MASTER.md`?
   - Se sim: usar como baseline
   - Se não: extrair identidade visual do código

3. **Verificar Content Strategy:**
   - Existe `docs/content/CONTENT-STRATEGY-{Projeto}.md`?
   - Se sim: usar como baseline
   - Se não: extrair conteúdo atual

---

### FASE 2: Auditoria de UI/UX

> **SKILL:** Seguir `ui-ux-discovery` para análise visual.

**Checklist de Auditoria:**

```markdown
## 🎨 Auditoria UI/UX - {página}

### Cores
- [ ] Cores seguem Design System?
- [ ] Contraste adequado (WCAG AA)?
- [ ] Consistência entre seções?

### Tipografia
- [ ] Fontes corretas aplicadas?
- [ ] Hierarquia visual clara?
- [ ] Tamanhos responsivos?

### Layout
- [ ] Espaçamento consistente?
- [ ] Responsividade funciona?
- [ ] Seções bem delimitadas?

### Efeitos Visuais
- [ ] Animações funcionando?
- [ ] Glassmorphism/shadows aplicados?
- [ ] Dark mode funciona (se aplicável)?

### Componentes
- [ ] Usando componentes do Design System?
- [ ] Sem estilos inline desnecessários?
- [ ] Acessibilidade (aria-labels, etc.)?
```

---

### FASE 2.5: VALIDAÇÃO VISUAL NO BROWSER (OBRIGATÓRIA)

> [!CAUTION]
> **GATE BLOQUEANTE:** Não prosseguir sem executar esta fase.
> Código pode parecer correto mas renderizar errado.

**1. Abrir Página no Browser:**
```
Use: browser_subagent
Task: "Navegar para {URL} e capturar estado da página"
```

**2. Capturar Screenshots de CADA Seção:**
```
Use: browser_subagent
Task: "Scrollar página e capturar screenshots de:
- Hero section (viewport inicial)
- Features/Cards section
- Social Proof section
- Pricing section (se houver)
- FAQ section (se houver)
- Footer
Retornar paths dos screenshots capturados."
```

**3. Análise Crítica Visual (OBRIGATÓRIO):**

Para CADA screenshot, analisar:

```markdown
## 🔍 Análise Visual Crítica

### Alinhamento e Espaçamento
- [ ] Cards em mesma row têm MESMA altura?
- [ ] Elementos estão centralizados corretamente?
- [ ] Gap entre elementos é uniforme?
- [ ] Padding interno dos cards é consistente?

### Grid e Layout
- [ ] Colunas estão balanceadas?
- [ ] Não há overflow ou corte de conteúdo?
- [ ] Breakpoints mobile/tablet funcionam?

### Tipografia
- [ ] Textos não estão quebrando de forma estranha?
- [ ] Hierarquia visual está clara?
- [ ] Line-height adequado?

### Cores e Contraste
- [ ] CTAs estão visíveis e destacados?
- [ ] Texto legível sobre backgrounds?
- [ ] Cores do Design System aplicadas?

### Erros Evidentes
- [ ] Elementos sobrepostos?
- [ ] Imagens quebradas?
- [ ] Ícones faltando ou errados?
- [ ] Bordas/sombras renderizando corretamente?
```

**4. Se Encontrar Problemas:**
```
⚠️ PARE e documente:
- Screenshot do problema
- Descrição exata
- Localização (seção, linha aproximada)
- Sugestão de fix

NÃO aprove a página visualmente até corrigir.
```

**Gate de Saída:**
```
[ ] Página aberta no browser
[ ] Screenshots de TODAS as seções capturados
[ ] Análise crítica de alinhamento feita
[ ] Análise de espaçamento feita
[ ] Problemas visuais documentados (se houver)
[ ] TODOS os problemas evidentes corrigidos
```

---

### FASE 3: Auditoria de Conteúdo

> **SKILL:** Seguir `content-strategy` para análise de copy.

**Checklist de Auditoria:**

```markdown
## 📝 Auditoria Conteúdo - {página}

### Hero Section
- [ ] Headline clara e impactante?
- [ ] Subheadline complementa sem repetir?
- [ ] CTAs têm verbos de ação?

### Features/Benefícios
- [ ] Títulos focam no BENEFÍCIO (não no recurso)?
- [ ] Descrições são concisas (max 15 palavras)?
- [ ] Ícones são relevantes?

### Social Proof
- [ ] Tem testimonials/logos/métricas?
- [ ] Dados são verificáveis?

### SEO
- [ ] Title tag presente e otimizado?
- [ ] Meta description presente?
- [ ] Heading hierarchy correta (H1 > H2 > H3)?
- [ ] Alt text em imagens?

### Tom de Voz
- [ ] Consistente com CONTENT-STRATEGY?
- [ ] Adequado ao público-alvo?
```

---

### FASE 4: Relatório e Recomendações

**Gerar relatório em:**
`docs/reviews/REVIEW-{página}-{data}.md`

**Estrutura do Relatório:**

```markdown
# Page Review: {página}
> **Data:** {YYYY-MM-DD}
> **Revisor:** Claude Agent

---

## 📊 Resumo Executivo

| Aspecto | Score | Status |
|---------|-------|--------|
| UI/UX | X/10 | 🟢/🟡/🔴 |
| Conteúdo | X/10 | 🟢/🟡/🔴 |
| SEO | X/10 | 🟢/🟡/🔴 |
| Acessibilidade | X/10 | 🟢/🟡/🔴 |

**Score Geral:** X/10

---

## 🔴 Issues Críticas (Fix Imediato)

| # | Issue | Local | Recomendação |
|---|-------|-------|--------------|
| 1 | | | |

---

## 🟡 Melhorias Sugeridas

| # | Melhoria | Impacto | Esforço |
|---|----------|---------|---------|
| 1 | | Alto/Médio/Baixo | Alto/Médio/Baixo |

---

## 🟢 Pontos Positivos

- {o que está bom}

---

## 📋 Próximos Passos

1. [ ] {ação 1}
2. [ ] {ação 2}
```

---

## Gate de Saída

```
[ ] Página analisada
[ ] Auditoria UI/UX completa
[ ] Auditoria de Conteúdo completa
[ ] Relatório gerado em docs/reviews/
[ ] Issues priorizadas
[ ] Recomendações acionáveis documentadas
```

---

## Integração com Outros Workflows

| Após Review | Workflow Sugerido |
|-------------|-------------------|
| Muitos issues de UI | `/enhance --visual` |
| Muitos issues de copy | `/enhance --content` |
| Redesign completo | `/legacy-project` |
| Pequenos ajustes | Editar diretamente |

---

## Exemplos de Uso

```bash
# Review completo da landing page
/review-page src/app/page.tsx

# Apenas UI/UX do dashboard
/review-page src/app/dashboard/page.tsx --ui-only

# Review rápido sem perguntas
/review-page src/app/pricing/page.tsx --quick
```
