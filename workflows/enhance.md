---
description: Add or update features in existing application with mandatory Notion tracking.
---

# /enhance - Update Application (Notion First)

$ARGUMENTS

---

## 🎯 PROPÓSITO

Este workflow executa melhorias rápidas, bugfixes ou pequenas features, garantindo que **tudo seja registrado no Notion** antes da execução.

---

## 🔴 FLUXO: Track → Plan → Apply → Update

### Fase 1: PRE-FLIGHT CHECK (Schema Validation)

**Trigger:** Antes de criar qualquer task

**Ação:**
1. **Validar Schema do Database:**
   - Verificar se o database possui as propriedades necessárias: `Status` e `Prioridade`.
   - Se faltar:
     ```
     🛑 ERRO DE CONFIGURAÇÃO DO NOTION
     
     O database selecionado não tem as colunas obrigatórias:
     - Status
     - Prioridade (Select)
     
     Por favor, adicione-as no Notion e tente novamente.
     ```
   - Se OK: Prosseguir.

---

### Fase 2: TRACK (Notion Creation)

**Trigger:** Schema validado

**Agente:** `orchestrator`

**Ação:**
1. Criar Task no Notion via `notion-mcp-server`:
   - **Database:** "Tasks Database" (padrão)
   - **Título:** `[ENHANCE] {Resumo da instrução}`
   - **Status:** "In Progress"
   - **Prioridade:** "P1" (Default) ou inferida
   - **Estimativa:** "S" (Default)
   - **Agente:** Inferir baseado na solicitação (ex: Frontend, Backend)
   - **Corpo:** Descrição completa da solicitação original

2. **Output:**
   ```
   ✅ Schema Validado & Task criada: [Link]
   🆔 Início da execução...
   ```

---

### Fase 3: PLAN & EXECUTE

**Agentes:** `frontend-specialist`, `backend-specialist`, ou outros conforme necessidade.

**Ações:**
1. **Understand:** Carregar estado do projeto (`session_manager.py info`)
2. **Plan:** Determinar arquivos afetados
3. **Apply:** Executar as mudanças

---

### Fase 4: VERIFY & UPDATE

**Trigger:** Após aplicar mudanças

**Ações:**
1. **Verificar:** Rodar testes ou lint (se aplicável)
2. **Atualizar Task Notion:**
   - Mudar **Status** para "Done" (ou "Review" se houver dúvida)
   - Adicionar comentário no corpo da task: "Implementado em [data]. Arquivos alterados: X, Y, Z."

3. **Notificar Usuário:**
   ```
   🚀 ENHANCE CONCLUÍDO
   
   📋 Task: [Link Notion] (Marcada como Done)
   📂 Arquivos: file1.ts, file2.css
   
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

## ⚠️ CAUTION

- **Notion é Mandatório:** Se a API do Notion falhar, perguntar ao usuário se deseja prosseguir sem track (modo offline).
- **Scope Creep:** Se o pedido for muito grande (> 4h), sugerir usar `/tdd` ou `/discovery`.
