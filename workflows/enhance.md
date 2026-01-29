---
description: Add or update features in existing application with mandatory Notion tracking.
---

# /enhance - Update Application (Notion First)

$ARGUMENTS

---

## 🎯 PROPÓSITO

Este workflow executa melhorias rápidas, bugfixes ou pequenas features, garantindo que **tudo seja registrado no Notion** ANTES da execução.

---

## 🚫 REGRA ABSOLUTA (LEIA PRIMEIRO)

> [!CAUTION]
> **VOCÊ NÃO PODE ESCREVER CÓDIGO OU MODIFICAR ARQUIVOS ANTES DE COMPLETAR A FASE 2.**
> 
> A Task no Notion DEVE existir e você DEVE ter o `page_id` salvo antes de qualquer ação de implementação.
> 
> **Se pular esta regra = VIOLAÇÃO DE PROTOCOLO.**

---

## 🔴 FLUXO OBRIGATÓRIO: Track → Plan → Apply → Update

### ✅ Fase 1: PRE-FLIGHT CHECK (Schema Validation)

**Trigger:** IMEDIATAMENTE ao receber `/enhance`

**Ações OBRIGATÓRIAS:**

1. **Buscar Database "Tasks" no Notion:**
   ```
   Use: mcp_notion-mcp-server_API-post-search
   Query: "Tasks" ou "Tarefas"
   Filter: { "property": "object", "value": "data_source" }
   ```

2. **Validar Schema do Database:**
   ```
   Use: mcp_notion-mcp-server_API-retrieve-a-data-source
   Verificar propriedades: Status, Prioridade
   ```

3. **Se faltar propriedades:**
   ```
   🛑 ERRO DE CONFIGURAÇÃO DO NOTION
   
   O database selecionado não tem as colunas obrigatórias:
   - Status (Select)
   - Prioridade (Select)
   
   Por favor, adicione-as no Notion e tente novamente.
   ```
   **→ PARAR AQUI. Não prosseguir.**

4. **Se OK:** Guardar `database_id` e prosseguir para Fase 2.

---

### 🚨 GATE 1: Só prossiga se tiver `database_id`

---

### ✅ Fase 2: TRACK (Notion Creation) — OBRIGATÓRIO

**Trigger:** `database_id` obtido na Fase 1

**Ação OBRIGATÓRIA:**

1. **Criar Task no Notion:**
   ```
   Use: mcp_notion-mcp-server_API-post-page
   
   parent: { "database_id": "<database_id>" }
   properties: {
     "title": { "title": [{ "text": { "content": "[ENHANCE] {Resumo}" } }] },
     "Status": { "select": { "name": "Em Progresso" } },
     "Prioridade": { "select": { "name": "P1" } }
   }
   ```

2. **Guardar `page_id` da resposta.**

3. **Confirmar para o usuário:**
   ```
   ✅ Task criada no Notion!
   📋 ID: {page_id}
   🔗 Link: https://notion.so/{page_id}
   
   Iniciando análise...
   ```

---

### 🚨 GATE 2: Só prossiga se tiver `page_id` da Task criada

> [!IMPORTANT]
> **Se a criação falhar:**
> Pergunte ao usuário: "A API do Notion falhou. Deseja prosseguir sem tracking (modo offline)?"
> - Se SIM: Prosseguir, mas avisar que não haverá registro.
> - Se NÃO: Parar.

---

### ✅ Fase 3: PLAN & EXECUTE

**Trigger:** `page_id` obtido na Fase 2

**Agentes:** Inferir baseado na solicitação (`frontend-specialist`, `backend-specialist`, etc.)

**Ações:**
1. **Understand:** Analisar contexto do projeto
2. **Plan:** Determinar arquivos afetados
3. **Apply:** Executar as mudanças

---

### ✅ Fase 4: VERIFY & UPDATE

**Trigger:** Após aplicar mudanças

**Ações:**

1. **Verificar:** Rodar testes ou lint (se aplicável)

2. **Atualizar Task no Notion:**
   ```
   Use: mcp_notion-mcp-server_API-patch-page
   page_id: {page_id guardado}
   properties: {
     "Status": { "select": { "name": "Feito" } }
   }
   ```

3. **Adicionar comentário:**
   ```
   Use: mcp_notion-mcp-server_API-create-a-comment
   parent: { "page_id": "{page_id}" }
   rich_text: [{ "text": { "content": "✅ Implementado em {data}.\nArquivos: {lista}" } }]
   ```

4. **Notificar Usuário:**
   ```
   🚀 ENHANCE CONCLUÍDO
   
   📋 Task: [Link Notion] (Status: Feito)
   📂 Arquivos alterados: file1.ts, file2.css
   
   Pronto para próxima tarefa.
   ```

---

## Usage Examples

```bash
# Melhora de UI
/enhance mudar cor do botão de login para primária

# Bugfix
/enhance corrigir erro 500 no checkout

# Feature pequena
/enhance adicionar filtro de data na listagem
```

---

## ⚠️ REGRAS FINAIS

| Regra | Descrição |
|-------|-----------|
| **Notion First** | NUNCA escreva código antes de criar a Task |
| **Gate Enforcement** | Cada fase tem um GATE que bloqueia a próxima |
| **Fallback Mode** | Se Notion falhar, PERGUNTE antes de prosseguir |
| **Scope Creep** | Se >4h de trabalho, sugerir `/tdd` ou `/discovery` |
