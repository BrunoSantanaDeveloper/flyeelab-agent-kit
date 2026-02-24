# Stack Adapter: Laravel Blade + Alpine.js

> For Laravel projects using Blade components, Tailwind CSS, and Alpine.js for interactivity.

---

## Folder Structure

For a component named `button` in the **atoms** category:

```
resources/views/components/atoms/
└── button.blade.php

app/View/Components/Atoms/
└── Button.php

tests/Unit/Components/Atoms/
└── ButtonTest.php
```

**Category paths (Blade views):**
- `resources/views/components/atoms/` — button, input, icon, badge
- `resources/views/components/molecules/` — search-bar, form-field
- `resources/views/components/organisms/` — header, card, modal

**Category paths (Component classes):**
- `app/View/Components/Atoms/`
- `app/View/Components/Molecules/`
- `app/View/Components/Organisms/`

---

## Required Files (3 minimum)

### 1. Component Class — `app/View/Components/Atoms/Button.php`

```php
<?php

namespace App\View\Components\Atoms;

use Illuminate\View\Component;

class Button extends Component
{
    /**
     * @param 'primary'|'secondary' $variant
     * @param 'sm'|'md'|'lg' $size
     * @param bool $disabled
     */
    public function __construct(
        public string $variant = 'primary',
        public string $size = 'md',
        public bool $disabled = false,
    ) {}

    public function render()
    {
        return view('components.atoms.button');
    }

    public function classes(): string
    {
        return implode(' ', array_filter([
            'button',
            "button--{$this->variant}",
            "button--{$this->size}",
        ]));
    }
}
```

**Rules:**
- PHPDoc for all constructor parameters with union types
- Promoted constructor properties
- Helper methods for computed values (like CSS classes)
- Namespace follows folder structure

### 2. Blade Template — `resources/views/components/atoms/button.blade.php`

```blade
<button
    {{ $attributes->merge(['class' => $classes()]) }}
    @if($disabled) disabled @endif
    {{ $attributes->except(['class']) }}
>
    {{ $slot }}
</button>
```

**Rules:**
- Use `$attributes->merge()` for class merging
- Use `$slot` (not `$children`)
- Keep templates minimal — logic in Component class
- Design tokens via Tailwind/CSS classes mapped to variables

#### With Alpine.js interactivity:

```blade
<button
    {{ $attributes->merge(['class' => $classes()]) }}
    @if($disabled) disabled @endif
    x-data="{ loading: false }"
    x-on:click="loading = true; $dispatch('button-click')"
    x-bind:class="{ 'button--loading': loading }"
>
    <span x-show="!loading">{{ $slot }}</span>
    <span x-show="loading" x-cloak>Loading...</span>
</button>
```

### 3. Test — `tests/Unit/Components/Atoms/ButtonTest.php`

```php
<?php

namespace Tests\Unit\Components\Atoms;

use App\View\Components\Atoms\Button;
use Tests\TestCase;

class ButtonTest extends TestCase
{
    public function test_renders_with_default_props(): void
    {
        $component = new Button();

        $this->assertEquals('primary', $component->variant);
        $this->assertEquals('md', $component->size);
        $this->assertFalse($component->disabled);
    }

    public function test_generates_correct_classes(): void
    {
        $component = new Button(variant: 'secondary', size: 'lg');

        $this->assertStringContainsString('button--secondary', $component->classes());
        $this->assertStringContainsString('button--lg', $component->classes());
    }

    public function test_renders_in_view(): void
    {
        $view = $this->component(Button::class, [
            'variant' => 'primary',
        ]);

        $view->assertSee('button--primary');
    }

    public function test_disabled_state(): void
    {
        $view = $this->component(Button::class, [
            'disabled' => true,
        ]);

        $view->assertSee('disabled');
    }
}
```

**Rules:**
- PHPUnit (Laravel default)
- Test: construction, class generation, rendering, states
- Location: `tests/Unit/Components/{Category}/`

---

## Usage in Blade Views

```blade
{{-- Basic usage --}}
<x-atoms.button variant="primary">
    Save
</x-atoms.button>

{{-- With attributes --}}
<x-atoms.button
    variant="secondary"
    size="lg"
    wire:click="submit"
    class="mt-4"
>
    Submit Form
</x-atoms.button>

{{-- Molecule using atoms --}}
<x-molecules.search-bar
    placeholder="Search..."
    action="/search"
/>
```

---

## Styling Approach

Blade projects typically use **Tailwind CSS** for styling. Map design tokens via `tailwind.config.js`:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'var(--color-primary)',
        secondary: 'var(--color-secondary)',
      },
      spacing: {
        xs: 'var(--spacing-xs)',
        sm: 'var(--spacing-sm)',
        md: 'var(--spacing-md)',
        lg: 'var(--spacing-lg)',
        xl: 'var(--spacing-xl)',
      },
    },
  },
};
```

Or use BEM with a separate SCSS file:

```
resources/css/components/atoms/_button.scss
```

Import in `app.css`:
```css
@import 'components/atoms/button';
```

---

## Artisan Helper

Create components quickly via artisan:

```bash
php artisan make:component Atoms/Button
```

This generates both the class and view. Adjust namespace and paths as needed.

---

## Infrastructure Detection

| Check | File to Scan | When Present |
|-------|-------------|-------------|
| Laravel | `artisan` file in root | ✅ Blade adapter |
| Blade views | `resources/views/` | ✅ Standard location |
| Alpine.js | `package.json` → `alpinejs` | Interactive components |
| Tailwind | `tailwind.config.*` | Utility-first styling |
| PHPUnit | `phpunit.xml` | Test framework |
