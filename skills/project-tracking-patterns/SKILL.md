---
name: project-tracking-patterns
description: Regras de atualização de progresso durante workflows. Atualização de PROJECT-PROGRESS.md, histórico, e Notion sincronizado.
---

# Project Tracking Patterns

> **Single Source of Truth** para rastrear progresso durante workflows longos.

---

## 🎯 PROPÓSITO

Garantir que durante execução de workflows:
1. **Arquivo de progresso** seja atualizado a cada fase
2. **Histórico** seja registrado a cada ação
3. **Notion** seja sincronizado após cada task
4. **Tasks individuais** sejam listadas e rastreadas

---

## 🔴 REGRAS OBRIGATÓRIAS

> [!CAUTION]
> **TODAS as regras abaixo são BLOQUEANTES.**
> O workflow NÃO pode prosseguir sem cumpri-las.

### 1. Atualização Após Cada Fase

**Quando:** Ao completar qualquer fase de um workflow

**Onde:** Arquivo de progresso (`PROJECT-PROGRESS.md`, `LEGACY-PROGRESS.md`, etc.)

**O que atualizar:**
- [ ] `Fase Atual` → Próxima fase
- [ ] Status da fase concluída → `✅ Concluído`
- [ ] Artefato gerado (se houver)
- [ ] `Última atualização` → Data/hora atual

```markdown
## Exemplo de atualização:

| Fase | Status | Artefato |
|------|--------|----------|
| 2. TDD Técnico | ✅ Aprovado | `docs/design/TDD-{nome}.md` |  ← ATUALIZADO
| 3. Breakdown | 🟡 Em Progresso | - |  ← NOVA FASE ATUAL
```

---

### 2. Registro no Histórico

**Quando:** Após QUALQUER ação significativa

**Formato:**
```markdown
| Data | Fase | Ação |
|------|------|------|
| 2026-02-02 12:30 | 3 | Breakdown iniciado |
| 2026-02-02 12:35 | 3 | 10 tasks criadas no Notion |
| 2026-02-02 12:40 | 3 | Breakdown concluído |
```

**Ações que DEVEM ser registradas:**
- Início de fase
- Conclusão de fase
- Criação de artefatos
- Criação de tasks no Notion
- Aprovações humanas
- Erros ou bloqueios

---

### 3. Atualização de Tasks Após Cada Item

**Quando:** Ao trabalhar em Phase 4 (Testes) ou Phase 5 (Implementação)

**Onde:** Seção `📝 Tasks` no arquivo de progresso

**Template:**
```markdown
## 📝 Tasks (Phase 4-5)

| # | Task | Teste | Código | Status |
|---|------|-------|--------|--------|
| 1 | Setup inicial | ✅ | ✅ | ✅ Completo |
| 2 | Auth básica | ✅ | 🟡 | 🟡 Em Progresso |  ← ATUALIZAR AQUI
| 3 | CRUD usuários | ⏳ | ⏳ | ⏳ Pendente |
```

---

### 4. Sincronização com Notion

**Quando:** Após cada task ser trabalhada

**Ação:** Chamar `/task-update` ou API do Notion

**Template de chamada:**
```
/task-update {task_id} progress "{descrição do progresso}"
```

---

## 📋 CHECKLIST DE COMPLIANCE

Antes de prosseguir para próxima fase:

- [ ] Arquivo de progresso atualizado
- [ ] Histórico registrado
- [ ] Tasks individuais atualizadas (se aplicável)
- [ ] Notion sincronizado (se aplicável)

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Arquivo de Progresso |
|----------|---------------------|
| `/new-project` | `docs/PROJECT-PROGRESS.md` |
| `/legacy-project` | `docs/LEGACY-PROGRESS.md` |
| `/enhance` | `docs/ENHANCE-PROGRESS.md` |
