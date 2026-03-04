# MASTER.md — Template: Corporate Landing

> **Template baseado em:** Perspec (2026-03)
> **Uso:** Sites institucionais, corporativos, financeiros, jurídicos, imobiliários
> **Instruções:** Substituir `{PALETTE}` pela paleta escolhida. Ajustar conteúdo por projeto.

---

## Direção Visual

- **Pattern:** Corporate Landing — Profissional, confiável, premium
- **Style:** Modern Corporate com acentos de cor primária
- **Mood:** Profissional, confiável, acessível e humano

---

## 🎨 Cores — ESCOLHER PALETA

> ⚠️ **Escolher uma paleta da biblioteca `COLOR-PALETTES.md` antes de prosseguir.**
> A paleta define: Primary, Primary Light, Primary Dark, Primary Accent, Primary Muted.
> Os neutros e cores de suporte abaixo são universais.

### Paleta Primária (Da paleta escolhida)

| Token | Valor | Uso |
|-------|-------|-----|
| `--color-primary` | `{PALETTE.primary}` | Cor principal (brand identity) |
| `--color-primary-light` | `{PALETTE.primary-light}` | Variante clara (hovers, destaques) |
| `--color-primary-dark` | `{PALETTE.primary-dark}` | Variante escura (textos sobre fundo claro) |
| `--color-primary-accent` | `{PALETTE.primary-accent}` | Accent (CTAs, botões) |
| `--color-primary-muted` | `{PALETTE.primary-muted}` | Suave (bordas, dividers) |

### Paleta de Suporte (Universal)

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-success` | `#14704b` | Aprovado, positivo |
| `--color-success-light` | `#357b49` | Variante light |
| `--color-error` | `#BC0C06` | Erro, alerta crítico |
| `--color-error-light` | `#dd3333` | Variante light |

### Neutros (Universal)

| Token | Hex | Uso |
|-------|-----|-----|
| `--color-bg-primary` | `#ffffff` | Fundo principal |
| `--color-bg-secondary` | `#f9f9f9` | Fundo alternado (seções) |
| `--color-bg-tertiary` | `#f5f5f5` | Fundo de cards |
| `--color-bg-dark` | `#1a1a1a` | Fundo escuro (footer, hero) |
| `--color-bg-dark-alt` | `#222222` | Fundo escuro alternativo |
| `--color-text-primary` | `#1a1a1a` | Texto principal |
| `--color-text-secondary` | `#666666` | Texto secundário |
| `--color-text-muted` | `#999999` | Texto desabilitado/muted |
| `--color-text-inverse` | `#ffffff` | Texto sobre fundo escuro |
| `--color-border` | `#e2e3e3` | Bordas padrão |
| `--color-border-light` | `#efefef` | Bordas sutis |

---

## 🔤 Tipografia

| Token | Valor | Uso |
|-------|-------|-----|
| `--font-primary` | `'Inter', sans-serif` | Corpo de texto, UI |
| `--font-heading` | `'Plus Jakarta Sans', sans-serif` | Títulos e headings |

> **Google Fonts:** `Inter:400,500,600,700` + `Plus+Jakarta+Sans:600,700,800`

### Escala Tipográfica

| Token | Size | Weight | Uso |
|-------|------|--------|-----|
| `--text-xs` | 0.75rem (12px) | 400 | Captions, labels |
| `--text-sm` | 0.875rem (14px) | 400 | Secundário, meta |
| `--text-base` | 1rem (16px) | 400 | Corpo padrão |
| `--text-lg` | 1.125rem (18px) | 500 | Corpo destaque |
| `--text-xl` | 1.25rem (20px) | 600 | Sub-títulos |
| `--text-2xl` | 1.5rem (24px) | 600 | Títulos de seção |
| `--text-3xl` | 2rem (32px) | 700 | Títulos de página |
| `--text-4xl` | 2.5rem (40px) | 800 | Hero titles |
| `--text-5xl` | 3.5rem (56px) | 800 | Hero display (desktop) |

---

## 📐 Espaçamento

| Token | Valor | Uso |
|-------|-------|-----|
| `--space-1` | 0.25rem (4px) | Micro gaps |
| `--space-2` | 0.5rem (8px) | Inline spacing |
| `--space-3` | 0.75rem (12px) | Compact |
| `--space-4` | 1rem (16px) | Default |
| `--space-5` | 1.5rem (24px) | Between elements |
| `--space-6` | 2rem (32px) | Section padding |
| `--space-8` | 3rem (48px) | Section gap |
| `--space-10` | 4rem (64px) | Large section gap |
| `--space-12` | 5rem (80px) | Hero/section padding |
| `--space-16` | 8rem (128px) | Page-level spacing |

### Container

| Token | Valor |
|-------|-------|
| `--container-sm` | 640px |
| `--container-md` | 768px |
| `--container-lg` | 1024px |
| `--container-xl` | 1200px |
| `--container-padding` | 1.5rem (mobile) / 2rem (desktop) |

---

## 🔲 Border Radius

| Token | Valor | Uso |
|-------|-------|-----|
| `--radius-sm` | 4px | Inputs, small elements |
| `--radius-md` | 8px | Cards, containers |
| `--radius-lg` | 12px | Modals, featured cards |
| `--radius-xl` | 16px | Hero elements |
| `--radius-full` | 9999px | Badges, pills, avatars |

---

## 🌑 Shadows

| Token | Valor | Uso |
|-------|-------|-----|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle elevation |
| `--shadow-md` | `0 4px 12px rgba(0,0,0,0.08)` | Cards |
| `--shadow-lg` | `0 8px 24px rgba(0,0,0,0.12)` | Elevated cards, dropdowns |
| `--shadow-xl` | `0 16px 48px rgba(0,0,0,0.15)` | Modals, hero elements |
| `--shadow-brand` | `0 4px 16px {PALETTE.shadow-rgba}` | CTA buttons (brand shadow) |

---

## ✨ Efeitos Visuais

### Transições
| Token | Valor |
|-------|-------|
| `--transition-fast` | `150ms ease` |
| `--transition-base` | `250ms ease` |
| `--transition-slow` | `400ms ease` |
| `--transition-spring` | `500ms cubic-bezier(0.34, 1.56, 0.64, 1)` |

### Hover Effects
- **Cards:** `translateY(-4px)` + `shadow-lg` on hover
- **Buttons:** brightness + scale(1.02) + shadow-brand
- **Links:** underline-offset animation + color transition
- **Images:** subtle zoom (scale 1.03) dentro de overflow hidden

### Gradients (Gerados a partir da paleta)
| Token | Valor | Uso |
|-------|-------|-----|
| `--gradient-brand` | `linear-gradient(135deg, {PALETTE.primary}, {PALETTE.primary-accent})` | CTAs, hero overlay |
| `--gradient-dark` | `linear-gradient(180deg, #1a1a1a, #222222)` | Footer, seções escuras |
| `--gradient-hero` | `linear-gradient(135deg, rgba(26,26,26,0.85), rgba(34,34,34,0.7))` | Overlay do hero |

---

## 📱 Breakpoints

| Token | Valor | Dispositivo |
|-------|-------|-------------|
| `--bp-sm` | 640px | Mobile landscape |
| `--bp-md` | 768px | Tablet |
| `--bp-lg` | 1024px | Desktop pequeno |
| `--bp-xl` | 1280px | Desktop |

---

## 🎯 Componentes Recomendados

| Componente | Descrição |
|-----------|-----------|
| **Header** | Scroll-aware: transparente → sólido. Logo + nav + contact. Fixed. |
| **Footer** | bg-dark, grid 3 colunas. Logo + links + endereço. |
| **HeroSlider** | Slides com autoplay + crossfade. Overlay gradient + CTA. |
| **ServicesGrid** | Cards com ícone Lucide + hover lift. |
| **PageHero** | Hero de páginas internas com background image + breadcrumb. |
| **CTABanner** | Faixa com gradient-brand. |
| **CookieConsent** | Banner LGPD. |

---

## ❌ Anti-Patterns (EVITAR)

| Evitar | Usar |
|--------|------|
| Gradients arco-íris | Gradients sutis (2 cores da paleta) |
| Neon / glow effects | Shadows e elevação elegante |
| Fontes decorativas em body | Inter para corpo, Jakarta para títulos |
| Cards sem sombra/borda | Sempre shadow-md ou border |
| Cores saturadas demais | Palette harmoniosa |
| Animações que distraem | Micro-animações sutis (hover, entrada) |
| Tailwind classes | CSS Modules com custom properties |
| Valores hardcoded no CSS | Tokens do design system |
| Emojis como ícones | SVG via Lucide React |
