---
description: Deployment command for production releases. Pre-flight checks and deployment execution.
---

# /deploy - Production Deployment

$ARGUMENTS

---

## Purpose

This command handles production deployment with pre-flight checks, deployment execution, and verification.

**Agentes Envolvidos:**
- `devops-engineer` - Execução do deploy e configuração de infra
- `security-auditor` - Validação de segurança pré-deploy
- `test-engineer` - Verificação de testes antes do deploy

---

## 🌍 Environment Discovery Gate (OBRIGATÓRIO)

> [!CAUTION]
> **BLOQUEADOR:** ANTES de qualquer deploy, o agente DEVE perguntar sobre ambientes.

### Perguntas Obrigatórias

**Se ambientes NÃO estão documentados no TDD ou PROJECT-PROGRESS.md:**

```markdown
## 🌍 Definição de Ambientes

Preciso entender sua estratégia de ambientes antes do deploy:

1. **Quais ambientes você precisa?**
   - [ ] Development (local)
   - [ ] Staging (testes/validação)
   - [ ] Production (usuários finais)

2. **Onde será hospedado cada ambiente?**
   - Ex: Vercel, Railway, VPS, Docker, etc.

3. **Variáveis de ambiente diferem por ambiente?**
   - Ex: API keys de teste vs produção
```

### Tabela de Ambientes Padrão

| Ambiente | URL Típica | Propósito |
|----------|------------|-----------|
| Development | `localhost:3000` | Desenvolvimento local |
| Staging | `staging.app.com` | Testes e validação |
| Production | `app.com` | Usuários finais |

### Variáveis por Ambiente (Template)

| Variável | Dev | Staging | Prod | Descrição |
|----------|-----|---------|------|-----------|
| `DATABASE_URL` | local | staging-db | prod-db | Conexão DB |
| `API_KEY` | test-key | test-key | prod-key | APIs externas |
| `DEBUG` | true | true | false | Modo debug |

### Gate de Saída

```
[ ] Ambientes definidos (dev/staging/prod ou subset)
[ ] URLs planejadas para cada ambiente
[ ] Variáveis de ambiente mapeadas por ambiente
[ ] Estratégia de deploy documentada
```

> [!TIP]
> **Projetos simples:** Se o usuário confirmar "só preciso de prod", ok. Mas a pergunta DEVE ser feita.

---

## Sub-commands

```
/deploy            - Interactive deployment wizard
/deploy check      - Run pre-deployment checks only
/deploy preview    - Deploy to preview/staging
/deploy production - Deploy to production
/deploy rollback   - Rollback to previous version
```

---

## Pre-Deployment Checklist

Before any deployment:

```markdown
## 🚀 Pre-Deploy Checklist

### Code Quality
- [ ] No TypeScript errors (`npx tsc --noEmit`)
- [ ] ESLint passing (`npx eslint .`)
- [ ] All tests passing (`npm test`)

### Security
- [ ] No hardcoded secrets
- [ ] Environment variables documented
- [ ] Dependencies audited (`npm audit`)

### Performance
- [ ] Bundle size acceptable
- [ ] No console.log statements
- [ ] Images optimized

### Documentation
- [ ] README updated
- [ ] CHANGELOG updated
- [ ] API docs current

### Ready to deploy? (y/n)
```

---

## Deployment Flow

```
┌─────────────────┐
│  /deploy        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Pre-flight     │
│  checks         │
└────────┬────────┘
         │
    Pass? ──No──► Fix issues
         │
        Yes
         │
         ▼
┌─────────────────┐
│  Build          │
│  application    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Deploy to      │
│  platform       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Health check   │
│  & verify       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ✅ Complete    │
└─────────────────┘
```

---

## Output Format

### Successful Deploy

```markdown
## 🚀 Deployment Complete

### Summary
- **Version:** v1.2.3
- **Environment:** production
- **Duration:** 47 seconds
- **Platform:** Vercel

### URLs
- 🌐 Production: https://app.example.com
- 📊 Dashboard: https://vercel.com/project

### What Changed
- Added user profile feature
- Fixed login bug
- Updated dependencies

### Health Check
✅ API responding (200 OK)
✅ Database connected
✅ All services healthy
```

### Failed Deploy

```markdown
## ❌ Deployment Failed

### Error
Build failed at step: TypeScript compilation

### Details
```
error TS2345: Argument of type 'string' is not assignable...
```

### Resolution
1. Fix TypeScript error in `src/services/user.ts:45`
2. Run `npm run build` locally to verify
3. Try `/deploy` again

### Rollback Available
Previous version (v1.2.2) is still active.
Run `/deploy rollback` if needed.
```

### 🔔 FLYEE BRIDGE EMIT (Condicional)

> Se `flyee.json` existe E `enabled: true`:

**Deploy com sucesso:**
```bash
python .agent/flyee-bridge/bridge.py emit "dev.deploy_completed" '{"environment": "{env}", "version": "{version}", "platform": "{platform}", "url": "{url}"}'

# Registrar decisão de deploy
python3 .agent/flyee-bridge/bridge.py --create-decision \
  --decision "Deploy {version} to {env} via {platform}" \
  --category deploy \
  --reason "Release {version} — {changelog summary}" \
  --impact "Environment: {env} — URL: {url}"
```

**Deploy com falha:**
```bash
python .agent/flyee-bridge/bridge.py emit "dev.deploy_failed" '{"environment": "{env}", "error": "{error_summary}", "platform": "{platform}"}'
```

> Se bridge não configurado → Pular silenciosamente.

---

## Platform Support

| Platform | Command | Notes |
|----------|---------|-------|
| Vercel | `vercel --prod` | Auto-detected for Next.js |
| Railway | `railway up` | Needs Railway CLI |
| Fly.io | `fly deploy` | Needs flyctl |
| Docker | `docker compose up -d` | For self-hosted |

---

## Examples

```
/deploy
/deploy check
/deploy preview
/deploy production --skip-tests
/deploy rollback
```
