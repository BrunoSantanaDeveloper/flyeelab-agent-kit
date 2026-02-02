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

### 4. Sincronização com Notion (OBRIGATÓRIO) 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** O Notion DEVE ser atualizado após cada épico/fase.
> NÃO prosseguir para próximo épico sem sincronizar.

**Quando sincronizar:**
| Momento | Ação |
|---------|------|
| Após completar um épico | Atualizar todas as tasks do épico |
| Após completar uma fase | Adicionar comentário de conclusão |
| Ao iniciar implementação de task | Status → "Em Progresso" |
| Ao finalizar implementação de task | Status → "Concluído", % → 100% |

**Como sincronizar (escolha uma):**

**Opção 1 - Via Workflow:**
```bash
/task-update {task_id} done "{descrição do que foi feito}"
```

**Opção 2 - Via API direta:**
```
Use: mcp_notion-mcp-server_API-patch-page
page_id: {task_page_id}
properties: {
  "Status": { "status": { "name": "Concluído" } },
  "% Progresso": { "number": 100 }
}
```

**Opção 3 - Comentário de conclusão:**
```
Use: mcp_notion-mcp-server_API-create-a-comment
parent: { "page_id": "{task_page_id}" }
rich_text: [{ "text": { "content": "✅ Implementado: {descrição}" } }]
```

---

### 5. Gate de Sincronização por Épico 🔴

> [!CAUTION]
> **BLOQUEADOR:** Antes de iniciar próximo épico, verificar:

```markdown
## Checklist de Sincronização - Épico {N}

- [ ] Todas as tasks do épico atualizadas no Notion
- [ ] Status correto (Concluído/Em Progresso)
- [ ] % Progresso atualizado
- [ ] Comentário de conclusão adicionado

> **SE NÃO SINCRONIZADO:** PARAR e sincronizar antes de prosseguir.
```

**Mensagem obrigatória ao completar épico:**
```markdown
📊 **Épico {N} Concluído - Notion Sync**

| Task ID | Status | % |
|---------|--------|---|
| {id} | ✅ | 100% |
| {id} | ✅ | 100% |

✅ Notion sincronizado. Prosseguindo para Épico {N+1}.
```

---

## 📋 CHECKLIST DE COMPLIANCE

Antes de prosseguir para próxima fase:

- [ ] Arquivo de progresso atualizado
- [ ] Histórico registrado
- [ ] Tasks individuais atualizadas (se aplicável)
- [ ] **🔴 Notion sincronizado (OBRIGATÓRIO)**

> [!CAUTION]
> **Falha em sincronizar Notion = Workflow incompleto**

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Arquivo de Progresso |
|----------|---------------------|
| `/new-project` | `docs/PROJECT-PROGRESS.md` |
| `/legacy-project` | `docs/LEGACY-PROGRESS.md` |
| `/enhance` | `docs/ENHANCE-PROGRESS.md` |
| `/discovery` | Tasks direto no Notion |
| `/execute` | Task específica no Notion |
