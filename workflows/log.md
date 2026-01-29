---
description: Registrar trabalho já concluído no Notion. Para bugs corrigidos, features implementadas ou tarefas feitas antes do tracking.
---

# /log - Registrar Trabalho Retroativo

$ARGUMENTS

---

## 🎯 PROPÓSITO

Este workflow registra no Notion trabalhos que **já foram concluídos** antes de serem rastreados. Ideal para:

- 🐛 Bugs corrigidos sem Task prévia
- ✨ Features implementadas rapidamente
- 🔧 Ajustes feitos durante debug
- 📝 Documentar trabalho técnico realizado

---

## 📋 SINTAXE

```bash
/log <tipo> "<descrição>"

# Tipos disponíveis:
# fix    → Bugfix
# feat   → Feature/melhoria
# refac  → Refatoração
# docs   → Documentação
# chore  → Manutenção/configs
```

### Exemplos

```bash
/log fix "Corrigi erro de validação no CFOP 5101"
/log feat "Adicionei filtro de data na listagem"
/log refac "Reorganizei estrutura de pastas do módulo fiscal"
/log docs "Atualizei README com instruções de deploy"
```

---

## 🔴 FLUXO: Parse → Track → Confirm

### ✅ Fase 1: PARSE (Entender a Solicitação)

**Trigger:** Ao receber `/log`

**Ações:**
1. **Extrair tipo e descrição** do argumento
2. **Inferir categoria:**
   | Tipo | Categoria Notion |
   |------|------------------|
   | fix | Bugfix |
   | feat | Feature |
   | refac | Refatoração |
   | docs | Documentação |
   | chore | Manutenção |

3. **Inferir agente responsável** baseado na descrição:
   - Menções a "API", "backend", "database" → `backend-specialist`
   - Menções a "UI", "CSS", "tela", "botão" → `frontend-specialist`
   - Menções a "mobile", "app" → `mobile-developer`
   - Default: `orchestrator`

4. **Detectar arquivos alterados (opcional):**
   - Se houver commit recente, extrair lista de arquivos
   - `git diff --name-only HEAD~1` (últimos arquivos alterados)

---

### ✅ Fase 2: TRACK (Criar Task no Notion como Feita)

**Ações OBRIGATÓRIAS:**

1. **Buscar Database "Tasks" no Notion:**
   ```
   Use: mcp_notion-mcp-server_API-post-search
   Query: "Tasks" ou "Tarefas"
   Filter: { "property": "object", "value": "data_source" }
   ```

2. **Criar Task com Status = Feito:**
   ```
   Use: mcp_notion-mcp-server_API-post-page
   
   parent: { "database_id": "<database_id>" }
   properties: {
     "title": { "title": [{ "text": { "content": "[LOG] {Descrição}" } }] },
     "Status": { "select": { "name": "Feito" } },
     "Prioridade": { "select": { "name": "P2" } },
     "Categoria": { "select": { "name": "{categoria}" } }
   }
   ```

3. **Adicionar comentário com detalhes:**
   ```
   Use: mcp_notion-mcp-server_API-create-a-comment
   parent: { "page_id": "{page_id}" }
   rich_text: [{
     "text": {
       "content": "📝 Trabalho registrado retroativamente\n\n📅 Data: {data atual}\n🏷️ Tipo: {tipo}\n👤 Agente: {agente}\n📂 Arquivos: {lista ou 'N/A'}"
     }
   }]
   ```

---

### ✅ Fase 3: CONFIRM (Notificar Usuário)

**Output:**
```
✅ TRABALHO REGISTRADO NO NOTION

📋 Task: [Link Notion]
🏷️ Tipo: {tipo} ({categoria})
📅 Registrado em: {data/hora}
📂 Arquivos detectados: {lista ou "Nenhum detectado"}

O trabalho foi documentado com Status = Feito.
```

---

## ⚙️ OPÇÕES AVANÇADAS

### Com commit específico
```bash
/log fix "Descrição" --commit abc123
```
→ Extrai arquivos do commit específico e adiciona hash no comentário.

### Com arquivos manuais
```bash
/log feat "Descrição" --files "src/api.ts, src/utils.ts"
```
→ Usa lista de arquivos fornecida pelo usuário.

### Com prioridade
```bash
/log fix "Bug crítico em produção" --priority P0
```
→ Define prioridade específica em vez de P2 default.

---

## ⚠️ REGRAS

| Regra | Descrição |
|-------|-----------|
| **Sempre Feito** | Tasks criadas via `/log` SEMPRE têm Status = "Feito" |
| **Retroativo** | NUNCA execute código neste workflow, apenas registre |
| **Comentário Rich** | Sempre adicione comentário com contexto completo |
| **Fallback** | Se Notion falhar, pergunte se quer salvar localmente |

---

## 🔗 RELACIONADOS

- `/enhance` → Para trabalho futuro (criar task → executar → marcar done)
- `/task-commit` → Para atualizar task existente via commit
- `/execute` → Para executar task já existente no Notion
