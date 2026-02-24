---
description: Create Atomic Design components (Atoms, Molecules, Organisms) with design tokens, typing, tests, and quality gates. Stack-agnostic.
---

# /atomic — Atomic Design Component Builder

> Cria componentes seguindo Atomic Design, independente de stack.
> Skill: `@[skills/atomic-design]`

---

## Phase 1: Intake Sequencial

> 🔴 **UMA pergunta por vez. Esperar resposta antes de prosseguir.**

### Step 1: Component Name
```
Qual o nome do componente?
(Ex: Button, SearchBar, Header)
```

### Step 2: Category
```
Qual a categoria?
1. ⚛️ Atom (elemento indivisível: Button, Input, Icon)
2. 🧬 Molecule (grupo simples: SearchBar, FormField)
3. 🦠 Organism (seção complexa: Header, Modal, DataTable)

Se tiver dúvida, consulte: @[skills/atomic-design] → classification-guide.md
```

### Step 3: Stack Detection
```
Auto-detectar stack do projeto:
- next.config.* / vite.config.* + react → React
- nuxt.config.* / vite.config.* + vue → Vue
- artisan + resources/views/ → Blade

Se não detectar → Perguntar ao usuário:
"Qual stack do projeto? (React / Vue / Blade / outro)"
```

### Step 4: Referência Visual
```
Tem referência visual?
1. 🔗 Link do Figma
2. 📸 Screenshot/imagem
3. 📝 Descrição textual
4. 🚫 Sem referência (criar do zero)
```

### Step 5: Base Library
```
Usar biblioteca UI como base?
1. shadcn/ui (instalo se necessário)
2. Headless UI
3. Radix UI
4. Nenhuma (construir do zero)
```

### Step 6: Extras
```
Deseja gerar extras?
- [ ] Storybook story
- [ ] Testes unitários (recomendado)
```

---

## Phase 2: Infrastructure Check

> Executar silenciosamente. Só perguntar ao usuário se precisar instalar algo.

### 2.1 Design Tokens
```
Verificar se existe arquivo de tokens:
- variables.css / variables.scss
- tailwind.config.* com tokens customizados
- design-system/tokens.*

Se NÃO existir → Criar starter template (ver SKILL.md § Token Starter)
```

### 2.2 Test Framework
```
Se usuário pediu testes:
- React: vitest.config.* existe?
- Vue: vitest.config.* existe?
- Blade: phpunit.xml existe?

Se NÃO → Perguntar: "Framework de testes não encontrado. Instalar [Vitest/PHPUnit]?"
```

### 2.3 Storybook
```
Se usuário pediu Storybook:
- .storybook/ existe?

Se NÃO → Perguntar: "Storybook não encontrado. Instalar agora?"
```

### 2.4 UI Library
```
Se usuário escolheu shadcn:
- components.json existe?
  - SIM → Identificar primitive e instalar: npx shadcn@latest add [primitive]
  - NÃO → Inicializar: npx shadcn@latest init
```

---

## Phase 3: Generation

### 3.1 Carregar Stack Adapter
```
Ler: @[skills/atomic-design] → references/stacks/stack-{stack}.md
```

### 3.2 Gerar Arquivos
```
Seguir a ordem obrigatória do adapter:
1. Types/Interface (PRIMEIRO — contrato)
2. Component implementation
3. Styles (design tokens + BEM)
4. Tests (se solicitado)
5. Barrel export (index)
6. Story (se solicitado)
```

### 3.3 Composição com UI Library
```
Se shadcn/Headless UI foi escolhido:
- Importar primitive como base
- Envolver (wrap) com estilos customizados
- NÃO reconstruir o que a library já faz
```

---

## Phase 4: Quality Gate

> 🔴 **OBRIGATÓRIO antes de considerar o componente pronto.**

```
Executar checklist: @[skills/atomic-design] → references/quality-checklist.md

Verificar:
[ ] Classificação correta (Atom/Molecule/Organism)
[ ] Todos os arquivos obrigatórios criados
[ ] Design tokens usados (zero hardcoded values)
[ ] Tipagem completa (zero `any`)
[ ] Testes passando (se gerados)
[ ] Acessibilidade básica
[ ] Componente renderiza sem erros
```

---

## Exemplos de Uso

```bash
# Criar um Button atom
/atomic

# O workflow vai perguntar:
# 1. Nome? → Button
# 2. Categoria? → Atom
# 3. Stack detectado: React ✓
# 4. Referência? → Descrição: "botão com variantes primary/secondary/ghost"
# 5. Base? → shadcn
# 6. Extras? → Storybook + Testes
```

---

## Regras

1. **UMA pergunta por vez** — nunca fazer múltiplas perguntas
2. **Stack adapter obrigatório** — sempre carregar o adapter correto
3. **Types PRIMEIRO** — sempre gerar o contrato antes da implementação
4. **Quality Gate FINAL** — nunca pular o checklist
5. **Respeitar Design System** — se o projeto já tem tokens via `/ds-init`, usar esses tokens
