---
description: Workflow obrigatório para finalizar tasks. Garante sync com tracker (Notion ou Local), logs de execução e atualização de progresso.
---

# /task-complete

> **OBRIGATÓRIO** ao finalizar qualquer task. Garante compliance com tracking patterns.
> Suporta **dois modos de tracking**: Notion (API) ou Local (`docs/TASKS.md`).
> O modo é definido pela configuração `Tracker de Tasks` em `PROJECT-PROGRESS.md`.

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

## Etapa 0: Identificar Modo de Tracking (PRE-REQUISITO)

> [!CAUTION]
> **REGRA:** Ao INICIAR qualquer trabalho vinculado a uma task, o agente DEVE:
> 1. Ler `PROJECT-PROGRESS.md` → seção `Configurações` → campo `Tracker de Tasks`
> 2. **Se Notion:** Identificar o `page_id` da task (via `API-post-search` ou `API-query-data-source`)
> 3. **Se Local:** Identificar a linha/checkbox correspondente em `docs/TASKS.md`
>
> Sem essa identificação, as etapas de sync são impossíveis e serão esquecidas.

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

### Etapa 2: Atualizar Tracker

#### Se Tracker = Notion:
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

#### Se Tracker = Local:
Editar `docs/TASKS.md` — alterar `- [ ]` para `- [x]` na task correspondente.

### Etapa 2.5: Adicionar Nota de Conclusão (INLINE — NÃO PULAR)

> [!CAUTION]
> Os campos abaixo DEVEM ser preenchidos com os dados do **Resumo de Execução** (Etapa 1.5).
> NÃO usar placeholders genéricos. Se o Resumo de Execução não foi produzido, PARAR e voltar à Etapa 1.5.

#### Se Tracker = Notion:
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

#### Se Tracker = Local:
Nenhuma ação extra necessária (o checkbox `[x]` já foi marcado na Etapa 2).

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

### Etapa 5: Retorno ao Workflow Pai (OBRIGATÓRIO)

> [!IMPORTANT]
> Após completar o sync da task, o agente DEVE verificar se foi invocado
> dentro de um loop de workflow (Phase 7B do `/legacy-project`).

1. Verificar se existe seção `🔧 TASK ATIVA` no `LEGACY-PROGRESS.md`
2. **Se SIM** → Limpar a seção `🔧 TASK ATIVA` e retornar ao loop da Phase 7B (seção `🔁 LOOP CONTINUATION`)
3. **Se NÃO** → Tarefa standalone, encerrar normalmente
4. Verificar em `LEGACY-PROGRESS.md` se há tasks `[ ]` pendentes na Phase 7B atual

> [!WARNING]
> O agente NÃO DEVE encerrar a sessão após `/task-complete` se ainda há tasks
> pendentes no loop da Phase 7B. O encerramento prematuro perde o contexto
> do loop e exige re-invocação manual com `--resume`.

---

## Checklist de Conclusão

Antes de prosseguir para próxima task:

- [ ] Log de Execução exibido
- [ ] **Resumo de Execução produzido** (Etapa 1.5 — com O que foi feito, Arquivos, Verificação)
- [ ] **Tracker atualizado** (Notion: Status + Tempo Gasto + % | Local: checkbox `[x]`)
- [ ] **Nota de conclusão** (Notion: `patch-block-children` | Local: N/A)
- [ ] **Comentário rico** (Notion: `create-a-comment` | Local: N/A)
- [ ] **Docs impactados** verificados e atualizados?
- [ ] PROJECT-PROGRESS.md atualizado
- [ ] **Retorno ao workflow pai** verificado (Etapa 5)
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
- **ANTES de chamar `notify_user` para reportar conclusão de trabalho vinculado a uma task Notion**

> 🔴 **REGRA:** O agente NÃO pode prosseguir para próxima task sem executar este workflow.

---

## 🛑 REGRA UNIVERSAL DE ENFORCEMENT (Anti-Bypass)

> [!CAUTION]
> **REGRA BLOQUEANTE ABSOLUTA — APLICA-SE A QUALQUER CONTEXTO:**
>
> Se o agente completou trabalho que corresponde a uma task rastreada
> (no Notion ou em `docs/TASKS.md`), ele **DEVE** executar `/task-complete`
> **ANTES** de:
>
> - Chamar `notify_user` para reportar conclusão
> - Iniciar a próxima task
> - Encerrar a sessão
>
> **SELF-CHECK antes de `notify_user`:**
> ```
> ❓ Existe task rastreada vinculada ao trabalho que acabei de fazer?
> → SIM → Executar /task-complete ANTES de notify_user
> → NÃO → Prosseguir com notify_user normalmente
> ```
>
> **VIOLAÇÃO:** Chamar `notify_user` reportando task concluída SEM ter executado
> `/task-complete` é uma violação de compliance. O tracker ficará dessincronizado.
