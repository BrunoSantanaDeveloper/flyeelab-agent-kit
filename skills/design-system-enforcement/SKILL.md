---
name: design-system-enforcement
description: Garante que código UI usa Design System desde a criação. Aplica-se durante TDD GREEN phase e qualquer criação de componente UI.
---

# Design System Enforcement

> **Regra:** Todo código UI DEVE usar o Design System desde a criação, não apenas na fase de "styling".

---

## 🚨 Quando Esta Skill se Aplica

| Situação | Aplica? |
|----------|---------|
| TDD GREEN phase com componente UI | ✅ SIM |
| Criação de nova página | ✅ SIM |
| Criação de novo componente | ✅ SIM |
| Código backend/API | ❌ NÃO |
| Testes unitários | ❌ NÃO |

---

## 📋 Pré-requisitos (OBRIGATÓRIO)

ANTES de escrever qualquer código UI:

```markdown
[ ] CSS Variables instaladas em src/app/globals.css (ou equivalente)
[ ] design-system/{projeto}/MASTER.md lido e carregado
[ ] design-system/{projeto}/layout/SHARED-LAYOUT.md lido (se Header, Footer, Menu, ou layout global)
[ ] design-system/{projeto}/pages/PAGE-SPEC-{página}.md lido (se implementando seção de página)
[ ] Conhecimento dos anti-patterns do workflow /ui-ux-pro-max
```

> [!CAUTION]
> **FALHA QUE GEROU ESTA EXPANSÃO:** MASTER.md sozinho cobre tokens CSS (cores, tipografia,
> spacing). Mas elementos estruturais (quais ícones no header, quantas colunas no footer,
> tipo de mobile menu) estão nos specs de layout/página. Sem lê-los, o agente implementa
> com base em padrões genéricos em vez do design aprovado.

**Se CSS Variables NÃO existem:**
1. Abrir `design-system/{projeto}/MASTER.md`
2. Copiar seção de tokens/variáveis CSS
3. Colar em `globals.css`
4. Definir body styling base

---

## 🎨 Durante Criação de Componente

Para CADA elemento visual criado:

| Aspecto | ✅ Correto | ❌ Errado |
|---------|-----------|----------|
| **Cores** | `style={{ color: 'var(--lime)' }}` | `style={{ color: '#CFFF00' }}` |
| **Background** | `var(--bg-card)` | `#111111` ou `bg-gray-900` |
| **Bordas** | `var(--radius-md)` | `12px` hardcoded |
| **Fontes** | Font do MASTER.md | Arial, sans-serif |
| **Ícones** | `<Home size={20} />` (Lucide) | `🏠` emoji |
| **Interação** | `className="cursor-pointer"` | Sem cursor |
| **Glass** | `backdrop-filter: blur(16px)` + overlay | `background-color: var(--bg-card)` solid ⭐ |
| **Shadows** | `var(--shadow-md)` | `box-shadow: 0 4px 12px...` hardcoded |

---

## 💠 Efeitos Visuais (MASTER.md § Efeitos Visuais)

> [!CAUTION]
> **FALHA QUE GEROU ESTA SEÇÃO:** Dashboard UI foi criado com cores sólidas
> (`background-color: var(--color-bg-secondary)`) sem aplicar glassmorphism
> (`backdrop-filter: blur(16px)`, `var(--color-overlay-*)`) definido no MASTER.md.
> O agente tecnicamente "usou CSS variables" (satisfazendo as regras anteriores),
> mas ignorou completamente a seção de Efeitos Visuais.
> Resultado: dashboard visualmente plano, sem a estética premium das referências.

**Se MASTER.md define Efeitos Visuais (glassmorphism, gradientes, glows, etc.), então:**

| Componente | Efeito Obrigatório | Implementação |
|------------|-------------------|---------------|
| **Cards** (KPI, Project, etc.) | Glassmorphism | `backdrop-filter: blur()` + `var(--color-overlay-05)` + border translúcida |
| **Sidebar** | Glass ou surface | `backdrop-filter: blur()` ou `var(--color-bg-secondary)` se spec permitir opaco |
| **TopBar / Header** | Glass com blur | `backdrop-filter: blur()` para visual premium |
| **Modals / Dropdowns** | Elevated glass | `var(--shadow-lg)` + `backdrop-filter` |
| **Hover states** | Micro-animation | `transform`, `box-shadow`, `border-color` com transition |

**Anti-patterns de Efeitos:**

| ❌ Errado | ✅ Correto |
|----------|----------|
| `background-color: var(--bg-card)` sem blur | `background: var(--color-overlay-05); backdrop-filter: blur(16px)` |
| Card sem shadow alguma | `box-shadow: var(--shadow-md)` |
| Hover sem feedback visual | `transition: all 200ms; transform: translateY(-2px)` |
| Border opaca | `border: 1px solid var(--color-overlay-08)` |

---

## 🏗️ Anatomia de Layout (Reference Matching)

> [!IMPORTANT]
> **REFERENCE MODE:** Quando `frontend-specialist.md` ativa o Reference Mode,
> esta seção é a mais crítica. A análise de anatomia abaixo é **OBRIGATÓRIA**
> e deve ser feita ANTES de escrever qualquer CSS. Regras anti-template e
> anti-safe-harbor do frontend-specialist são SUSPENSAS em Reference Mode.

> [!CAUTION]
> **FALHA QUE GEROU ESTA SEÇÃO:** Dashboard Sidebar e TopBar foram implementados
> como "floating pills" com `border-radius: 32px` e `gap: 1.5rem` descolados das bordas,
> quando a referência SphereUI mostrava claramente componentes **edge-to-edge**
> (sidebar colada à borda esquerda, topbar como faixa horizontal contínua).
> O agente "olhou" a referência mas não analisou a anatomia espacial — pulou direto
> para escrever CSS baseado em suposições genéricas.

**ANTES de implementar qualquer layout, o agente DEVE:**

1. **Descrever textualmente** o que vê na referência visual (se disponível):
   ```markdown
   ## Análise da Referência — {componente}
   - Sidebar: [edge-to-edge | floating | pill]
   - Sidebar border-radius: [nenhum nas bordas da viewport | apenas interno | todos os lados]
   - TopBar: [faixa contínua acima do conteúdo | se estende sobre sidebar | pill flutuante]
   - Toggle collapse: [header da sidebar | topbar | inline no conteúdo]
   - Elementos colam na viewport? [sim — top/left/bottom | não — margin ao redor]
   ```
2. **Comparar** com o que está implementando
3. **Se não houver referência visual:** Perguntar ao usuário ou seguir o PAGE-SPEC

**Checklist de Anatomia Espacial:**

| Aspecto | Pergunta | Impacto se errado |
|---------|----------|-------------------|
| **Ancoragem** | O componente encosta na borda da viewport? | Edge-to-edge vs floating pill |
| **Border-radius** | Quais cantos são arredondados? | Todos = floating. Apenas internos = encostado na borda |
| **Span** | TopBar cobre toda a largura ou só o conteúdo? | Layout em colunas (sidebar + main) vs layout unificado |
| **Toggle position** | O collapse está no header da sidebar ou no topbar? | Afeta onde o botão é renderizado |
| **Height** | Sidebar tem height: 100vh ou height: auto? | Scroll behavior e ancoragem |

---

## ✅ Checklist por Componente

Antes de considerar um componente "pronto":

```markdown
Para: {ComponentName}

### Variáveis CSS
[ ] Todas as cores usam var(--xxx)
[ ] Backgrounds usam var(--bg-xxx)
[ ] Border-radius usa var(--radius-xxx)

### Efeitos Visuais (se MASTER.md define) ⭐
[ ] Cards/surfaces usam glassmorphism (backdrop-filter + overlay) conforme MASTER.md
[ ] Shadows aplicadas conforme nível de elevação (sm/md/lg)
[ ] Hover states têm micro-animações (transition, transform)
[ ] Borders usam overlay variables (var(--color-overlay-08))

### Tipografia
[ ] Font-family definida no MASTER.md ou herdada do body
[ ] Font-sizes seguem escala do Design System

### Ícones
[ ] Nenhum emoji usado como ícone
[ ] Ícones de Lucide React ou Heroicons

### Interação
[ ] cursor-pointer em elementos clicáveis
[ ] Hover states com feedback visual
[ ] Transitions suaves (150-300ms)

### Acessibilidade
[ ] role="xxx" onde apropriado
[ ] aria-label em ícones/botões sem texto
```

---

## 🔴 Gate de Saída

Componente só está "pronto para commit" quando:

```markdown
[ ] Usa APENAS variáveis do Design System
[ ] Sem cores/valores hardcoded
[ ] Sem emojis como ícones
[ ] cursor-pointer em clicáveis
[ ] Efeitos visuais aplicados conforme MASTER.md (glassmorphism, shadows, animations) ⭐
[ ] Passou no ui_antipattern_check.py (se disponível)
```

---

## 🔗 Workflows que Referenciam Esta Skill

| Workflow | Fase |
|----------|------|
| `/new-project` | Phase 4 (TDD GREEN) |
| `/enhance` | Fase 3.5 (TDD) |
| `/legacy-project` | Phase 6 (Testes) |

---

## 📝 Exemplo Prático

### ❌ Errado (hardcoded)

```tsx
export default function Card() {
  return (
    <div style={{ 
      backgroundColor: '#111111',  // ❌ hardcoded
      color: 'white',              // ❌ hardcoded
      borderRadius: '12px'         // ❌ hardcoded
    }}>
      <span>🚀</span>  {/* ❌ emoji como ícone */}
      <button>Click</button>  {/* ❌ sem cursor-pointer */}
    </div>
  )
}
```

### ✅ Correto (Design System)

```tsx
import { Rocket } from 'lucide-react'

export default function Card() {
  return (
    <div style={{ 
      backgroundColor: 'var(--bg-card)',
      color: 'var(--text-primary)',
      borderRadius: 'var(--radius-md)'
    }}>
      <Rocket size={20} style={{ color: 'var(--lime)' }} />
      <button className="cursor-pointer hover:opacity-80 transition-opacity">
        Click
      </button>
    </div>
  )
}
```

---

> **Lembre-se:** O Design System é lei. Não há exceções para "fazer rápido" ou "ajustar depois".
