# Stack Adapter: Vue 3 (SFC + TypeScript)

> For Vue 3 projects using Composition API, TypeScript, and SCSS.

---

## Folder Structure

For a component named `BaseButton` in the **atoms** category:

```
src/components/atoms/BaseButton/
├── index.ts                  # Barrel export
├── BaseButton.vue            # SFC (template + script + style)
├── BaseButton.types.ts       # TypeScript interfaces
├── BaseButton.test.ts        # Tests (Vitest + Vue Test Utils)
└── BaseButton.stories.ts     # Storybook story (optional)
```

**Naming convention:** Vue components use `Base` prefix for atoms to avoid conflicts with HTML elements.

**Category paths:**
- `src/components/atoms/` — BaseButton, BaseInput, BaseIcon
- `src/components/molecules/` — SearchBar, FormField
- `src/components/organisms/` — AppHeader, DataTable, SideBar

---

## Required Files (4 minimum)

### 1. Types — `BaseButton.types.ts` (ALWAYS FIRST)

```ts
export interface BaseButtonProps {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

export interface BaseButtonEmits {
  (e: 'click'): void;
}
```

### 2. Component — `BaseButton.vue`

```vue
<script setup lang="ts">
import type { BaseButtonProps, BaseButtonEmits } from './BaseButton.types';

withDefaults(defineProps<BaseButtonProps>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
});

defineEmits<BaseButtonEmits>();
</script>

<template>
  <button
    :class="['button', `button--${variant}`, `button--${size}`]"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<style lang="scss" scoped>
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
</style>
```

**Rules:**
- `<script setup>` with `lang="ts"` (Composition API)
- `defineProps<T>()` with `withDefaults()` for typed props
- `defineEmits<T>()` for typed events
- `<style lang="scss" scoped>` for scoped BEM styles
- Slots instead of `children` prop

### 3. Tests — `BaseButton.test.ts`

```ts
import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import BaseButton from './BaseButton.vue';

describe('BaseButton', () => {
  it('renders slot content', () => {
    const wrapper = mount(BaseButton, {
      slots: { default: 'Click me' },
    });
    expect(wrapper.text()).toContain('Click me');
  });

  it('applies variant class', () => {
    const wrapper = mount(BaseButton, {
      props: { variant: 'secondary' },
      slots: { default: 'Test' },
    });
    expect(wrapper.classes()).toContain('button--secondary');
  });

  it('emits click event', async () => {
    const wrapper = mount(BaseButton, {
      slots: { default: 'Click me' },
    });
    await wrapper.trigger('click');
    expect(wrapper.emitted('click')).toHaveLength(1);
  });

  it('is disabled when prop is set', () => {
    const wrapper = mount(BaseButton, {
      props: { disabled: true },
      slots: { default: 'Disabled' },
    });
    expect(wrapper.attributes('disabled')).toBeDefined();
  });
});
```

### 4. Barrel Export — `index.ts`

```ts
export { default as BaseButton } from './BaseButton.vue';
export type { BaseButtonProps, BaseButtonEmits } from './BaseButton.types';
```

---

## Optional: Storybook Story — `BaseButton.stories.ts`

```ts
import type { Meta, StoryObj } from '@storybook/vue3';
import BaseButton from './BaseButton.vue';

const meta: Meta<typeof BaseButton> = {
  title: 'Atoms/BaseButton',
  component: BaseButton,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof BaseButton>;

export const Primary: Story = {
  args: { variant: 'primary' },
  render: (args) => ({
    components: { BaseButton },
    setup: () => ({ args }),
    template: '<BaseButton v-bind="args">Primary</BaseButton>',
  }),
};

export const Secondary: Story = {
  args: { variant: 'secondary' },
  render: (args) => ({
    components: { BaseButton },
    setup: () => ({ args }),
    template: '<BaseButton v-bind="args">Secondary</BaseButton>',
  }),
};
```

---

## Composables Pattern

For components with complex logic, extract to composables:

```
src/composables/useButton.ts
```

```ts
import { computed } from 'vue';

export function useButton(variant: string) {
  const classes = computed(() => ['button', `button--${variant}`]);
  return { classes };
}
```

---

## Infrastructure Detection

| Check | File to Scan | Install Command |
|-------|-------------|----------------|
| Vue 3 | `package.json` → `vue` | — |
| TypeScript | `tsconfig.json` | `npm install -D typescript vue-tsc` |
| SCSS | `package.json` → `sass` | `npm install -D sass` |
| Vitest | `vitest.config.*` | `npm install -D vitest @vue/test-utils` |
| Storybook | `.storybook/` dir | `npx storybook@latest init --type vue3` |
