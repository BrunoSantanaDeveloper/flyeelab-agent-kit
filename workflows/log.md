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
   | fix | Correção de bugs |
   | feat | Novo recurso |
   | refac | Aprimoramento |
   | docs | Aprimoramento |
   | chore | Aprimoramento |

3. **Inferir agente responsável** (apenas para registro interno, não enviar ao Notion se não houver campo)

---

### ✅ Fase 2: TRACK (Criar Task no Notion)

**Ações OBRIGATÓRIAS:**

1. **Criar Task no Database "Daily → Tático":**
   ```
   Use: mcp_notion-mcp-server_API-post-page
   
   parent: { "database_id": "2df85c5d-674f-80f6-8086-fdbce0dec151" }
   properties: {
     "title": { "title": [{ "text": { "content": "[LOG] {Descrição}" } }] },
     "Status": { "status": { "name": "Concluído" } },
     "Prioridade": { "select": { "name": "Média" } }, 
     "Categoria": { "multi_select": [{ "name": "{categoria}" }] },
     "Estimativa": { "select": { "name": "Pequeno" } }
   }
   ```
   *(Nota: Se Prioridade "Média" falhar, tente "Medium" ou remova)*

2. **Adicionar corpo da página (APENAS User History):**
   ```
   Use: mcp_notion-mcp-server_API-patch-block-children
   block_id: {page_id da task criada}
   children: [
     {
       "object": "block",
       "type": "paragraph",
       "paragraph": {
         "rich_text": [{ "type": "text", "text": { "content": "{Descrição detalhada}" } }]
       }
     }
   ]
   ```

3. **Confirmar para o usuário:**
   ```
   ✅ TRABALHO REGISTRADO (Retroativo)
   
   📋 Task: [Link Notion]
   🏷️ Categoria: {categoria}
   
   Status definido como "Concluído".
   ```

---

### ✅ Fase 3: CONFIRM

**Output:** Mensagem de sucesso simples.

---

## ⚙️ OPÇÕES AVANÇADAS

- `--commit`: Adiciona link do commit na descrição.
- `--priority`: Alta, Média, Baixa.

---

## ⚠️ REGRAS

| Regra | Descrição |
|-------|-----------|
| **Hardcoded ID** | Use o ID `2df85c5d...` para evitar erros de busca |
| **Clean Body** | O corpo deve conter APENAS o histórico/descrição |
| **Status Type** | Use propriedade `status`, não `select` |
