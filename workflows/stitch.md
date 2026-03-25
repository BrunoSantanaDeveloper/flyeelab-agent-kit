---
description: Workflow unificado para usar as Stitch Skills (design-md, enhance-prompt, react-components, stitch-loop, remotion, shadcn-ui). Gera UI com IA.
skills: design-md, enhance-prompt, react-components, stitch-loop, remotion, shadcn-ui, design-system-enforcement
---

# /stitch - UI Generation Workflow

$ARGUMENTS

**Flags:**

| Flag | Descrição |
|------|-----------|
| `--design` | Gerar/analisar `DESIGN.md` com design system semântico |
| `--prompt` | Melhorar prompt de UI para Stitch |
| `--components` | Converter screens para componentes React |
| `--loop` | Modo autônomo: gerar website completo |
| `--video` | Gerar vídeo walkthrough com Remotion |
| `--shadcn` | Adicionar componentes shadcn/ui |

---

## 🎯 PROPÓSITO

Workflow para geração de UI usando as **Stitch Skills** do Google Labs.
Cada flag ativa uma skill específica para o tipo de trabalho desejado.

---

## 🧭 QUICK REFERENCE

| Quero... | Comando |
|----------|---------|
| Documentar design system existente | `/stitch --design` |
| Melhorar um prompt de UI | `/stitch --prompt "descrição vaga"` |
| Converter screen para React | `/stitch --components` |
| Gerar site completo | `/stitch --loop "objetivo"` |
| Criar vídeo de demo | `/stitch --video` |
| Adicionar componente shadcn | `/stitch --shadcn button` |

---

## 📋 FLUXO POR FLAG

### 🎨 `--design` → Skill: design-md

**Objetivo:** Analisar projeto Stitch e gerar `DESIGN.md` com design system semântico.

**Pré-requisitos:**
- Projeto Stitch existente OU screens para análise

**Passos:**
1. Ler skill: `.agent/skills/design-md/SKILL.md`
2. Analisar screens existentes
3. Extrair padrões visuais (cores, tipografia, espaçamento)
4. Gerar `DESIGN.md` no formato otimizado para Stitch

**Output esperado:**
```
📄 DESIGN.md criado com:
- Color palette documentada
- Typography system
- Spacing scale
- Component patterns
- Stitch generation notes
```

---

### ✨ `--prompt` → Skill: enhance-prompt

**Objetivo:** Transformar descrições vagas em prompts otimizados para Stitch.

**Pré-requisitos:**
- Descrição/ideia de UI (pode ser vaga)

**Passos:**
1. Ler skill: `.agent/skills/new-task-prompt/SKILL.md`
2. Analisar descrição fornecida
3. Aplicar enhancers:
   - Adicionar keywords de UI/UX
   - Injetar contexto de design system
   - Estruturar para melhor resultado
4. Retornar prompt otimizado

**Exemplo:**
```
IN:  "página de login simples"
OUT: "Modern login page with glassmorphic card, centered form with email/password fields, 
      social OAuth buttons (Google, GitHub), subtle gradient background, 
      responsive mobile-first design, clear error states..."
```

---

### ⚛️ `--components` → Skill: react-components

**Objetivo:** Converter screens do Stitch para componentes React modulares.

**Pré-requisitos:**
- Screen HTML do Stitch
- Design tokens definidos (ou DESIGN.md)

**Passos:**
1. Ler skill: `.agent/skills/react-components/SKILL.md`
2. Executar scripts de validação
3. Extrair componentes do HTML
4. Aplicar design tokens consistentes
5. Validar com AST

**Scripts disponíveis:**
```bash
# Validação de componentes
node .agent/skills/react-components/scripts/validate.js
```

---

### 🔄 `--loop` → Skill: stitch-loop

**Objetivo:** Gerar website multi-página de forma autônoma.

**Pré-requisitos:**
- `DESIGN.md` (ou gerar com --design primeiro)
- `SITE.md` com visão do projeto
- Acesso ao Stitch MCP Server

**Passos:**
1. Ler skill: `.agent/skills/stitch-loop/SKILL.md`
2. Verificar/criar `next-prompt.md` (baton)
3. Consultar `SITE.md` para roadmap
4. Gerar página com Stitch
5. Integrar ao site
6. Atualizar baton para próxima iteração

**Estrutura esperada:**
```
project/
├── next-prompt.md      # Baton - tarefa atual
├── stitch.json         # Stitch project ID
├── DESIGN.md           # Design system
├── SITE.md             # Visão e roadmap
├── queue/              # Staging do Stitch
└── site/public/        # Páginas prontas
```

---

### 🎬 `--video` → Skill: remotion

**Objetivo:** Gerar vídeo walkthrough profissional do projeto.

**Pré-requisitos:**
- Screenshots das páginas
- Remotion instalado

**Passos:**
1. Ler skill: `.agent/skills/remotion/SKILL.md`
2. Coletar screenshots
3. Configurar transições e zoom
4. Adicionar overlays de texto
5. Renderizar vídeo

**Scripts disponíveis:**
```bash
# Gerar vídeo
npx remotion render
```

---

### 🧩 `--shadcn` → Skill: shadcn-ui

**Objetivo:** Integrar componentes shadcn/ui ao projeto.

**Pré-requisitos:**
- Projeto React/Next.js
- shadcn/ui inicializado

**Passos:**
1. Ler skill: `.agent/skills/shadcn-ui/SKILL.md`
2. Descobrir componente desejado
3. Instalar via CLI
4. Customizar conforme design system
5. Integrar ao código

**Comandos comuns:**
```bash
# Instalar componente
npx shadcn-ui@latest add button

# Ver componentes disponíveis
npx shadcn-ui@latest add --help
```

---

## 🔗 COMBINAÇÕES RECOMENDADAS

| Cenário | Comando |
|---------|---------|
| Novo projeto do zero | `/stitch --loop "descrição do site"` |
| Melhorar UI existente | `/stitch --prompt` → `/stitch --design` |
| Extrair componentes | `/stitch --design` → `/stitch --components` |
| Criar demo | `/stitch --video` |
| Adicionar UI library | `/stitch --shadcn [componente]` |

---

## ⚠️ REGRAS IMPORTANTES

1. **Sempre ler a skill antes de usar** - Cada skill tem instruções detalhadas
2. **DESIGN.md é central** - A maioria das skills depende dele
3. **Stitch MCP** - Para --loop, precisa do Stitch MCP Server configurado
4. **Design System primeiro** - Use --design antes de --components

---

## 🆘 TROUBLESHOOTING

| Problema | Solução |
|----------|---------|
| Prompt não gera bom resultado | Use `--prompt` para melhorar |
| Estilos inconsistentes | Gere/atualize `DESIGN.md` com `--design` |
| Componentes não validam | Verifique design tokens |
| Loop não continua | Verifique se `next-prompt.md` foi atualizado |
