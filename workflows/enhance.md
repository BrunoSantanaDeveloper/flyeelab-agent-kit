---
description: Add or update features with mandatory Analysis, Splitting, and Notion tracking. Supports dynamic database discovery.
skills: notion-task-patterns, checkpointing-patterns, history-check-patterns, project-tracking-patterns
---

# /enhance - Structured Improvement Workflow

$ARGUMENTS

**Flags:**

| Flag | Descrição |
|------|-----------|
| `--tdd` | Modo **TDD obrigatório** (testes antes do código) |
| `--resume` | **Retomar** de onde parou |
| `--skip-history` | Pular consulta de histórico (não recomendado) |

---

## 🎯 PROPÓSITO

Workflow para melhorias e correções que exige **Análise Prévia** e **Registro no Notion**.
Totalmente dinâmico: adapta-se ao projeto atual buscando o database correto.

---

## 💾 SISTEMA DE CHECKPOINTING

> [!IMPORTANT]
> O workflow mantém estado em **dois lugares**:
> - `docs/ENHANCE-PROGRESS.md` (local)
> - Task no Notion (remoto)

### Arquivo Local: `docs/ENHANCE-PROGRESS.md`

```markdown
# Enhance Progress - {feature}

## Status
| Campo | Valor |
|-------|-------|
| Feature | {nome} |
| Iniciado | {data} |
| Fase Atual | 3/5 - Execution |
| Notion Task | {link} |

## Subitens
| # | Subitem | Peso | Status |
|---|---------|------|--------|
| 1 | Análise | 10% | ✅ |
| 2 | Setup testes | 20% | ✅ |
| 3 | Implementar X | 30% | 🟡 |
| 4 | Implementar Y | 30% | ⏳ |
| 5 | Verificação | 10% | ⏳ |

## Histórico
| Data | Ação |
|------|------|
| ... | ... |
```

### Retomada

```bash
/enhance --resume
```

1. Carrega `docs/ENHANCE-PROGRESS.md`
2. Busca task correspondente no Notion
3. Continua da fase pendente

---

## 🚫 FLUXO: HISTORY → DISCOVER → ANALYSE → TRACK → EXECUTE → VERIFY

> [!CAUTION]
> **REGRA DE OURO:** NUNCA use IDs fixos. Sempre busque o contexto do projeto atual.

---

### 🕵️ Fase -1: HISTORY CHECK (Aprender com o passado)

> [!IMPORTANT]
> **OBRIGATÓRIO** antes de implementar qualquer coisa.
> Evita repetir erros e reimplementar soluções já feitas.

**Objetivo:** Consultar histórico de tarefas relacionadas à demanda.

**1. Buscar Tasks Relacionadas no Notion:**
```
Use: mcp_notion-mcp-server_API-post-search
query: "{palavras-chave da demanda}"
filter: { "property": "object", "value": "page" }
```

**2. Buscar por Categoria:**
```
Use: mcp_notion-mcp-server_API-query-data-source
data_source_id: "{DATABASE_ID}"
filter: {
    "or": [
        { "property": "Categoria", "multi_select": { "contains": "Bug" } },
        { "property": "Categoria", "multi_select": { "contains": "Feature" } }
    ]
}
```

**3. Analisar Resultados:**

| Tipo | O que procurar |
|------|----------------|
| **Bugs Resolvidos** | Mesma área? Mesmo componente? |
| **Features Anteriores** | Já implementado algo similar? |
| **Comentários** | Problemas encontrados? Soluções aplicadas? |

**4. Se Encontrar Histórico Relevante:**
```
📚 **Histórico Encontrado:**

| Task | Tipo | Data | Relevância |
|------|------|------|------------|
| [#123] Auth refactor | Feature | 2025-01-10 | Alta - mesmo módulo |
| [#98] Fix login erro | Bug | 2025-01-05 | Média - pode recorrer |

**Lições aprendidas:**
- Em #123: "Usar middleware novo, não o legado"
- Em #98: "Race condition no token refresh"

**Aplicar:**
- [ ] Verificar se solução de #98 ainda se aplica
- [ ] Seguir padrão estabelecido em #123
```

**5. Se NÃO Encontrar:**
```
✅ Nenhum histórico relevante encontrado para "{demanda}".
Prosseguindo com análise do zero.
```

**Gate de Saída:**
```
[ ] Histórico consultado
[ ] Lições identificadas (se houver)
[ ] Checkpoints anteriores verificados
```

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
      "{Nome do Título}": { "title": [{ "text": { "content": "{Titulo}" } }] },
      "ID": { "rich_text": [{ "text": { "content": "{N.X}" } }] },
      "Épico": { "select": { "name": "{Nome do Épico ou 'Melhoria'}" } },
      "Status": { "status": { "name": "Em Progresso" } },
      "% Progresso": { "number": 0 },
      "Categoria": { "multi_select": [{ "name": "Melhoria" }] },
      "Estimativa": { "rich_text": [{ "text": { "content": "{Xh}" } }] },
      "Prioridade": { "select": { "name": "{P0/P1/P2}" } },
      "Tempo Gasto": { "rich_text": [{ "text": { "content": "0h" } }] }
    }
    ```
    
    > **ID para Melhorias:** Se não houver épico definido, usar `M.{seq}` (ex: `M.1`, `M.2`)

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
    *   Atualizar `docs/ENHANCE-PROGRESS.md`

---

### 🧪 Fase 3.5: TDD METODOLOGIA (Se --tdd)

> [!NOTE]
> **Ativado com:** `/enhance --tdd [descrição]`
> **Obrigatório para:** Features complexas, código crítico, ou quando solicitado.

**Objetivo:** Garantir testes antes do código.

**1. RED - Escrever Testes Primeiro:**
```
Para cada funcionalidade:
1. Escrever teste que FALHA
2. Confirmar que teste falha pelo motivo certo
3. Registrar no checkpoint
```

**2. GREEN - Implementar Mínimo:**
```
1. Escrever código MÍNIMO para passar o teste
2. Rodar testes
3. Confirmar que passam
```

**3. REFACTOR - Melhorar:**
```
1. Refatorar código mantendo testes passando
2. Limpar duplicações
3. Melhorar legibilidade
```

**Atualizar Notion após cada ciclo:**
```
Use: mcp_notion-mcp-server_API-create-a-comment
parent: { "page_id": "{page_id}" }
rich_text: [{ "text": { "content": "🔴 RED: {teste}\n🟢 GREEN: {implementação}\n🔵 REFACTOR: {melhoria}" } }]
```

---

### 🎨 Fase 3.7: UI STYLING (Se feature tem UI)

> [!NOTE]
> **Ativado se:** A feature envolve componentes visuais, páginas ou mudanças de UI.
> **Pulado se:** Feature é apenas backend, API ou lógica sem interface.

**Objetivo:** Garantir que UI segue Design System e padrões profissionais.

**1. Verificar Design System Existente:**
```bash
# Verificar se existe Design System
cat design-system/MASTER.md 2>/dev/null || cat docs/design/DESIGN-SYSTEM-*.md 2>/dev/null
```

**2. Se NÃO Existir Design System:**
```bash
# Gerar Design System com /ui-ux-pro-max
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "{produto} {indústria}" --design-system --persist -p "{Projeto}"
```

**3. Se Existir, Carregar e Aplicar:**
```bash
# Buscar guidelines específicas do stack
python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "{componentes}" --stack {html-tailwind|react|nextjs}
```

**4. Pre-Delivery Checklist (OBRIGATÓRIO para UI):**

```markdown
### Visual Quality
- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] Hover states don't cause layout shift
- [ ] Theme colors applied correctly

### Interaction
- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation

### Light/Dark Mode
- [ ] Light mode text has sufficient contrast (4.5:1)
- [ ] Glass/transparent elements visible in light mode
- [ ] Test both modes before delivery

### Responsive
- [ ] Works at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile
```

**Gate de Saída:**
```
[ ] Design System carregado/criado
[ ] Pre-Delivery Checklist verificado
[ ] UI revisada visualmente
```

---

### ✅ Fase 4: VERIFICATION & COMPLETION

**Ação Final:**

1.  **Gate de Cobertura (OBRIGATÓRIO se --tdd):**
    > [!CAUTION]
    > Se `--tdd` foi usado, verificar cobertura antes de concluir.
    
    ```bash
    # Verificar cobertura
    npm run test:coverage  # ou equivalente
    ```
    
    | Cobertura | Ação |
    |-----------|------|
    | >= 80% | ✅ Prosseguir para conclusão |
    | < 80% | ⚠️ Adicionar mais testes ou justificar |
    
    **Se cobertura insuficiente:**
    ```
    ⚠️ Cobertura atual: {X}% (mínimo: 80%)
    
    Opções:
    1. Adicionar testes para aumentar cobertura
    2. Justificar exceção (código legado, UI, etc.)
    
    Qual opção?
    ```

2.  **Verificar TODOS os Itens Antes de Concluir:**
    > [!CAUTION]
    > **OBRIGATÓRIO:** Antes de marcar como "Concluído", verificar:
    > - [ ] Todos os arquivos foram modificados conforme o plano?
    > - [ ] O código funciona corretamente?
    > - [ ] Testes passaram (se aplicável)?
    > - [ ] Cobertura >= 80% (se --tdd)?
    
    **Se algum item NÃO foi resolvido → NÃO marque como Concluído!**

3.  **Atualizar Notion (Propriedades Obrigatórias):**
    ```
    Use: mcp_notion-mcp-server_API-patch-page
    
    page_id: {page_id_da_task}
    properties: {
        "Status": { "status": { "name": "Concluído" } },
        "% Progresso": { "number": 100 },
        "Tempo Gasto": { "rich_text": [{ "text": { "content": "{Xh}m" } }] }
    }
    ```

4.  **Comentário Final com Resumo:**
    ```
    Use: mcp_notion-mcp-server_API-create-a-comment
    parent: { "page_id": "{page_id}" }
    rich_text: [{ "text": { "content": "✅ **Feito!**\n⏱️ Tempo: {Tempo}\n🧪 Cobertura: {X}%\n\n📋 **Alterações:**\n- {lista de mudanças}\n\n📁 **Arquivos:**\n- {lista de arquivos}\n\n📚 **Histórico aplicado:**\n- {lições de tasks anteriores usadas}" } }]
    ```

5.  **Atualizar Checkpoint Local:**
    ```markdown
    # Em docs/ENHANCE-PROGRESS.md
    Status: ✅ Concluído
    Cobertura Final: {X}%
    Tasks Relacionadas: [#123, #98]
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