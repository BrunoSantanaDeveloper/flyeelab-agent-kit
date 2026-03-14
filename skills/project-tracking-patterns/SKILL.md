---
name: project-tracking-patterns
description: Regras de atualização de progresso durante workflows. Atualização de PROJECT-PROGRESS.md, histórico, e Flyee sincronizado.
---

# Project Tracking Patterns

> **Single Source of Truth** para rastrear progresso durante workflows longos.

---

## 🎯 PROPÓSITO

Garantir que durante execução de workflows:
1. **Arquivo de progresso** seja atualizado a cada fase
2. **Histórico** seja registrado a cada ação
3. **Flyee** seja sincronizado após cada task
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
| 2026-02-02 12:35 | 3 | 10 tasks criadas no Flyee |
| 2026-02-02 12:40 | 3 | Breakdown concluído |
```

**Ações que DEVEM ser registradas:**
- Início de fase
- Conclusão de fase
- Criação de artefatos
- Criação de tasks no Flyee
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

### 4. Sincronização de Tarefas (OBRIGATÓRIO) 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** As tarefas (Flyee ou Local) DEVEM ser atualizadas após cada épico/fase conforme a configuração de `Tracker de Tasks`.
> NÃO prosseguir para próximo épico sem sincronizar o respectivo tracker.

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
Use: Flyee API: update_task()
page_id: {task_page_id}
properties: {
  "Status": { "status": { "name": "Concluído" } }
}
```

**Opção 3 - Comentário de conclusão:**
```
Use: Flyee API: update_task() (output)
parent: { "page_id": "{task_page_id}" }
rich_text: [{ "text": { "content": "✅ Implementado: {descrição}" } }]
```

---

### 5. Gate de Sincronização por Épico 🔴

> [!CAUTION]
> **BLOQUEADOR:** Antes de iniciar próximo épico, verificar o **Modo de Tracking** do projeto:

#### Se Tracker = Flyee:
```markdown
## Checklist de Sincronização - Épico {N}

- [ ] Todas as tasks do épico atualizadas no Flyee
- [ ] Status correto (Concluído/Em Progresso)
- [ ] % Progresso atualizado
- [ ] Comentário de conclusão adicionado

> **SE NÃO SINCRONIZADO:** PARAR e sincronizar antes de prosseguir.
```

#### Se Tracker = Local (`docs/TASKS.md`):
```markdown
## Checklist de Sincronização - Épico {N}

- [ ] Todas as tasks do épico marcadas com `[x]` no arquivo `docs/TASKS.md`

> **SE NÃO SINCRONIZADO:** PARAR e atualizar arquivo antes de prosseguir.
```

**Mensagem obrigatória ao completar épico:**
```markdown
📊 **Épico {N} Concluído - Tracker Sync**

| Task ID | Status | % |
|---------|--------|---|
| {id} | ✅ | 100% |
| {id} | ✅ | 100% |

✅ Flyee sincronizado. Prosseguindo para Épico {N+1}.
```

---

### 6. Logging de Execução por Task 🔴

> [!CAUTION]
> **REGRA BLOQUEANTE:** Ao completar verificação/execução de CADA task individual,
> você DEVE exibir o log de execução ANTES de prosseguir para a próxima task.

**Quando:** Após completar verificação ou execução de qualquer task

**Template OBRIGATÓRIO:**
```markdown
### ✅ Task {ID}: {Nome}

**Verificação:**
- ✅ {arquivo/componente verificado}
- ✅ {critério de aceitação atendido}
- ✅ {teste passando, se aplicável}

**Arquivos Relevantes:**
- `{caminho/arquivo1.ts}`
- `{caminho/arquivo2.tsx}`

**Ação Flyee:**
- Status: Não iniciado → Concluído
- Última edição: {timestamp automático}

**Tempo aproximado:** {X}min
```

**Exemplo Preenchido:**
```markdown
### ✅ Task 1.1: Setup Next.js 15 + App Router

**Verificação:**
- ✅ `package.json` contém `next@15.1.7`
- ✅ `src/app/layout.tsx` existe com App Router
- ✅ `npm run build` passa sem erros

**Arquivos Relevantes:**
- `package.json`
- `src/app/layout.tsx`
- `next.config.ts`

**Ação Flyee:**
- Status: Não iniciado → Concluído
- Última edição: 2026-02-03T14:15:00

**Tempo aproximado:** 2min
```

**Regras:**
1. **NUNCA** pular este log - mesmo para tasks simples
2. **SEMPRE** listar arquivos verificados/criados
3. **SEMPRE** incluir critérios de aceitação verificados
4. **ATUALIZAR** Flyee ANTES de prosseguir para próxima task

---

## 📋 CHECKLIST DE COMPLIANCE

Antes de prosseguir para próxima fase:

- [ ] Arquivo de progresso atualizado
- [ ] Histórico registrado
- [ ] Tasks individuais atualizadas (se aplicável)
- [ ] **🔴 Log de execução exibido para cada task**
- [ ] **🔴 Flyee sincronizado (OBRIGATÓRIO)**

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Arquivo de Progresso |
|----------|---------------------|
| `/new-project` | `docs/PROJECT-PROGRESS.md` |
| `/legacy-project` | `docs/LEGACY-PROGRESS.md` |
| `/enhance` | `docs/ENHANCE-PROGRESS.md` |
| `/discovery` | Tasks direto no Flyee |
| `/execute` | Task específica no Flyee |
