---
description: Extrair Design System de projeto finalizado e salvar como template reutilizável em .agent/templates/design-system/. Gera template + paleta de cores automaticamente.
skills: frontend-design, ui-ux-discovery
---

# /extract-template - Extrair Template de Projeto

---

## 🎯 PROPÓSITO

Transforma o Design System de um projeto **finalizado e aprovado** em um template reutilizável, para que futuros projetos similares não precisem recriar o Design System do zero.

**Gera:**
- Template genérico em `.agent/templates/design-system/{TEMPLATE-NAME}.md`
- Paleta de cores extraída, adicionada ao `COLOR-PALETTES.md`
- Registro no workflow `/new-project` (Phase 2.5)

---

## 📊 QUANDO USAR

| Situação | Usar? |
|----------|-------|
| Projeto finalizado com Design System aprovado | ✅ Sim |
| Design System foi refinado manualmente durante implementação | ✅ Sim (melhor resultado) |
| Projeto ainda em andamento | ❌ Não — finalizar primeiro |
| Template já existe para esse tipo | ⚠️ Perguntar se quer substituir ou criar variante |

---

## 🧩 SUBCOMMANDS

| Comando | Ação |
|---------|------|
| `/extract-template` | Extrai do projeto atual (detecta MASTER.md automaticamente) |
| `/extract-template [caminho]` | Extrai de um caminho específico |
| `/extract-template --list` | Lista templates existentes |
| `/extract-template --preview` | Mostra o que seria extraído sem salvar |

---

## 🔴 FLUXO

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  DETECTAR    │───▶│   ANALISAR   │───▶│  ABSTRAIR    │───▶│   PALETA     │───▶│  REGISTRAR   │
│  (MASTER.md) │    │  (Padrões)   │    │  (Template)  │    │  (Cores)     │    │  (Workflow)  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
      ✅                  ✅                  ✋                  ✋                  ✅
   Automático          Automático          Aprovação           Aprovação          Automático
```

---

### Step 1: DETECTAR — Localizar Design System do Projeto

**Ações:**
1. Buscar `design-system/MASTER.md` no projeto
2. Se não encontrado: buscar `design-system/*/MASTER.md`
3. Se não encontrado: perguntar caminho ao usuário
4. Ler também: `src/styles/tokens.css`, `src/app/globals.css` (para padrões reais)

```markdown
## 📂 Design System Detectado

| Arquivo | Caminho | Status |
|---------|---------|--------|
| MASTER.md | `design-system/MASTER.md` | ✅ Encontrado |
| tokens.css | `src/styles/tokens.css` | ✅ / ❌ |
| globals.css | `src/app/globals.css` | ✅ / ❌ |

Confirma que este é o Design System finalizado? (sim/não)
```

**AGUARDAR** confirmação.

---

### Step 2: ANALISAR — Extrair Padrões

**Ler e catalogar:**

| Aspecto | O que extrair | Fonte |
|---------|--------------|-------|
| **Cores** | Paleta primária completa (5 variações) | MASTER.md / tokens.css |
| **Tipografia** | Font families, escala tipográfica, weights | MASTER.md |
| **Espaçamento** | Escala de spacing | MASTER.md / tokens.css |
| **Radius** | Escala de border-radius | MASTER.md |
| **Shadows** | Todos os níveis + brand shadow | MASTER.md |
| **Efeitos** | Transições, gradients, hover patterns | MASTER.md |
| **Breakpoints** | Escala responsiva | MASTER.md |
| **Componentes** | Lista de componentes implementados | MASTER.md |
| **Anti-patterns** | O que NÃO fazer | MASTER.md |
| **Direção Visual** | Pattern, style, mood | MASTER.md |

**Apresentar análise ao usuário:**

```markdown
## 📊 Análise do Design System

### Identificação
- **Projeto:** {nome}
- **Direção Visual:** {pattern} — {style}
- **Mood:** {mood}

### Paleta Extraída
| Token | Hex | Nome sugerido |
|-------|-----|---------------|
| primary | {hex} | — |
| primary-light | {hex} | — |
| primary-dark | {hex} | — |
| primary-accent | {hex} | — |
| primary-muted | {hex} | — |

### Tipografia
- Heading: {font}
- Body: {font}

### Componentes ({N} total)
{lista}

### Tipo de Template Sugerido
**{tipo}** — Baseado na direção visual e componentes identificados.

Segmentos recomendados para reutilização: {segmentos}
```

---

### Step 3: ABSTRAIR — Gerar Template

**Perguntas ao usuário:**

```markdown
## ✏️ Configuração do Template

1. **Nome do template:**
   Sugestão: `{sugestão baseada na direção visual}`
   (ex: "Corporate Landing", "SaaS Dashboard", "Minimal Portfolio")

2. **Para quais tipos de projeto?**
   - [ ] Site Institucional / LP
   - [ ] Web App / SaaS
   - [ ] Mobile App
   - [ ] E-commerce
   - [ ] Portfólio
   - [ ] Blog
   - [ ] Outro: ___

3. **Segmentos-alvo:**
   Sugestão: {segmentos detectados}
   (ex: "Financeiro, jurídico, imobiliário, seguros")

4. **Manter tipografia atual ou torná-la configurável?**
   A) Manter (Inter + Plus Jakarta Sans) — recomendado para consistência
   B) Tornar configurável — mais flexível mas menos testado
```

**AGUARDAR** respostas.

**Gerar template:**
1. Copiar estrutura do MASTER.md
2. Substituir cores específicas por placeholders `{PALETTE.*}`
3. Substituir `--shadow-gold` (ou brand shadow) por `{PALETTE.shadow-rgba}`
4. Substituir gradient específico por `{PALETTE.primary}` + `{PALETTE.primary-accent}`
5. Manter todos os outros tokens como valores concretos
6. Adicionar header com metadados do template
7. Salvar em `.agent/templates/design-system/{TEMPLATE-NAME}.md`

**Apresentar template gerado para aprovação.**

**AGUARDAR** aprovação.

---

### Step 4: PALETA — Registrar Cores na Biblioteca

**Gerar entrada para `COLOR-PALETTES.md`:**

```markdown
## {emoji} {N+1}. {Nome da Paleta}

> **Segmentos:** {segmentos do projeto original}
> **Mood:** {mood extraído}

| Token | Hex | Preview |
|-------|-----|---------|
| `primary` | `{hex}` | {emoji} {descrição} |
| `primary-light` | `{hex}` | {descrição} |
| `primary-dark` | `{hex}` | {descrição} |
| `primary-accent` | `{hex}` | {descrição} |
| `primary-muted` | `{hex}` | {descrição} |
| `shadow-rgba` | `rgba({r}, {g}, {b}, 0.{opacidade})` | Sombra {cor} |
```

**Perguntar ao usuário:**

```markdown
## 🎨 Registrar Paleta de Cores

As cores deste projeto serão adicionadas como nova paleta em `COLOR-PALETTES.md`.

**Nome sugerido:** {nome baseado no projeto}
**Emoji sugerido:** {emoji baseado na cor}

Quer ajustar o nome, emoji ou segmentos? (ou aprovar)
```

**AGUARDAR** aprovação. Adicionar ao final de `COLOR-PALETTES.md`.

---

### Step 5: REGISTRAR — Atualizar Workflow

**Ações automáticas:**

1. Atualizar a tabela de templates na Phase 2.5 do `/new-project`:

```markdown
| {Template Name} | `{TEMPLATE-FILE}.md` | {tipos compatíveis} |
```

2. Atualizar a tabela de paletas na Phase 2.5 do `/new-project` (se a tabela de preview existir)

3. Gerar relatório final:

```markdown
## ✅ Template Extraído com Sucesso

### Arquivos Criados/Atualizados

| Arquivo | Ação |
|---------|------|
| `.agent/templates/design-system/{TEMPLATE}.md` | ✅ Criado |
| `.agent/templates/design-system/COLOR-PALETTES.md` | ✅ Paleta adicionada |
| `.agent/workflows/new-project.md` | ✅ Tabela de templates atualizada |

### Como Usar

No próximo projeto:
```bash
/new-project meu-site
```

O agente oferecerá automaticamente:
> "Encontrei o template **{nome}**. Escolha a paleta de cores..."

### Templates Disponíveis ({N} total)

| # | Template | Tipos | Paletas |
|---|----------|-------|---------|
{tabela atualizada de todos os templates}
```

---

## 📋 GATES DE SAÍDA

```
[ ] MASTER.md do projeto-fonte localizado e confirmado
[ ] Padrões analisados e apresentados ao usuário
[ ] Template gerado com placeholders de cor
[ ] Template aprovado pelo usuário
[ ] Paleta extraída e adicionada ao COLOR-PALETTES.md
[ ] Tabela de templates no /new-project atualizada
[ ] Relatório final apresentado
```

---

## ⚠️ REGRAS

1. **Nunca extrair de projeto incompleto** — o MASTER.md deve ser a versão final
2. **Preferir o que foi REALMENTE implementado** — se houve divergência entre MASTER.md e o CSS real, usar os valores do CSS (tokens.css / globals.css)
3. **Não substituir templates existentes** sem permissão — perguntar se quer criar variante
4. **Nomes descritivos** — evitar nomes genéricos como "Template 1"
5. **Testar contraste** — verificar que as cores extraídas passam WCAG AA
