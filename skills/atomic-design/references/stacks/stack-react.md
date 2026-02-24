# Stack Adapter: React (TSX)

> For React projects using TypeScript, SCSS, and optionally Storybook.

---

## Folder Structure

For a component named `Button` in the **atoms** category:

```
src/components/atoms/Button/
├── index.ts              # Barrel export
├── Button.tsx            # Component implementation
├── Button.styles.scss    # BEM styles with design tokens
├── Button.types.ts       # TypeScript interfaces
├── Button.test.tsx       # Tests (Vitest + RTL)
└── Button.stories.tsx    # Storybook story (optional)
```

**Category paths:**
- `src/components/atoms/` — Buttons, Inputs, Icons
- `src/components/molecules/` — SearchBar, FormField
- `src/components/organisms/` — Header, Card, Modal

---

## Required Files (5 minimum)

### 1. Types — `Button.types.ts` (ALWAYS FIRST)

```tsx
export interface ButtonProps {
  readonly children: React.ReactNode;
  readonly variant?: 'primary' | 'secondary';
  readonly size?: 'sm' | 'md' | 'lg';
  readonly disabled?: boolean;
  readonly onClick?: () => void;
}
```

**Rules:**
- Use `Readonly` or `readonly` modifier on all props
- Export interface separately for consumers
- Define all variants as union types

### 2. Component — `Button.tsx`

```tsx
import React from 'react';
import type { ButtonProps } from './Button.types';
import './Button.styles.scss';

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
}) => {
  return (
    <button
      className={`button button--${variant} button--${size}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};

export default Button;
```

**Rules:**
- Functional components only (no class components)
- Default export for the component
- Import styles directly (NOT CSS Modules)
- All props with defaults where sensible

### 3. Styles — `Button.styles.scss`

```scss
.button {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-medium);
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background-color 0.2s ease, opacity 0.2s ease;

  &--primary {
    background-color: var(--color-primary);
    color: var(--color-background);
  }

  &--secondary {
    background-color: transparent;
    color: var(--color-primary);
    border-color: var(--color-primary);
  }

  &--sm { padding: var(--spacing-xs) var(--spacing-sm); font-size: var(--font-size-sm); }
  &--lg { padding: var(--spacing-md) var(--spacing-lg); font-size: var(--font-size-lg); }

  &:hover:not(:disabled) { opacity: 0.85; }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
```

**Rules:**
- BEM methodology strictly
- ALL values from design tokens (CSS variables)
- ZERO hardcoded hex/px values
- Import pattern: `import './Button.styles.scss';` (not modules)

### 4. Tests — `Button.test.tsx`

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import Button from './Button';

describe('Button', () => {
  it('renders children correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('applies variant class', () => {
    render(<Button variant="secondary">Test</Button>);
    expect(screen.getByText('Test')).toHaveClass('button--secondary');
  });

  it('calls onClick when clicked', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByText('Click me')).toBeDisabled();
  });

  it('does not call onClick when disabled', () => {
    const handleClick = vi.fn();
    render(<Button disabled onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).not.toHaveBeenCalled();
  });
});
```

**Rules:**
- Vitest + React Testing Library
- Test: rendering, props, interactions, disabled state
- Minimum 80% coverage

### 5. Barrel Export — `index.ts`

```ts
export { default } from './Button';
export type { ButtonProps } from './Button.types';
```

---

## Optional: Storybook Story — `Button.stories.tsx`

```tsx
import type { Meta, StoryObj } from '@storybook/react';
import Button from './Button';

const meta: Meta<typeof Button> = {
  title: 'Atoms/Button',
  component: Button,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: { children: 'Primary Button', variant: 'primary' },
};

export const Secondary: Story = {
  args: { children: 'Secondary Button', variant: 'secondary' },
};

export const Disabled: Story = {
  args: { children: 'Disabled', disabled: true },
};
```

**Title pattern:** `{Category}/{ComponentName}` (e.g., `Atoms/Button`, `Molecules/SearchBar`)

---

## Composition with shadcn/ui

When the user opts to use shadcn as a base:

1. Check `components.json` exists. If not: `npx shadcn@latest init`
2. Identify matching primitive: `npx shadcn@latest add button`
3. Import and wrap:

```tsx
import { Button as ShadcnButton } from '@/components/ui/button';
import type { ButtonProps } from './Button.types';
import './Button.styles.scss';

const Button: React.FC<ButtonProps> = ({ children, variant, ...props }) => (
  <ShadcnButton className={`button button--${variant}`} {...props}>
    {children}
  </ShadcnButton>
);
```

**Rule:** Use shadcn for behavior, BEM/tokens for custom visuals.

---

## Infrastructure Detection

| Check | File to Scan | Install Command |
|-------|-------------|----------------|
| React | `package.json` → `react` | — |
| TypeScript | `tsconfig.json` | `npm install -D typescript @types/react` |
| SCSS | `package.json` → `sass` | `npm install -D sass` |
| Vitest | `vitest.config.*` | `npm install -D vitest @testing-library/react @testing-library/jest-dom` |
| Storybook | `.storybook/` dir | `npx storybook@latest init` |
