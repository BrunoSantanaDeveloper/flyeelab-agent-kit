---
name: project-setup
description: Project initialization and infrastructure setup. Init commands by stack, test runner config, folder structure, and environment separation. Used before TDD methodology phase.
---

# Project Setup

> Prepare base infrastructure before writing tests. No tests without a working project.

---

## 🎯 When to Use

| Workflow | Phase | Trigger |
|----------|-------|---------|
| `/new-project` | Phase 3.5 | After Breakdown |
| `/legacy-project` | Verify setup | Ensure test runner exists |
| `/enhance` | If missing infra | Before adding feature |

> [!CAUTION]
> Do NOT start TDD (Phase 4) without infrastructure configured.
> Cannot write tests without an initialized project.

---

## 🆕 New Project (No Existing Code)

### 1. Initialize Project

```bash
# Web (Next.js)
npx -y create-next-app@latest ./ --typescript --tailwind --app --src-dir --import-alias "@/*"

# Mobile (React Native)
npx react-native init {ProjectName} --template react-native-template-typescript

# Package (TypeScript)
npm init -y && npm install -D typescript tsup vitest
```

### 2. Configure Test Runner

```bash
# Next.js / React
npm install -D vitest @testing-library/react @testing-library/dom jsdom @vitejs/plugin-react
```

### 3. Create Base Structure

```
src/
├── app/           # Routes (Next.js)
├── components/    # UI components
├── lib/           # Business logic
├── tests/         # Tests
└── types/         # TypeScript types
```

### 4. Configure vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
  },
});
```

### 5. Verify Setup

```bash
npm test -- --run  # Must run without errors (0 tests ok)
```

### 6. Configure Environment Separation (MANDATORY)

> Delegate to skill `deployment-procedures` section "Environment Separation".
> Follow all rules for `.env.local`, `.env.example`, and `.env.production`.

**Quick checklist:**

```markdown
⚠️ ENVIRONMENT VALIDATION GATE

[ ] `.env.example` exists with generic placeholders
[ ] `.env.local` exists with DEVELOPMENT credentials
[ ] `.env.local` does NOT point to production projects
[ ] `.gitignore` includes `.env.local` and `.env.production`
[ ] Production variables will be configured ONLY on deploy platform (Vercel)
```

**If dev projects don't exist, ask the user:**

```markdown
## 🔐 Environment Separation

For security, I need **DEVELOPMENT** credentials (not production).

| Service | Required Action |
|---------|----------------|
| **Supabase** | Create project `{name}-dev` in Supabase dashboard |
| **Stripe** | Use `test` keys (already available in dashboard) |
| **Sanity** | Create `development` dataset (Settings → Datasets) |

When you have the dev credentials, let me know to configure `.env.local`.
```

---

## 🔄 Existing Project (Has Code)

1. Verify test runner exists
2. If missing → install (step 2 above)
3. Verify folder structure
4. **Verify environment separation (step 6 above)**
5. Proceed to TDD phase

> [!TIP]
> If project already exists and has tests configured, this phase is automatic (verification only).

---

## 🔴 Exit Gate

```markdown
[ ] Project initialized (package.json exists)
[ ] Test runner configured (vitest/jest)
[ ] Folder structure created
[ ] `npm test` runs without errors
[ ] **Environments separated (dev ≠ prod)** ⭐
[ ] **`.env.local` with DEVELOPMENT credentials only** ⭐
[ ] **`.env.example` with generic placeholders** ⭐
```

> After passing this gate, sync setup tasks with tracker.
> Follow skill `project-tracking-patterns` for sync protocol.
