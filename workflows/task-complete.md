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

## Fluxo de Execução (5 Etapas)

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

### Etapa 1.5: Resumo de Execução (OBRIGATÓRIO — NÃO PULAR)

> [!CAUTION]
> **REGRA BLOQUEANTE:** O agente DEVE produzir o Resumo de Execução ANTES de atualizar
> o Notion. Este resumo é o que garante ao usuário **visibilidade total** sobre o que
> foi feito para resolver a task. Sem ele, a task fica marcada como concluída mas
> ninguém sabe o que mudou.

**Template OBRIGATÓRIO (todos os campos são required):**

```markdown
## Resumo de Execução — Task #{ID}

### O que foi feito
{Descrição técnica detalhada das mudanças. NÃO usar frases genéricas como
"implementado conforme solicitado". Descrever CADA mudança com contexto técnico.}

### Arquivos modificados
| Arquivo | Tipo de Mudança | Detalhe |
|---------|----------------|---------|
| `{path/file1.ts}` | {Criado/Modificado/Deletado} | {O que mudou neste arquivo} |
| `{path/file2.tsx}` | {Criado/Modificado/Deletado} | {O que mudou neste arquivo} |

### Verificação
- TypeScript: {✅ 0 erros / ❌ N erros}
- Testes: {✅ X/Y passando / ⚠️ sem testes / ❌ N falhando}
- Build: {✅ OK / ⚠️ não verificado}

### Decisões técnicas (se aplicável)
- {Decisão 1: por que escolheu abordagem X em vez de Y}
- {Decisão 2: trade-off feito}
```

> [!IMPORTANT]
> Este resumo será usado como fonte para:
> - **Etapa 2.5** (nota inline no corpo da task)
> - **Etapa 3** (comentário rico)
> - **Etapa 4** (LEGACY-PROGRESS.md)
>
> O agente DEVE copiar as informações deste resumo para os templates das etapas seguintes.
> NÃO inventar informações diferentes em cada etapa.

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

### Etapa 2.5: Adicionar Nota de Conclusão no Corpo (INLINE — NÃO PULAR)

> [!CAUTION]
> Os campos abaixo DEVEM ser preenchidos com os dados do **Resumo de Execução** (Etapa 1.5).
> NÃO usar placeholders genéricos. Se o Resumo de Execução não foi produzido, PARAR e voltar à Etapa 1.5.

```json
// Tool: mcp_notion-mcp-server_API-patch-block-children
{
  "block_id": "{task_page_id}",
  "children": [
    { "type": "divider", "divider": {} },
    { "type": "callout", "callout": { "icon": { "type": "emoji", "emoji": "✅" }, "rich_text": [{ "type": "text", "text": { "content": "Concluído em {data} — Tempo: {tempo}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📋 O que foi feito: {copiar de Etapa 1.5 → 'O que foi feito'}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📁 Arquivos: {copiar de Etapa 1.5 → 'Arquivos modificados' — listar path + tipo}" } }] } },
    { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "🧪 Verificação: {copiar de Etapa 1.5 → 'Verificação' — TS/Testes/Build}" } }] } }
  ]
}
```

### Etapa 3: Adicionar Comentário Rico (OBRIGATÓRIO)
> **Idioma:** Usar idioma definido em `PROJECT-PROGRESS.md` (PT-BR ou EN)

> [!CAUTION]
> O comentário DEVE conter detalhes técnicos reais extraídos do **Resumo de Execução** (Etapa 1.5).
> NÃO usar frases genéricas como "implementado conforme solicitado" ou "ajustes realizados".
> O comentário é o registro permanente que o usuário consultará para entender o que foi feito.

#### 🇧🇷 Português (PT-BR)
```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{task_page_id}" },
  "rich_text": [{
    "text": {
      "content": "✅ Task Concluída\n\n📋 O que foi feito:\n{copiar de Etapa 1.5 → 'O que foi feito' — cada mudança como bullet}\n\n📁 Arquivos modificados:\n{copiar de Etapa 1.5 → tabela de arquivos como bullets: • path — tipo — detalhe}\n\n🧪 Verificação:\n{copiar de Etapa 1.5 → 'Verificação' como bullets}\n\n🔗 Próximos passos:\n• {task relacionada ou 'Nenhum'}"
    }
  }]
}
```

#### 🇺🇸 English (EN)
```json
// Tool: mcp_notion-mcp-server_API-create-a-comment
{
  "parent": { "page_id": "{task_page_id}" },
  "rich_text": [{
    "text": {
      "content": "✅ Task Completed\n\n📋 What was done:\n{copy from Etapa 1.5 → 'O que foi feito' — each change as bullet}\n\n📁 Modified files:\n{copy from Etapa 1.5 → file table as bullets: • path — type — detail}\n\n🧪 Verification:\n{copy from Etapa 1.5 → 'Verificação' as bullets}\n\n🔗 Next steps:\n• {related task or 'None'}"
    }
  }]
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
- [ ] **Resumo de Execução produzido** (Etapa 1.5 — com O que foi feito, Arquivos, Verificação)
- [ ] Notion atualizado (Status + Tempo Gasto + %)
- [ ] **Nota de conclusão** adicionada no corpo (`patch-block-children`) — com dados da Etapa 1.5
- [ ] **Comentário rico** adicionado (no idioma do projeto) — com dados da Etapa 1.5
- [ ] **Docs impactados** verificados e atualizados? (buscar arquivos modificados em `docs/flows/` e `docs/design/`)
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
