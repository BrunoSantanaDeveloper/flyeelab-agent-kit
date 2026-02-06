---
description: Workflow obrigatório para finalizar tasks. Garante sync com Notion, logs de execução e atualização de progresso.
---

# /task-complete

> **OBRIGATÓRIO** ao finalizar qualquer task. Garante compliance com tracking patterns.

## Uso

```bash
/task-complete <task_id> "<tempo_gasto>"
```

**Exemplo:**
```bash
/task-complete 1.1 "30min"
/task-complete 2.3 "1h15m"
```

---

## Fluxo de Execução (4 Etapas)

### Etapa 1: Exibir Log de Execução

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

**Ação Notion:**
- Status: {anterior} → Concluído
- Tempo Gasto: {tempo}

**Tempo aproximado:** {tempo}
```

### Etapa 2: Atualizar Notion

```json
// Tool: mcp_notion-mcp-server_API-patch-page
{
  "page_id": "{task_page_id}",
  "properties": {
    "Status": { "status": { "name": "Concluído" } },
    "Tempo Gasto": { "rich_text": [{ "text": { "content": "{tempo}" } }] },
    "% Progresso": { "number": 100 }
  }
}
```

### Etapa 3: Adicionar Comentário

```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{task_page_id}" },
  "rich_text": [{ "text": { "content": "✅ Concluído: {resumo do que foi feito}" } }]
}
```

### Etapa 4: Atualizar PROJECT-PROGRESS.md

Atualizar a tabela de tasks:

```markdown
| # | Task | Teste | Código | Status |
|---|------|-------|--------|--------|
| {id} | {nome} | ✅ | ✅ | ✅ Completo |  ← ATUALIZAR
```

---

## Checklist de Conclusão

Antes de prosseguir para próxima task:

- [ ] Log de Execução exibido
- [ ] Notion atualizado (Status + Tempo Gasto + %)
- [ ] Comentário adicionado no Notion
- [ ] PROJECT-PROGRESS.md atualizado
- [ ] Mensagem de confirmação exibida

---

## Mensagem Final Obrigatória

```markdown
✅ **Task {ID} Concluída**

| Campo | Valor |
|-------|-------|
| Status | Concluído |
| Tempo Gasto | {tempo} |
| Notion | ✅ Sincronizado |

Prosseguindo para próxima task...
```

---

## Gatilhos Automáticos

Este workflow DEVE ser invocado quando o agente:

- Disser "task completa" ou "task concluída"
- Marcar um item como `[x]` no task.md
- Antes de iniciar uma nova task
- Ao finalizar um épico

> 🔴 **REGRA:** O agente NÃO pode prosseguir para próxima task sem executar este workflow.
