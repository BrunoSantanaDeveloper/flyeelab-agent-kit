---
name: local-verification
description: Gate obrigatório de verificação local antes de commits. Dev server, testes, build. Previne push de código quebrado.
---

# Local Verification Gate

> **Single Source of Truth** para verificação local antes de commits.

---

## 🎯 PROPÓSITO

Garantir que **NENHUM código quebrado** seja commitado, através de verificação local obrigatória.

---

## 🔗 QUANDO USAR?

| Workflow | Fase | Trigger |
|----------|------|---------|
| `/legacy-project` | Phase 7 | Antes de cada commit |
| `/new-project` | Phase 5-6 | Antes de cada commit |
| `/enhance` | Phase 3 | Antes de cada commit |
| `/execute` | Durante implementação | Antes de cada commit |

---

## 🧪 GATE DE VERIFICAÇÃO LOCAL (OBRIGATÓRIO)

> [!CAUTION]
> **BLOQUEADOR:** ANTES de commitar qualquer mudança, TODOS os itens devem passar.

### Checklist Obrigatório

```markdown
## ✅ Verificação Local - Antes do Commit

### 1. 🖥️ Dev Server
- [ ] `npm run dev` (ou equivalente) rodando sem erros
- [ ] Console do browser sem erros críticos
- [ ] Mudanças visíveis no localhost

### 2. 🧪 Testes
- [ ] `npm test` passando (se projeto tem testes)
- [ ] Nenhum teste quebrado pela mudança

### 3. 🏗️ Build
- [ ] `npm run build` completa sem erros
- [ ] Nenhum warning crítico

### 4. 👁️ Revisão Visual
- [ ] Comportamento esperado no browser
- [ ] Responsividade testada (se UI)
- [ ] Dark/Light mode testados (se aplicável)
```

---

## 📋 COMANDOS POR STACK

### Next.js / React

```bash
# Dev server
npm run dev

# Testes
npm test
npm run test:coverage  # Se disponível

# Build
npm run build

# Lint (opcional mas recomendado)
npm run lint
```

### HTML/CSS/JS Vanilla

```bash
# Dev server (usar live-server ou similar)
npx live-server ./public

# Sem testes automáticos típicos
# Verificar manualmente no browser
```

### Python

```bash
# Dev server
python -m http.server 8000  # Para sites estáticos
uvicorn app:main --reload   # Para APIs

# Testes
pytest
pytest --cov                # Com cobertura
```

---

## 🔄 FLUXO DE IMPLEMENTAÇÃO

```
Para CADA mudança/feature:

1. ✏️ Modificar código
         ↓
2. 🖥️ npm run dev → Verificar no browser
         ↓
3. 🧪 npm test → Garantir que testes passam
         ↓
4. 🏗️ npm run build → Garantir que compila
         ↓
5. ✅ GATE PASSOU? → Commit
         ↓
6. ❌ GATE FALHOU? → Corrigir antes de commit
```

---

## ⚠️ SE GATE FALHAR

### Dev Server com Erro

```markdown
❌ **Dev Server Falhou**

**Erro:** {descrição do erro}

**Ações:**
1. Verificar console para stack trace
2. Corrigir erro de sintaxe/import
3. Reiniciar dev server
4. Tentar novamente
```

### Testes Falhando

```markdown
❌ **Testes Falharam**

**Testes quebrados:**
- {nome do teste 1}
- {nome do teste 2}

**Ações:**
1. Verificar se a mudança impactou lógica existente
2. Atualizar testes se comportamento mudou intencionalmente
3. Corrigir código se for regressão
```

### Build Falhou

```markdown
❌ **Build Falhou**

**Erro:** {descrição}

**Ações:**
1. Verificar TypeScript errors
2. Verificar imports ausentes
3. Verificar variáveis de ambiente
4. Corrigir e tentar novamente
```

---

## 🔴 REGRAS CRÍTICAS

1. **NUNCA** commitar sem rodar verificação local
2. **NUNCA** ignorar testes falhando
3. **SEMPRE** verificar visualmente no browser antes de commit
4. **SEMPRE** rodar build antes de push

---

## 📊 TEMPLATE DE REGISTRO

Ao completar verificação, registrar:

```markdown
### ✅ Verificação Local Completa

| Check | Status | Comando |
|-------|--------|---------|
| Dev Server | ✅ | `npm run dev` |
| Testes | ✅ | `npm test` (15 passed) |
| Build | ✅ | `npm run build` |
| Visual | ✅ | localhost:3000 |

**Pronto para commit.**
```

