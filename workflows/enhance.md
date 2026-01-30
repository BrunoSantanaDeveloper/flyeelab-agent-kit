---
description: Add or update features with mandatory Analysis, Splitting, and Notion tracking. Supports dynamic database discovery.
---

# /enhance - Structured Improvement Workflow

$ARGUMENTS

---

## 🎯 PROPÓSITO

Workflow para melhorias e correções que exige **Análise Prévia** e **Registro no Notion**.
Totalmente dinâmico: adapta-se ao projeto atual buscando o database correto.

---

## 🚫 FLUXO: DISCOVER → ANALYSE → TRACK → EXECUTE

> [!CAUTION]
> **REGRA DE OURO:** NUNCA use IDs fixos. Sempre busque o contexto do projeto atual.

---

### 🔍 Fase 0: DISCOVERY & SCHEMA (Setup)

**Objetivo:** Encontrar onde registrar as tarefas neste projeto.

**Agente Envolvido:** `explorer-agent`

1.  **Buscar Database:**
    *   Tente encontrar o database de tarefas do projeto.
    *   *Queries sugeridas:* "Tasks", "Tarefas", "Daily", "Sprint".
    ```
    Use: mcp_notion-mcp-server_API-post-search
    filter: { "property": "object", "value": "database" }
    query: "Tarefas" // ou nome inferido do projeto
    ```

2.  **Validar & Mapear Schema:**
    *   Ao encontrar o Database, analise suas propriedades (`properties`).
    *   **Mapeie mentalmente:**
        *   `Status` (Status)
        *   `Estimativa` (Select/Number)
        *   `Tempo Gasto` (Se existir)
    
3.  **Check de "Tempo Gasto":**
    *   Se a propriedade `Tempo Gasto` (ou `Time Spent`) **NÃO** existir no schema retornado:
        > 🛑 **PARE E PERGUNTE:** "O database '{Nome}' não tem campo de tempo. Deseja criar a propriedade 'Tempo Gasto' agora?"
        *   Se SIM: Crie (Type: Rich Text ou Number).
        *   Se NÃO: Trabalhe sem ela (apenas comentários).

---

### 📚 Fase 0.5: CONTEXT CHECK (Documentação)

**Objetivo:** Garantir contexto antes de implementar.

**Agente Envolvido:** `explorer-agent`

1. **Buscar Documentação Existente:**
   - Verificar `docs/INDEX.md` para lista de documentações
   - Procurar em `docs/flows/` por documentação do módulo afetado
   - Identificar documentos relacionados

2. **Se Documentação EXISTE:**
   - ✅ Carregar contexto do documento
   - Identificar componentes envolvidos
   - Listar casos de teste essenciais já documentados
   - Verificar dependências mapeadas

3. **Se Documentação NÃO EXISTE:**
   > 🛑 **PARE E PERGUNTE:** 
   > "Não há documentação para '{módulo/fluxo}'. Deseja criar agora com `/document` antes de prosseguir?"
   
   - Se **SIM**: Executar `/document {módulo}` primeiro
   - Se **NÃO**: Prosseguir com análise de código (anotar para documentar depois)

4. **Registrar Gap:**
   - Se prosseguiu sem documentação, adicionar comentário na task do Notion:
   > "⚠️ Implementado sem documentação prévia. Recomendado executar `/document` após conclusão."

---

### 🧠 Fase 1: ANÁLISE TÉCNICA (Offline/Mental)

**Trigger:** Database identificado e validado.

**Agentes Envolvidos:**
- `project-planner` - Decomposição e estimativa
- `backend-specialist` / `frontend-specialist` / `mobile-developer` - Conforme domínio

**1. Análise de Complexidade:**
   - O pedido toca em múltiplos contextos?
   - Tempo estimado > 2h?

**2. Estratégia de Particionamento (Split):**
   - **SIMPLES:** 1 Task.
   - **COMPLEXA:** Múltiplas sub-tasks.

**3. Estimativa:**
   - Defina a estimativa para cada task (P/M/G ou Pontos).

---

### 📝 Fase 2: TRACKING (Notion)

**Ação:** Criar as tasks no database ENCONTRADO na Fase 0.

**Agente Envolvido:** `project-planner`

**Para CADA Task definida:**

1.  **Criar Página:**
    *   Use o `id` do database encontrado dinamicamente.
    *   Adapte o payload às propriedades reais do banco.
    ```
    Use: mcp_notion-mcp-server_API-post-page
    
    parent: { "database_id": "{DATABASE_ID_ENCONTRADO}" }
    properties: {
      "{Nome do Título}": { "title": [{ "text": { "content": "[ENHANCE] {Titulo}" } }] },
      "{Nome do Status}": { "status": { "name": "Em andamento" } },
      
      // Propriedades Opcionais (Se existirem no schema):
      "{Nome da Categoria}": { "multi_select": [{ "name": "Aprimoramento" }] },
      "{Nome da Estimativa}": { "select": { "name": "{Valor}" } },
      
      // Se "Tempo Gasto" existir:
      "{Nome do Tempo Gasto}": { "rich_text": [{ "text": { "content": "0h" } }] }
    }
    ```

2.  **Detalhar Plano Técnico (Body):**
    ```
    Use: mcp_notion-mcp-server_API-patch-block-children
    block_id: {page_id}
    children: [
        { "paragraph": { "rich_text": [{ "text": { "content": "📋 **Plano Técnico:**\n{Detalhes...}" } }] } }
    ]
    ```

3.  **Confirmar:**
    *   Liste IDs e Links.

---

### 💻 Fase 3: EXECUTION (Code)

**Ação:** Implementar as mudanças.

**Agentes Envolvidos:**
- `backend-specialist` - Para lógica de API/serviços
- `frontend-specialist` - Para UI/componentes web
- `mobile-developer` - Para apps React Native/Flutter
- `test-engineer` - Para criação de testes

---

### ✅ Fase 4: COMPLETION (Verify & Report)

**Ação Final:**

**Agentes Envolvidos:**
- `test-engineer` - Validação de testes
- `security-auditor` - Revisão de segurança (se aplicável)

1.  **Atualizar Notion:**
    ```
    Use: mcp_notion-mcp-server_API-patch-page
    
    page_id: {page_id_da_task}
    properties: {
        "{Nome do Status}": { "status": { "name": "Concluído" } },
        // Se mapeado:
        "{Nome do Tempo Gasto}": { "rich_text": [{ "text": { "content": "{Tempo}" } }] }
    }
    ```

2.  **Comentário Final:**
    ```
    Use: mcp_notion-mcp-server_API-create-a-comment
    rich_text: [{ "text": { "content": "✅ **Feito!**\n⏱️ {Tempo}" } }]
    ```
