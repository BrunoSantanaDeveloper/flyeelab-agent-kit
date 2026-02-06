---
name: content-strategy
description: Define conteúdo textual (copy) para LPs, páginas internas e metadados SEO antes da implementação
---

# Content Strategy Skill

> **Objetivo:** Definir TODO o conteúdo textual ANTES de implementar UI.
> Evita retrabalho e garante consistência de mensagem.

---

## Quando Usar

| Cenário | Usar? |
|---------|-------|
| SaaS com Landing Page | ✅ Obrigatório |
| Site institucional | ✅ Obrigatório |
| E-commerce | ✅ Obrigatório |
| Dashboard interno | ⚠️ Opcional (empty states, labels) |
| API/Backend puro | ❌ Pular |

---

## Processo (4 Passos)

### PASSO 1: Identificar Páginas

Listar todas as páginas que precisam de conteúdo:

```markdown
## Páginas Identificadas

### Públicas (Marketing) - OBRIGATÓRIAS para SaaS/Produto
- [ ] Landing Page `/` (Hero, Features, Pricing Preview, FAQ Preview)
- [ ] Iniciar Projeto `/start` (Wizard Entry - Link padrão YouTube)
- [ ] Pricing `/pricing` (Detalhado, com FAQs próprias)
- [ ] Como Funciona `/how-it-works` (Educação rápida, não curso)
- [ ] Biblioteca/Catálogo `/workflows` ou `/features` (Semi-aberto: público + premium)

### Públicas (Opcional)
- [ ] Blog `/blog` (se estratégia de conteúdo)
- [ ] Comunidade `/community` (delimitadora, filtra público errado)
- [ ] Páginas por Vídeo `/videos/{slug}` (CMS, SEO, ponte YouTube→Produto)

### Privadas (App)
- [ ] Dashboard
- [ ] Onboarding/Wizard
- [ ] Settings
- [ ] Profile
```

> [!IMPORTANT]
> **Para SaaS/Produtos com YouTube:** A página `/start` deve ser o link padrão dos vídeos.
> As páginas de vídeo (`/videos/{slug}`) devem ser CMS, não hardcoded.

---

### PASSO 2: Perguntas ao Usuário ⭐

> [!CAUTION]
> **BLOQUEADOR:** Fazer estas perguntas ANTES de definir o copy.

#### Perguntas Obrigatórias

1. **Tom de Voz:**
   - A) Formal/Corporativo
   - B) Profissional mas acessível
   - C) Casual/Amigável
   - D) Técnico/Developer-focused

2. **Público Principal:**
   - Quem é o usuário ideal? (persona)
   - Qual o nível técnico?

3. **Proposta de Valor:**
   - Qual o principal benefício em UMA frase?
   - O que diferencia dos concorrentes?

4. **Urgência/CTA:**
   - Qual ação principal queremos que o usuário tome?
   - Há senso de urgência? (Early access, Limited spots, etc.)

5. **Pricing (se aplicável):**
   - Quantos planos?
   - Qual a estrutura de preços?
   - Há trial/free tier?

---

### PASSO 3: Gerar Documento

Criar `docs/content/CONTENT-STRATEGY-{Projeto}.md` com:

```markdown
# Content Strategy - {Projeto}

> **Tom de Voz:** {resposta}
> **Público:** {resposta}
> **USP:** {resposta em 1 linha}

---

## 1. Landing Page

### Hero Section
| Elemento | Conteúdo |
|----------|----------|
| **Headline** | {título principal - max 10 palavras} |
| **Subheadline** | {descrição - max 25 palavras} |
| **CTA Primário** | {ex: "Começar Grátis"} |
| **CTA Secundário** | {ex: "Ver Demo"} |

### Features (3-6 cards)
| # | Título | Descrição (max 15 palavras) | Ícone |
|---|--------|------------------------------|-------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### How it Works (3-5 steps)
| Step | Título | Descrição |
|------|--------|-----------|
| 1 | | |
| 2 | | |
| 3 | | |

### Social Proof
- [ ] Testimonials (quantos?)
- [ ] Logos de clientes
- [ ] Métricas (ex: "10k+ usuários")

### Pricing (se aplicável)
| Plano | Preço | Features |
|-------|-------|----------|
| Free | $0 | |
| Pro | $ | |
| Enterprise | $ | |

### FAQ (5-10 perguntas)
| # | Pergunta | Resposta |
|---|----------|----------|
| 1 | | |
| 2 | | |

### Footer
- **Links:** Home, Features, Pricing, FAQ, Contact, Terms, Privacy
- **Social:** Twitter, LinkedIn, GitHub (quais?)

---

## 2. Páginas Internas

### Empty States
| Página | Mensagem quando vazio | CTA |
|--------|----------------------|-----|
| Dashboard | | |
| Projects | | |

### Labels de Navegação
| Seção | Label |
|-------|-------|
| Home | Dashboard |
| | |

### Onboarding Steps (se aplicável)
| Step | Título | Instrução | Placeholder |
|------|--------|-----------|-------------|
| 1 | | | |

---

## 3. SEO Metadata

| Página | Title (max 60 chars) | Meta Description (max 155 chars) |
|--------|---------------------|----------------------------------|
| Home | | |
| Pricing | | |
| Dashboard | | |
```

---

### PASSO 4: Validar e Aprovar

**Gate de Saída:**
```
[ ] Documento CONTENT-STRATEGY gerado
[ ] Hero copy definido (headline, subheadline, CTAs)
[ ] Features descritas
[ ] Pricing documentado (se aplicável)
[ ] FAQ com pelo menos 5 perguntas
[ ] SEO metadata para páginas principais
[ ] Conteúdo APROVADO pelo humano
```

> [!CAUTION]
> **BLOQUEADOR:** Não prosseguir para implementação sem aprovação do Content Strategy.

---

## Integração com Workflows

Esta skill é chamada por:
- `/new-project` → Phase 2.75
- `/discovery` → Fase 4.5
- `/legacy-project` → Phase 5.75

**Referência nos workflows:**
```markdown
> [!IMPORTANT]
> **SKILL:** Seguir `content-strategy` para definição de copy e conteúdo.
```

---

## Flags Relacionadas

| Flag | Efeito |
|------|--------|
| `--no-content` | Pula esta fase (para APIs/backends) |
| `--minimal-content` | Apenas Hero + Features (sem FAQ/Pricing detalhado) |
