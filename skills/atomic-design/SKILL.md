---
name: atomic-design
description: Stack-agnostic Atomic Design component generation. Creates well-structured Atoms, Molecules, and Organisms with design tokens, typing, tests, and quality gates. Works with React, Vue, Blade, or any stack.
---

# Atomic Design Component Builder

> **Philosophy:** Components are the building blocks of interfaces. Structure them right once, reuse forever.
> **Core Principle:** Atomic Design is a METHODOLOGY, not a technology. Stack is an implementation detail.

---

## 🎯 Selective Reading Rule (MANDATORY)

| File | Status | When to Read |
|------|--------|--------------|
| [classification-guide.md](references/classification-guide.md) | 🔴 **REQUIRED** | Always — defines Atom/Molecule/Organism |
| [quality-checklist.md](references/quality-checklist.md) | 🔴 **REQUIRED** | Always — the quality gate |
| [stack-react.md](references/stacks/stack-react.md) | ⚪ Stack-specific | When target is React (Vite, CRA) |
| [stack-nextjs.md](references/stacks/stack-nextjs.md) | ⚪ Stack-specific | When target is Next.js (App Router) |
| [stack-vue.md](references/stacks/stack-vue.md) | ⚪ Stack-specific | When target is Vue/Nuxt |
| [stack-blade.md](references/stacks/stack-blade.md) | ⚪ Stack-specific | When target is Laravel Blade |

> 🔴 **Read Classification Guide + Quality Checklist ALWAYS. Then read the stack adapter that matches the project.**

---

## 1. Stack Detection (ALWAYS FIRST)

Before generating any component, determine the stack:

### Auto-Detection

1. Scan project root for indicators:
   - `next.config.*` → **Next.js** (use `stack-nextjs.md`)
   - `vite.config.*` + `react` in package.json → **React** (use `stack-react.md`)
   - `nuxt.config.*` or `vite.config.*` + `vue` in package.json → **Vue**
   - `artisan` + `resources/views/` → **Blade**
   - `svelte.config.*` → **Svelte** (use principles, no adapter yet)
   - `angular.json` → **Angular** (use principles, no adapter yet)

2. If auto-detection fails → **ASK** the user

### Stack Adapter Loading

Once stack is known:
1. Read the matching `references/stacks/stack-{name}.md`
2. Use its folder structure, file patterns, and templates
3. If no adapter exists → apply universal principles from this SKILL.md

---

## 2. Component Generation Workflow

### Phase 1: Discovery

Before writing ANY code:

1. **Component Name** — What is it called? (PascalCase for JS, kebab-case for Blade)
2. **Category** — Atom, Molecule, or Organism? (read classification guide if unsure)
3. **Reference** — Figma link, screenshot, or text description?
4. **Base Library** — Use a UI library base? (shadcn, Headless UI, Radix, none)
5. **Extras** — Storybook story? Tests?

> 🔴 **Ask ONE question at a time. Wait for response before next.**

### Phase 2: Infrastructure Check

**BEFORE generating any component code:**

| Check | Action if Missing |
|-------|-------------------|
| **Design Tokens file** | Create starter `variables.css` (see § Token Starter below) |
| **Test framework** | Ask user: "Install Vitest/PHPUnit/Jest?" |
| **Storybook** | Ask user: "Install Storybook?" (only if requested) |
| **UI Library** | Install via CLI if user opted in (e.g., `npx shadcn@latest init`) |

### Phase 3: Scaffold & Implement

1. Create folder structure per stack adapter
2. Generate **ALL required files** in sequence:
   - Types/Interface file (FIRST — define the contract)
   - Component implementation
   - Styles (design tokens, BEM naming)
   - Tests (minimum 80% coverage target)
   - Barrel export (index file)
   - Story file (if opted in)
3. Run quality checklist (see `references/quality-checklist.md`)

---

## 3. Universal Design Principles

### Atomic Classification (Summary)

| Level | What | Examples | Rule |
|-------|------|----------|------|
| **Atom** | Smallest indivisible UI element | Button, Input, Icon, Label, Badge | Cannot be broken down further |
| **Molecule** | Simple group of atoms working together | SearchBar (Input+Button), FormField (Label+Input+Error) | 2-3 atoms combined for one purpose |
| **Organism** | Complex section composed of molecules/atoms | Header, Card, Modal, Sidebar, DataTable | Self-contained section of interface |

> 📖 Full guide with decision tree: [classification-guide.md](references/classification-guide.md)

### Design Token Usage (MANDATORY)

**❌ NEVER hardcode style values:**
```css
/* BAD */
.button { background-color: #0070f3; padding: 16px; }
```

**✅ ALWAYS use design tokens:**
```css
/* GOOD */
.button { background-color: var(--color-primary); padding: var(--spacing-md); }
```

### Token Starter Template

If no token file exists, create `variables.css` (or equivalent):

```css
:root {
  /* Colors */
  --color-primary: #0070f3;
  --color-secondary: #7928ca;
  --color-text: #333;
  --color-text-light: #666;
  --color-background: #fff;
  --color-border: #e1e1e1;

  /* Spacing Scale */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* Typography */
  --font-size-sm: 14px;
  --font-size-md: 16px;
  --font-size-lg: 18px;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;
}
```

> **Note:** If the project already has a Design System (e.g., via `/ds-init`), use those tokens instead. Do NOT create a duplicate token file.

### BEM Naming (Default Methodology)

```
Block:    .button
Element:  .button__icon
Modifier: .button--primary

Nesting in SCSS/CSS:
.card {
  &__header { }
  &__body { }
  &--featured { }
}
```

> **Exception:** If the stack convention differs (e.g., Tailwind utility-first), follow stack adapter instructions. BEM is the fallback.

### Type Safety (MANDATORY)

Every component MUST have typed props/parameters:

| Stack | Mechanism |
|-------|-----------|
| React/Vue (TS) | TypeScript `interface` with `Readonly<T>` |
| React (JS) | PropTypes + JSDoc |
| Vue (SFC) | `defineProps<T>()` with TypeScript |
| Blade | PHPDoc on Component class + `@props` |

**❌ FORBIDDEN:** `any`, `unknown` as prop types, untyped parameters.

### Testing (MANDATORY)

| Requirement | Standard |
|-------------|----------|
| Coverage target | 80% minimum |
| Test location | Colocated with component |
| What to test | Rendering, props, interactions, disabled states, a11y basics |

### Accessibility (MANDATORY)

- Semantic HTML elements (not `div` for everything)
- ARIA attributes where needed
- Keyboard navigable
- Sufficient color contrast (WCAG 2.1 AA)
- Focus indicators visible

---

## 4. Restrictions & Prohibitions

### ❌ Absolute Prohibitions

- **NO** hardcoded style values (colors, spacing, font sizes)
- **NO** untyped props/parameters (`any`, missing types)
- **NO** monolithic files (split types, styles, tests)
- **NO** business logic inside components (extract to hooks/composables/services)
- **NO** static text hardcoded (extract to data/i18n files)
- **NO** `dangerouslySetInnerHTML` or `v-html` without sanitization

### ✅ Mandatory Requirements

- **MUST** check for design tokens before creating component
- **MUST** create ALL required files per stack adapter
- **MUST** use design tokens for ALL style values
- **MUST** type ALL props/parameters
- **MUST** colocate tests with components
- **MUST** use barrel exports (index file)

---

## 5. Composition with UI Libraries

When user opts to use a base UI library:

| Library | Check | Install Command |
|---------|-------|----------------|
| shadcn/ui | `components.json` exists? | `npx shadcn@latest init` |
| Headless UI | In package.json? | `npm install @headlessui/react` |
| Radix | In package.json? | `npm install @radix-ui/react-*` |

### Hybrid Styling Rule

When composing with a UI library:
- Use the **library's API** for behavior and base structure
- Use **BEM/token styles** for custom visual overrides
- Do NOT rebuild what the library provides

---

## 6. Decision Process Summary

```
For EVERY component:

1. DETECT STACK
   └── Auto-scan or ask user
   └── Load stack adapter

2. CLASSIFY
   └── Atom, Molecule, or Organism?
   └── Use classification guide if unsure

3. CHECK INFRASTRUCTURE
   └── Tokens exist? Tests? Storybook?
   └── Create/install as needed

4. GENERATE
   └── Types FIRST, then component, styles, tests, exports
   └── Use adapter templates

5. QUALITY GATE
   └── Run quality-checklist.md
   └── ALL items must pass before done
```

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `frontend-design` | Design principles (colors, typography, UX) — use BEFORE atomic-design |
| `clean-code` | Code quality standards — always active |
| `testing-patterns` | Testing strategies — complements test generation |
| `design-system-enforcement` | Ensures DS compliance — post-generation audit |
| `shadcn-ui` | shadcn/ui integration details — when using shadcn base |
