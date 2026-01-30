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

1.  **Buscar Database:**
    *   Tente encontrar o database de tarefas do projeto.
    *   *Queries sugeridas:* "Tasks", "Tarefas", "Daily", "Sprint".
    ```
    Use: mcp_notion-mcp-server_API-post-search
    filter: { "property": "object", "value": "database" }
    query: "Tarefas" // ou nome inferido do projeto
    ```

2.  **Validar Schema (OBRIGATÓRIO):**
    *   Ao encontrar o Database, analise suas propriedades (`properties`).
    *   **Propriedades OBRIGATÓRIAS:**
    
    | Propriedade | Tipo | Descrição |
    |-------------|------|-----------|
    | `Status` | status | "A Fazer", "Em andamento", "Concluído" |
    | `% Progresso` | number | Progresso de 0 a 100 |
    | `Tempo Gasto` | rich_text | Ex: "2h30m" |
    | `Categoria` | multi_select | "Aprimoramento", "Bug", "Feature" |
    | `Estimativa` | rich_text | Ex: "2h", "4h", "8h" (em horas) |
    | `Prioridade` | select | "P0", "P1", "P2" |

3.  **Check de Propriedades Ausentes:**
    *   Se QUALQUER propriedade obrigatória **NÃO** existir no schema:
        > 🛑 **PARE E INFORME:**
        ```
        ⚠️ Propriedades ausentes no database '{Nome}':
        
        | Propriedade | Tipo Esperado |
        |-------------|---------------|
        | {nome} | {tipo} |
        
        Por favor, crie estas propriedades no Notion antes de continuar.
        ```
    *   **NÃO prossiga** até que todas as propriedades existam.

---

### 📚 Fase 0.5: CONTEXT CHECK (Documentação)

**Objetivo:** Garantir contexto antes de implementar.

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

**Para CADA Task definida:**

1.  **Criar Página (TODAS as propriedades são obrigatórias):**
    ```
    Use: mcp_notion-mcp-server_API-post-page
    
    parent: { "database_id": "{DATABASE_ID_ENCONTRADO}" }
    properties: {
      "{Nome do Título}": { "title": [{ "text": { "content": "[TASK] {Titulo}" } }] },
      "Status": { "status": { "name": "Em andamento" } },
      "% Progresso": { "number": 0 },
      "Categoria": { "multi_select": [{ "name": "Aprimoramento" }] },
      "Estimativa": { "rich_text": [{ "text": { "content": "{Xh}" } }] },
      "Prioridade": { "select": { "name": "{P0/P1/P2}" } },
      "Tempo Gasto": { "rich_text": [{ "text": { "content": "0h" } }] }
    }
    ```

2.  **Definir Subitens (OBRIGATÓRIO):**
    > [!IMPORTANT]
    > Toda task DEVE ter subitens definidos para tracking de progresso.
    
    *   Lista de subitens com peso para cálculo de `% Progresso`
    *   Soma dos pesos deve ser 100%
    
    ```
    Use: mcp_notion-mcp-server_API-patch-block-children
    block_id: {page_id}
    children: [
        { "heading_2": { "rich_text": [{ "text": { "content": "📋 Checklist de Subitens" } }] } },
        { "to_do": { "rich_text": [{ "text": { "content": "Subitem 1 (30%)" } }], "checked": false } },
        { "to_do": { "rich_text": [{ "text": { "content": "Subitem 2 (40%)" } }], "checked": false } },
        { "to_do": { "rich_text": [{ "text": { "content": "Subitem 3 (30%)" } }], "checked": false } }
    ]
    ```

3.  **Detalhar Plano Técnico (Body):**
    ```
    Use: mcp_notion-mcp-server_API-patch-block-children
    block_id: {page_id}
    children: [
        { "heading_2": { "rich_text": [{ "text": { "content": "📋 Plano Técnico" } }] } },
        { "paragraph": { "rich_text": [{ "text": { "content": "{Detalhes do plano...}" } }] } }
    ]
    ```

4.  **Confirmar:**
    *   Liste IDs e Links.

---

### 💻 Fase 3: EXECUTION (Code)

**Ação:** Implementar as mudanças.

> [!IMPORTANT]
> **Atualização por Subitem:** A cada subitem concluído, atualizar o Notion.

**Para CADA Subitem Concluído:**

1.  **Calcular Novo Progresso:**
    *   Somar o peso do subitem ao `% Progresso` atual
    *   Exemplo: Se subitem tem 30% e atual é 20%, novo = 50%

2.  **Atualizar Notion:**
    ```
    Use: mcp_notion-mcp-server_API-patch-page
    
    page_id: {page_id_da_task}
    properties: {
        "% Progresso": { "number": {novo_progresso} }
    }
    ```

3.  **Adicionar Comentário de Progresso:**
    ```
    Use: mcp_notion-mcp-server_API-create-a-comment
    parent: { "page_id": "{page_id}" }
    rich_text: [{ "text": { "content": "✅ Subitem concluído: {descrição}\n📊 Progresso: {novo_progresso}%" } }]
    ```

4.  **Registrar Internamente:**
    *   Manter lista de arquivos modificados para o resumo final

---

### ✅ Fase 4: COMPLETION (Verify & Report)

**Ação Final:**

1.  **Verificar TODOS os Itens Antes de Concluir:**
    > [!CAUTION]
    > **OBRIGATÓRIO:** Antes de marcar como "Concluído", verificar:
    > - [ ] Todos os arquivos foram modificados conforme o plano?
    > - [ ] O código funciona corretamente?
    > - [ ] Testes passaram (se aplicável)?
    
    **Se algum item NÃO foi resolvido → NÃO marque como Concluído!**

2.  **Atualizar Notion (Propriedades Obrigatórias):**
    ```
    Use: mcp_notion-mcp-server_API-patch-page
    
    page_id: {page_id_da_task}
    properties: {
        "Status": { "status": { "name": "Concluído" } },
        "% Progresso": { "number": 100 },
        "Tempo Gasto": { "rich_text": [{ "text": { "content": "{Xh}m" } }] }
    }
    ```

3.  **Comentário Final com Resumo:**
    ```
    Use: mcp_notion-mcp-server_API-create-a-comment
    parent: { "page_id": "{page_id}" }
    rich_text: [{ "text": { "content": "✅ **Feito!**\n⏱️ Tempo: {Tempo}\n\n📋 **Alterações:**\n- {lista de mudanças}\n\n📁 **Arquivos:**\n- {lista de arquivos}" } }]
    ```

---

## 📌 Matriz de Propriedades por Fase

> [!IMPORTANT]
> **Todas as propriedades são obrigatórias e devem ser preenchidas/atualizadas nas fases indicadas.**

| Propriedade | Fase 2 (Criação) | Fase 3 (Execução) | Fase 4 (Conclusão) |
|-------------|------------------|-------------------|--------------------|
| `Status` | ✅ "Em andamento" | - | ✅ "Concluído" |
| `% Progresso` | ✅ 0 | ✅ +N% (por subitem) | ✅ 100 |
| `Categoria` | ✅ Definido | - | - |
| `Estimativa` | ✅ "{Xh}" | - | - |
| `Prioridade` | ✅ Definido | - | - |
| `Tempo Gasto` | ✅ "0h" | - | ✅ "{total}" |

---

## 🚨 REGRAS CRÍTICAS DE ENFORCEMENT

> [!CAUTION]
> **REGRA BLOQUEANTE:** Este workflow **NÃO PODE TERMINAR** sem:
> 1. Criar task no Notion (Fase 2)
> 2. Atualizar status para "Concluído" (Fase 4)
> 3. Adicionar comentário de fechamento (Fase 4)

### ⚠️ Checklist de Finalização (OBRIGATÓRIO)

**Antes de ENCERRAR a conversa ou resposta, o agente DEVE verificar:**

- [ ] **Fase 2 executada?** Task criada no Notion com ID registrado?
- [ ] **Fase 3 concluída?** Todas as alterações implementadas?
- [ ] **Fase 4 executada?** 
  - [ ] `API-patch-page` chamado com Status = "Concluído"?
  - [ ] `API-create-a-comment` chamado com resumo?

### 🔄 Se a Execução for Longa/Interrompida

Se o agente precisar pausar ou a conversa for longa:

1. **ANTES de parar:** Atualizar Notion com progresso parcial
2. **Informar usuário:** "Task {ID} em progresso - X de Y itens concluídos"
3. **Ao retomar:** Verificar status atual no Notion antes de continuar

### ❌ O Que NUNCA Fazer

1. ❌ **Encerrar conversa** sem atualizar Notion
2. ❌ **Marcar como Concluído** sem verificar se TODOS os itens foram resolvidos
3. ❌ **Esquecer de criar** a task inicialmente (Fase 2)
4. ❌ **Pular o comentário final** com resumo das alterações

### ✅ Verificação de Conclusão Correta

Quando o usuário perguntar "verificar task" ou "checar Notion":

1. **Buscar task:** `API-post-search` com o nome/ID
2. **Ler status atual:** Verificar Status e comentários
3. **Comparar com trabalho feito:** 
   - Listar arquivos modificados na sessão
   - Verificar se correspondem ao escopo da task
4. **Se incompleto:** Perguntar ao usuário antes de marcar como Concluído
   ```
   ⚠️ A task "{nome}" tem os seguintes itens pendentes:
   - [ ] {item 1}
   - [ ] {item 2}
   
   Deseja marcar como Concluído mesmo assim?
   ```