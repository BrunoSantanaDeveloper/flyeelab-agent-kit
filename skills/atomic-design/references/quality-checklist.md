# Component Quality Gate

> **MANDATORY:** Every component MUST pass ALL checks before being considered complete.

---

## Structural Integrity

- [ ] Component classified correctly (Atom/Molecule/Organism)
- [ ] ALL required files created per stack adapter
- [ ] Barrel export (`index.*`) exposes component and types
- [ ] No monolithic files (types, styles, tests are separate)
- [ ] Business logic extracted (hooks/composables/services)
- [ ] Static text/URLs extracted to data/i18n files

## Design Tokens & Styling

- [ ] Design token file (`variables.css` or equivalent) exists
- [ ] **Zero** hardcoded style values (colors, spacing, font sizes, radii)
- [ ] BEM naming used (or stack-specific convention documented)
- [ ] Dark mode support applied (if project uses dark mode)
- [ ] Responsive styles where appropriate

## Type Safety

- [ ] All props/parameters have explicit types
- [ ] **Zero** usage of `any` or untyped parameters
- [ ] Readonly/immutable prop interfaces (where applicable)
- [ ] Default values defined for optional props

## Testing

- [ ] Test file colocated with component
- [ ] Rendering test: component mounts correctly
- [ ] Props test: all prop combinations work
- [ ] Interaction test: click/input handlers fire correctly
- [ ] Edge case: disabled/loading/error states covered
- [ ] Coverage target: 80% minimum

## Accessibility

- [ ] Semantic HTML elements used (not `<div>` soup)
- [ ] Interactive elements are keyboard accessible
- [ ] ARIA attributes where native semantics insufficient
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 text, 3:1 large)
- [ ] Focus indicators visible

## Storybook (if opted in)

- [ ] Story file created with `autodocs` tag
- [ ] Default story renders correctly
- [ ] All variants have stories (primary, secondary, disabled, etc.)
- [ ] `title` follows `{Category}/{Name}` pattern (e.g., `Atoms/Button`)

## Final Verification

- [ ] Component renders in dev server without errors
- [ ] All tests pass
- [ ] Lint passes (no warnings or errors)
- [ ] No console errors/warnings in browser
