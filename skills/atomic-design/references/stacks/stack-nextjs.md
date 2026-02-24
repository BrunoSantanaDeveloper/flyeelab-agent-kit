# Stack Adapter: Next.js (App Router + TypeScript)

> Extends the React adapter with Next.js-specific patterns: Server/Client boundary, CSS Modules, and App Router conventions.
> **Base:** Read [stack-react.md](stack-react.md) first — this adapter adds Next.js-specific rules on top.

---

## Key Difference: Server vs Client Components

Next.js App Router components are **Server Components by default**. This affects how Atomic Design components are structured.

### When to use `'use client'`

| Needs | Directive | Examples |
|-------|-----------|---------|
| onClick, onChange, onSubmit | `'use client'` | Button, Input, Toggle, SearchBar |
| useState, useEffect, useRef | `'use client'` | Modal, Accordion, Tabs |
| Browser APIs (window, localStorage) | `'use client'` | ThemeSwitcher, ScrollToTop |
| Static rendering only | **None** (Server) | Badge, Avatar, Icon, Card (display-only) |
| Data fetching (async component) | **None** (Server) | DataTable with `fetch()`, UserProfile |

### Rule of Thumb

```
Does this component handle user interaction or use React hooks?
├── YES → 'use client' (first line of the .tsx file)
└── NO  → Server Component (no directive needed)
```

> 🔴 **Push `'use client'` as far DOWN the tree as possible.**
> A Header (Organism) can be a Server Component if only its SearchBar (Molecule) needs interactivity.

---

## Folder Structure

For a component named `Button` in the **atoms** category:

```
src/components/atoms/Button/
├── index.ts                  # Barrel export
├── Button.tsx                # Component ('use client' if interactive)
├── Button.module.scss        # CSS Modules (Next.js default)
├── Button.types.ts           # TypeScript interfaces
├── Button.test.tsx           # Tests (Vitest + RTL)
└── Button.stories.tsx        # Storybook story (optional)
```

**Category paths:**
- `src/components/atoms/` — Button, Input, Icon, Badge
- `src/components/molecules/` — SearchBar, FormField, NavItem
- `src/components/organisms/` — Header, Modal, DataTable

**Path alias:** Always use `@/components/...` (configured in `tsconfig.json`).

---

## Required Files

### 1. Types — `Button.types.ts` (ALWAYS FIRST)

Same as React adapter. No Next.js-specific changes.

```tsx
export interface ButtonProps {
  readonly children: React.ReactNode;
  readonly variant?: 'primary' | 'secondary' | 'ghost';
  readonly size?: 'sm' | 'md' | 'lg';
  readonly disabled?: boolean;
  readonly onClick?: () => void;
}
```

### 2. Component — `Button.tsx` (with `'use client'`)

```tsx
'use client';

import type { ButtonProps } from './Button.types';
import styles from './Button.module.scss';
import clsx from 'clsx';

export default function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
}: ButtonProps) {
  return (
    <button
      className={clsx(
        styles.button,
        styles[`button--${variant}`],
        styles[`button--${size}`],
      )}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

**Next.js-specific rules:**
- `'use client'` as first line if component uses interactivity/hooks
- **Named function export** (preferred in Next.js over `const + React.FC`)
- Default export for the component
- CSS Modules import with `clsx` for class composition

### 3. Styles — `Button.module.scss` (CSS Modules)

```scss
.button {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-medium);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background-color 0.2s ease, opacity 0.2s ease;
}

.button--primary {
  background-color: var(--color-primary);
  color: var(--color-background);
}

.button--secondary {
  background-color: transparent;
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.button--ghost {
  background-color: transparent;
  color: var(--color-text);
}

.button--sm { padding: var(--spacing-xs) var(--spacing-sm); font-size: var(--font-size-sm); }
.button--lg { padding: var(--spacing-md) var(--spacing-lg); font-size: var(--font-size-lg); }

.button:hover:not(:disabled) { opacity: 0.85; }

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

**CSS Modules rules:**
- File extension: `.module.scss` (NOT `.styles.scss`)
- Import as: `import styles from './Button.module.scss'`
- Classes accessed via `styles.button`, `styles['button--primary']`
- BEM modifiers use bracket notation: `styles['button--variant']`
- Design tokens via CSS variables still work (they're global)

> **Note:** BEM nesting (`&--modifier`) does NOT work with CSS Modules because class names are hashed. Use flat selectors instead.

### 4. Tests — `Button.test.tsx`

Same as React adapter (Vitest + React Testing Library). No changes.

### 5. Barrel Export — `index.ts`

```ts
export { default } from './Button';
export type { ButtonProps } from './Button.types';
```

---

## Server Component Example (no `'use client'`)

For a **display-only** component like a Badge:

```tsx
// No 'use client' — this is a Server Component
import type { BadgeProps } from './Badge.types';
import styles from './Badge.module.scss';
import clsx from 'clsx';

export default function Badge({ children, variant = 'default' }: BadgeProps) {
  return (
    <span className={clsx(styles.badge, styles[`badge--${variant}`])}>
      {children}
    </span>
  );
}
```

Server Components **cannot:**
- Use `onClick`, `onChange`, or any event handlers
- Use `useState`, `useEffect`, `useRef`, or any hooks
- Use browser APIs (`window`, `document`, `localStorage`)

Server Components **can:**
- Be `async` and fetch data directly
- Import and render other Server Components
- Import and render Client Components

---

## Composition with shadcn/ui

shadcn components in Next.js already include `'use client'` where needed:

```tsx
'use client';

import { Button as ShadcnButton } from '@/components/ui/button';
import type { ButtonProps } from './Button.types';
import styles from './Button.module.scss';
import clsx from 'clsx';

export default function Button({ children, variant, ...props }: ButtonProps) {
  return (
    <ShadcnButton className={clsx(styles.button, styles[`button--${variant}`])} {...props}>
      {children}
    </ShadcnButton>
  );
}
```

---

## Storybook Caveat

> ⚠️ **Server Components do NOT render in Storybook.** Only create stories for Client Components.

For Server Components, test rendering via Vitest with RSC support or integration tests.

---

## Token File Location

In Next.js, the global CSS file is typically:

```
src/app/globals.css     (App Router)
src/styles/globals.css  (alternative)
```

Add design tokens as `:root` variables in `globals.css`. They will be available to all CSS Modules via `var(--token-name)`.

---

## Infrastructure Detection

| Check | File to Scan | Install Command |
|-------|-------------|----------------|
| Next.js | `next.config.*` | — |
| TypeScript | `tsconfig.json` | Built-in with Next.js |
| SCSS | `package.json` → `sass` | `npm install -D sass` |
| clsx | `package.json` → `clsx` | `npm install clsx` |
| Vitest | `vitest.config.*` | `npm install -D vitest @testing-library/react @testing-library/jest-dom @vitejs/plugin-react` |
| Storybook | `.storybook/` dir | `npx storybook@latest init` |
| shadcn | `components.json` | `npx shadcn@latest init` |

---

## Quick Reference: React vs Next.js Adapter

| Aspect | React (`stack-react.md`) | Next.js (this file) |
|--------|------------------------|---------------------|
| Styles | `.styles.scss` (direct import) | `.module.scss` (CSS Modules) |
| BEM nesting | `&--modifier` in SCSS | Flat selectors (no nesting) |
| Class composition | String concatenation | `clsx()` utility |
| Component style | `React.FC<Props>` | Named function export |
| Server Components | N/A | Default, push `'use client'` down |
| Path alias | Optional | `@/components/...` (standard) |
