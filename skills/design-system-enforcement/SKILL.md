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
[ ] Conhecimento dos anti-patterns do workflow /ui-ux-pro-max
```

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

---

## ✅ Checklist por Componente

Antes de considerar um componente "pronto":

```markdown
Para: {ComponentName}

### Variáveis CSS
[ ] Todas as cores usam var(--xxx)
[ ] Backgrounds usam var(--bg-xxx)
[ ] Border-radius usa var(--radius-xxx)

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
