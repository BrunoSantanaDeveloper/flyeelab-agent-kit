# Atomic Design Classification Guide

> When in doubt about how to classify a component, use this decision tree.

---

## Definitions

### Atoms ⚛️

The **smallest, indivisible** UI elements. They cannot be broken down further without losing meaning.

**Characteristics:**
- Single responsibility
- No internal composition (does not contain other components)
- Accepts props for customization
- Reusable across the entire application

**Examples:**

| Atom | Props |
|------|-------|
| Button | variant, size, disabled, onClick |
| Input | type, placeholder, value, onChange |
| Label | htmlFor, children |
| Icon | name, size, color |
| Badge | variant, children |
| Avatar | src, alt, size |
| Spinner | size |
| Divider | orientation |
| Checkbox | checked, onChange |
| Tag | color, children |

---

### Molecules 🧬

**Simple groups of 2-3 atoms** working together as a unit for a single purpose.

**Characteristics:**
- Combines atoms into a functional unit
- Has one clear purpose
- Introduces layout/arrangement logic between atoms
- Still relatively simple

**Examples:**

| Molecule | Composed Of |
|----------|-------------|
| SearchBar | Input + Button |
| FormField | Label + Input + ErrorText |
| NavItem | Icon + Label |
| ToggleGroup | Label + Toggle |
| InputWithIcon | Icon + Input |
| AvatarWithName | Avatar + Label |
| StatCard | Label + Value (number) |
| MenuItem | Icon + Label + Badge |

---

### Organisms 🦠

**Complex, self-contained sections** composed of multiple molecules and/or atoms. They form distinct regions of the interface.

**Characteristics:**
- Self-contained section of UI
- May manage internal state
- Combines multiple molecules/atoms
- Can be placed directly in a page/template

**Examples:**

| Organism | Composed Of |
|----------|-------------|
| Header | Logo + NavItems + SearchBar + Avatar |
| Card | Image + Title + Description + Button |
| Modal | Overlay + Header + Body + Footer |
| DataTable | TableHeader + TableRows + Pagination |
| Sidebar | Logo + MenuItems + Footer |
| LoginForm | FormFields + Button + Link |
| CommentSection | AvatarWithName + TextArea + Button |
| ProductCard | Image + Badge + Title + Price + Button |

---

## Decision Tree

```
Is this component composed of other components?
│
├── NO → Is it a single HTML element (or thin wrapper)?
│   ├── YES → ⚛️ ATOM
│   └── NO  → Probably still an Atom (thin abstraction)
│
└── YES → How many sub-components does it combine?
    │
    ├── 2-3 simple components, ONE purpose
    │   └── 🧬 MOLECULE
    │
    └── 4+ components, or contains molecules, forms distinct UI section
        └── 🦠 ORGANISM
```

### Edge Cases

| Scenario | Classification | Reasoning |
|----------|---------------|-----------|
| Button with icon inside | ⚛️ **Atom** | Icon is a prop/slot, not a separate composed component |
| Dropdown (trigger + menu) | 🧬 **Molecule** | Two atoms working together |
| Multi-select with search | 🦠 **Organism** | Complex: Input + Dropdown + Tags + Search logic |
| Simple Card (title + text) | 🧬 **Molecule** | Just 2-3 atoms |
| Card with image + actions + badge | 🦠 **Organism** | Complex composition with multiple concerns |
| Toast/Notification | ⚛️ **Atom** | Self-contained, no internal composition |
| Toast with action button | 🧬 **Molecule** | Toast atom + Button atom |

---

## Naming Conventions

| Stack | Atoms | Molecules | Organisms |
|-------|-------|-----------|-----------|
| **React** | `Button.tsx` | `SearchBar.tsx` | `Header.tsx` |
| **Vue** | `BaseButton.vue` | `SearchBar.vue` | `AppHeader.vue` |
| **Blade** | `button.blade.php` | `search-bar.blade.php` | `header.blade.php` |

### Folder Paths

| Stack | Pattern |
|-------|---------|
| **React** | `src/components/{atoms\|molecules\|organisms}/{Name}/` |
| **Vue** | `src/components/{atoms\|molecules\|organisms}/{Name}/` |
| **Blade** | `resources/views/components/{atoms\|molecules\|organisms}/` |
