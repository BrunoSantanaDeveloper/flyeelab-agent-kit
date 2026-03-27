---
type: DESIGN_SYSTEM
doc_id: DS-{slug}
status: draft        # draft | review | approved | superseded
version: "1.0"
created_at: YYYY-MM-DD
approved_by: null
depends_on:
  - PRD-{slug}
related_docs:
  - docs/design/SDD-{slug}.md
  - docs/INDEX.md
---

# Design System — {slug}

---

## 0. Agent Context (Machine-Readable Summary)

> ⚡ Leitura rápida para agentes. Use esta seção para consultar tokens sem ler o doc inteiro.

| Token | Valor |
|-------|-------|
| **Primary** | {primary-color} |
| **Secondary** | {secondary-color} |
| **Background** | {bg-color} |
| **Text** | {text-color} |
| **Font family** | {font-family} |
| **Border radius** | {radius} |
| **Shadow** | {shadow} |

---

## 1. Color Palette

### 1.1 Brand Colors

| Name | Token | Value | Usage |
|------|-------|-------|-------|
| Primary | `--color-primary` | `{value}` | CTAs, links, accents |
| Primary Dark | `--color-primary-dark` | `{value}` | Hover states |
| Secondary | `--color-secondary` | `{value}` | Supporting elements |
| Accent | `--color-accent` | `{value}` | Highlights |

### 1.2 Neutrals

| Name | Token | Value |
|------|-------|-------|
| White | `--color-white` | `#ffffff` |
| Gray 100 | `--color-gray-100` | `{value}` |
| Gray 500 | `--color-gray-500` | `{value}` |
| Gray 900 | `--color-gray-900` | `{value}` |
| Black | `--color-black` | `#000000` |

### 1.3 Semantic Colors

| Name | Token | Value | Usage |
|------|-------|-------|-------|
| Success | `--color-success` | `{value}` | Confirmations |
| Warning | `--color-warning` | `{value}` | Alerts |
| Error | `--color-error` | `{value}` | Errors |
| Info | `--color-info` | `{value}` | Informational |

---

## 2. Typography

| Element | Font Family | Size | Weight | Line Height |
|---------|-------------|------|--------|-------------|
| H1 | {font} | {size} | {weight} | {lh} |
| H2 | {font} | {size} | {weight} | {lh} |
| H3 | {font} | {size} | {weight} | {lh} |
| Body | {font} | {size} | {weight} | {lh} |
| Small | {font} | {size} | {weight} | {lh} |
| Label | {font} | {size} | {weight} | {lh} |

```css
:root {
  --font-primary: '{font-name}', sans-serif;
  --font-mono: '{mono-font}', monospace;

  --text-xs: {size};
  --text-sm: {size};
  --text-base: {size};
  --text-lg: {size};
  --text-xl: {size};
  --text-2xl: {size};
  --text-4xl: {size};
}
```

---

## 3. Spacing

```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;
}
```

---

## 4. Border Radius

```css
:root {
  --radius-sm: {value};
  --radius-md: {value};
  --radius-lg: {value};
  --radius-xl: {value};
  --radius-full: 9999px;
}
```

---

## 5. Shadows & Effects

```css
:root {
  --shadow-sm: {value};
  --shadow-md: {value};
  --shadow-lg: {value};
  --shadow-glass: {value};   /* glassmorphism */
  --blur-glass: {value};
}
```

---

## 6. Animations & Transitions

```css
:root {
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
  --transition-slow: 400ms ease;
}
```

| Animation | Usage | Duration |
|-----------|-------|----------|
| Fade in | Page transitions | {duration} |
| Slide up | Modal, drawer | {duration} |
| Scale | Button press | {duration} |

---

## 7. Component Tokens

### Buttons
```css
:root {
  --btn-primary-bg: var(--color-primary);
  --btn-primary-text: var(--color-white);
  --btn-primary-hover: var(--color-primary-dark);
  --btn-radius: var(--radius-md);
  --btn-font-weight: 600;
}
```

### Cards
```css
:root {
  --card-bg: {value};
  --card-border: {value};
  --card-radius: var(--radius-lg);
  --card-shadow: var(--shadow-md);
  --card-padding: var(--space-6);
}
```

---

## 8. Breakpoints

| Name | Min Width | Usage |
|------|-----------|-------|
| sm | 640px | Mobile landscape |
| md | 768px | Tablet |
| lg | 1024px | Desktop |
| xl | 1280px | Wide desktop |
| 2xl | 1536px | Ultra-wide |

---

## 9. Approval Checklist

- [ ] Color palette aprovada (modo claro + escuro se aplicável)
- [ ] Tipografia aprovada (fontes carregadas, fallbacks definidos)
- [ ] Spacing e radius aprovados
- [ ] Sombras e efeitos aprovados
- [ ] Seção 0 Agent Context preenchida com valores finais
- [ ] **Aprovado pelo responsável de design**

---

## Histórico

| Data | Autor | Alteração |
|------|-------|-----------|
| YYYY-MM-DD | [Nome] | Criação inicial |
