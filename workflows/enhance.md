---
description: Add or update features with mandatory Analysis, Splitting, and Tracker sync (Flyee or Local). Supports dynamic database discovery.
skills: checkpointing-patterns, history-check-patterns, context-gathering-patterns, project-tracking-patterns, ui-ux-discovery, local-verification, integration-completeness, design-system-enforcement

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

Workflow para melhorias e correções que exige **Análise Prévia** e **Registro no Tracker** (Flyee ou Local).
Totalmente dinâmico: adapta-se ao projeto atual buscando o contexto correto.

> [!IMPORTANT]
> **Tracker-aware:** Lê `PROJECT-PROGRESS.md` → `Tracker de Tasks` para determinar
> se cria tasks via Flyee API ou em `docs/TASKS.md`.

---

## 💾 SISTEMA DE CHECKPOINTING

> [!IMPORTANT]
> O workflow mantém estado em **dois lugares**:
> - `docs/ENHANCE-PROGRESS.md` (local)
> - Task no Flyee (remoto)

### Arquivo Local: `docs/ENHANCE-PROGRESS.md`

```markdown
# Enhance Progress - {feature}

## Status
| Campo | Valor |
|-------|-------|
| Feature | {nome} |
| Iniciado | {data} |
| Fase Atual | 3/5 - Execution |
| Flyee Task | {link} |

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
2. Busca task correspondente no Flyee
3. Continua da fase pendente

---

## 🚫 FLUXO: PRE-CHECK → HISTORY → DISCOVER → ANALYSE → TRACK → EXECUTE → VERIFY

> [!CAUTION]
> **REGRA DE OURO:** NUNCA use IDs fixos. Sempre busque o contexto do projeto atual.

---

### 🚨 Fase -2: PRE-START CHECK (Gate de Finalização)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Seguir Flyee API → Seção "GATE DE FINALIZAÇÃO".
> Verificar se há tasks "Em andamento" antes de criar/iniciar nova.

**Ações:**
1. Verificar tasks abertas (Status="Em andamento")
2. Se houver: Perguntar se deseja finalizar primeiro
3. Se usuário quiser finalizar: Executar conclusão com `Tempo Gasto`

---

### 🕵️ Fase -1: HISTORY CHECK (Aprender com o passado)

> [!IMPORTANT]
> **OBRIGATÓRIO** antes de implementar qualquer coisa.
> Evita repetir erros e reimplementar soluções já feitas.

**Objetivo:** Consultar histórico de tarefas relacionadas à demanda.

**1. Buscar Tasks Relacionadas no Flyee:**
```
Use: Flyee API: list_tasks()
query: "{palavras-chave da demanda}"
filter: { "property": "object", "value": "page" }
```

**2. Buscar por Categoria:**
```
Use: Flyee API: list_tasks()
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
    Use: Flyee API: list_tasks()
    filter: { "property": "object", "value": "database" }
    query: "Tarefas" // ou nome inferido do projeto
    ```

2.  **Validar Schema (OBRIGATÓRIO):**
    *   Ao encontrar o Database, analise suas propriedades (`properties`).
    *   **Seguir Flyee API** para lista de propriedades obrigatórias.

3.  **Check de Propriedades Ausentes:**
    *   Se QUALQUER propriedade obrigatória **NÃO** existir no schema:
        > 🛑 **PARE E INFORME:**
        ```
        ⚠️ Propriedades ausentes no database '{Nome}':
        
        | Propriedade | Tipo Esperado |
        |-------------|---------------|
        | {nome} | {tipo} |
        
        Por favor, crie estas propriedades no Flyee antes de continuar.
        ```
    *   **NÃO prossiga** até que todas as propriedades existam.

---

### 📚 Fase 0.5: CONTEXT CHECK (Documentação)

**Objetivo:** Garantir contexto antes de implementar.

1. **Buscar Documentação Existente:**
   - Verificar `docs/INDEX.md` para lista de documentações
   - Procurar em `docs/flows/` por documentação do módulo afetado
   - Identificar documentos relacionados
   - Buscar no Tracker em **AMBOS** databases:
     - **"Documentação Técnica"** — docs técnicos (fluxos, TDD, arquitetura)
     - **"Manual do Usuário"** — guias de usuário e operador

2. **Se Documentação EXISTE:**
   - ✅ Carregar contexto do documento
   - Identificar componentes envolvidos
   - Listar casos de teste essenciais já documentados
   - Verificar dependências mapeadas
   - Verificar se **Manual do Usuário** também precisa de atualização

3. **Se Documentação NÃO EXISTE:**
   > 🛑 **PARE E PERGUNTE:** 
   > "Não há documentação para '{módulo/fluxo}'. Deseja criar agora com `/document` antes de prosseguir?"
   
   - Se **SIM**: Executar `/document {módulo}` primeiro
   - Se **NÃO**: Prosseguir com análise de código (anotar para documentar depois)

4. **Registrar Gap:**
   - Se prosseguiu sem documentação, adicionar comentário na task do Flyee:
   > "⚠️ Implementado sem documentação prévia. Recomendado executar `/document` após conclusão."
   
5. **Ao concluir melhoria que afeta UX:**
   - Atualizar doc na "Documentação Técnica" (se existir)
   - Atualizar guia no "Manual do Usuário" (se existir)

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

### 📝 Fase 2: TRACKING (Flyee)

**Ação:** Criar as tasks no database ENCONTRADO na Fase 0.

**Para CADA Task definida:**

1.  **Criar Página:**
    
    > **Seguir Flyee API** → Seção "➕ Criar Task"
    
    > **ID para Melhorias:** Se não houver épico definido, usar `M.{seq}` (ex: `M.1`, `M.2`)

2.  **Definir Subitens (OBRIGATÓRIO):**
    > [!IMPORTANT]
    > Toda task DEVE ter subitens definidos para tracking de progresso.
    
    > **Seguir Flyee API** → Seção "📝 Adicionar Corpo"

3.  **Detalhar Plano Técnico (Body):**
    ```
    Use: Flyee API: update_task() (output)
    block_id: {page_id}
    children: [
        { "heading_2": { "rich_text": [{ "text": { "content": "📋 Plano Técnico" } }] } },
        { "paragraph": { "rich_text": [{ "text": { "content": "{Detalhes do plano...}" } }] } }
    ]
    ```

4.  **Confirmar:**
    *   Liste IDs e Links.

#### 🔔 FLYEE BRIDGE EMIT (Condicional)

> Se `flyee.json` existe E `enabled: true`:

```bash
python .agent/flyee-bridge/bridge.py emit "dev.workflow_started" '{"workflow": "enhance", "task_id": "{page_id}", "task_name": "{nome_da_feature}"}'
```

> Se bridge não configurado → Pular silenciosamente.

---

### 💻 Fase 3: EXECUTION (Code)

**Ação:** Implementar as mudanças.

> [!CAUTION]
> **GATE OBRIGATÓRIO:** Seguir skill `context-gathering-patterns` → seção "PROCESSO DE CONTEXT GATHERING"
> ANTES de implementar. Se Fase 0.5 já carregou contexto, verificar que checklist de evidência
> está persistido em `docs/ENHANCE-PROGRESS.md`. Se ausente, preencher agora.

> [!IMPORTANT]
> **Atualização por Subitem:** A cada subitem concluído, atualizar o Flyee.

**Para CADA Subitem Concluído:**

1.  **Adicionar Comentário de Progresso:**
    > **Seguir Flyee API** → Seção "💬 Adicionar Comentário"

2.  **Registrar Internamente:**
    *   Manter lista de arquivos modificados para o resumo final
    *   Atualizar `docs/ENHANCE-PROGRESS.md`

---

### 🧪 Fase 3.5: TDD METODOLOGIA (Se --tdd)

> [!NOTE]
> **Ativado com:** `/enhance --tdd [descrição]`
> **Obrigatório para:** Features complexas, código crítico, ou quando solicitado.

**Objetivo:** Garantir testes antes do código.

> [!IMPORTANT]
> **Para componentes com UI:** Seguir skill `design-system-enforcement` durante GREEN.
> Componentes devem usar MASTER.md desde a criação, não apenas na fase de styling.

**1. RED - Escrever Testes Primeiro:**
```
Para cada funcionalidade:
1. Escrever teste que FALHA
2. Confirmar que teste falha pelo motivo certo
3. Registrar no checkpoint
```

**2. GREEN - Implementar Mínimo (usando Design System se UI):**
```
1. Escrever código MÍNIMO para passar o teste
2. Se tem UI: Usar variáveis CSS do MASTER.md (skill: design-system-enforcement)
3. Rodar testes
4. Confirmar que passam
```

**3. REFACTOR - Melhorar:**
```
1. Refatorar código mantendo testes passando
2. Limpar duplicações
3. Melhorar legibilidade
```


**Atualizar Tracker após cada ciclo:**
```
Use: Flyee API: update_task() (output)
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
# Verificar se existe Design System (ordem de prioridade)
cat design-system/*/MASTER.md 2>/dev/null || cat docs/design/DESIGN-SYSTEM-*.md 2>/dev/null
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
[ ] Validação de integração UI→Função (skill: integration-completeness)
```

---

### 🛑 GATE: Fase 3.7 → Fase 4 (Se feature tem UI)

> [!CAUTION]
> **BLOQUEADOR:** Se a feature envolve UI, você NÃO PODE prosseguir sem completar Fase 3.7.

**Passo 1: Executar Validação Automatizada**

> **Skill:** `ui-validation`

```bash
python .agent/skills/ui-validation/scripts/ui_antipattern_check.py .
```

**Passo 2: Checklist (OBRIGATÓRIO)**
```markdown
⚠️ VERIFICAÇÃO ANTES DE COMPLETION

[ ] Design System aplicado?
[ ] Pre-Delivery Checklist 100%?
[ ] 🔴 ui-validation script PASSOU?
[ ] Verificação visual feita?

❌ Se QUALQUER item desmarcado → Voltar para Fase 3.7
✅ TODOS marcados → Prosseguir para Fase 4
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

2.5. **Doc Refresh Check (OBRIGATÓRIO):**

    > [!CAUTION]
    > **Antes de marcar como Concluído**, verificar se a melhoria alterou
    > comportamento documentado em `docs/flows/` ou `docs/design/`.

    a. Listar todos os arquivos modificados durante a execução
    b. Buscar referências em documentação existente:
       ```bash
       grep -rl "{nome_do_arquivo}" docs/flows/ docs/design/ 2>/dev/null
       ```
    c. Se **referências encontradas** → Verificar e atualizar docs para refletir o estado real
    d. Se doc existe no Flyee ("Documentação Técnica") → Atualizar página correspondente
    e. Registrar no `ENHANCE-PROGRESS.md`: `📄 Docs atualizados: {lista ou "Nenhum afetado"}`

3.  **PERGUNTAR Tempo Gasto (OBRIGATÓRIO):**
    ```
    ⏱️ Quanto tempo foi gasto nesta task?
    (Ex: "2h30m", "4h", "30m")
    ```

4.  **Atualizar Tracker (Status → Concluído + Tempo Gasto + Progresso):**
    > **Seguir Flyee API** → Seção "✅ Atualizar Status → Concluído"

    ```json
    // Tool: Flyee API: update_task()
    {
      "page_id": "{page_id}",
      "properties": {
        "Status": { "status": { "name": "Concluído" } },
        "Tempo Gasto": { "rich_text": [{ "text": { "content": "{tempo}" } }] },
        "% Progresso": { "number": 100 }
      }
    }
    ```

5.  **Adicionar nota de conclusão no corpo (INLINE — NÃO PULAR):**

    ```json
    // Tool: Flyee API: update_task() (output)
    {
      "block_id": "{page_id}",
      "children": [
        { "type": "divider", "divider": {} },
        { "type": "callout", "callout": { "icon": { "type": "emoji", "emoji": "✅" }, "rich_text": [{ "type": "text", "text": { "content": "Concluído em {data}" } }] } },
        { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📋 {resumo da implementação}" } }] } },
        { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "🧪 Testes: {resultado}" } }] } },
        { "type": "bulleted_list_item", "bulleted_list_item": { "rich_text": [{ "type": "text", "text": { "content": "📁 Arquivos: {lista de arquivos modificados}" } }] } }
      ]
    }
    ```

6.  **Comentário Final com Resumo:**
    ```
    Use: Flyee API: update_task() (output)
    parent: { "page_id": "{page_id}" }
    rich_text: [{ "text": { "content": "✅ **Feito!**\n⏱️ Tempo: {Tempo}\n🧪 Cobertura: {X}%\n\n📋 **Alterações:**\n- {lista de mudanças}\n\n📁 **Arquivos:**\n- {lista de arquivos}\n\n📚 **Histórico aplicado:**\n- {lições de tasks anteriores usadas}" } }]
    ```
6.  **Atualizar Checkpoint Local:**
    ```markdown
    # Em docs/ENHANCE-PROGRESS.md
    Status: ✅ Concluído
    Cobertura Final: {X}%
    Tasks Relacionadas: [#123, #98]
    ```

#### 🔔 FLYEE BRIDGE EMIT (Condicional)

> Se `flyee.json` existe E `enabled: true`:

```bash
python .agent/flyee-bridge/bridge.py emit "dev.task_completed" '{"workflow": "enhance", "task_name": "{nome}", "time_spent": "{tempo}", "files_changed": ["{lista}"], "coverage": "{X}%"}'
```

> Se bridge não configurado → Pular silenciosamente.

---

## 📌 Matriz de Propriedades por Fase

> [!IMPORTANT]
> **Todas as propriedades são obrigatórias e devem ser preenchidas/atualizadas nas fases indicadas.**

| Propriedade | Fase 2 (Criação) | Fase 3 (Execução) | Fase 4 (Conclusão) |
|-------------|------------------|-------------------|--------------------|
| `Status` | ✅ "Em andamento" | - | ✅ "Concluído" |
| `Categoria` | ✅ Definido | - | - |
| `Prioridade` | ✅ Definido | - | - |
| `Estimativa` | ✅ **OBRIGATÓRIO** | - | - |
| `Tempo Gasto` | - | - | ✅ **OBRIGATÓRIO** |
| `% Progresso` | - | Atualizar parcial | ✅ 100 |

---

## 🚨 REGRAS CRÍTICAS DE ENFORCEMENT

> [!CAUTION]
> **REGRA BLOQUEANTE:** Este workflow **NÃO PODE TERMINAR** sem:
> 1. Registrar task no tracker (Flyee: `API-post-page` | Local: `docs/TASKS.md`)
> 2. Atualizar status para "Concluído" (Flyee: `API-patch-page` | Local: `[x]`)
> 3. Adicionar resumo de fechamento (Flyee: `API-create-a-comment` | Local: no `ENHANCE-PROGRESS.md`)

### ⚠️ Checklist de Finalização (OBRIGATÓRIO)

**Antes de ENCERRAR a conversa ou resposta, o agente DEVE verificar:**

- [ ] **Fase 2 executada?** Task criada no Flyee com ID registrado?
- [ ] **Fase 3 concluída?** Todas as alterações implementadas?
- [ ] **Doc Refresh executado?** Docs impactados verificados e atualizados (local + Flyee)?
- [ ] **Fase 4 executada?** 
  - [ ] `API-patch-page` chamado com Status = "Concluído" e `% Progresso: 100`?
  - [ ] `API-patch-block-children` chamado com nota de conclusão no corpo?
  - [ ] `API-create-a-comment` chamado com resumo?

### 🔄 Se a Execução for Longa/Interrompida

Se o agente precisar pausar ou a conversa for longa:

1. **ANTES de parar:** Atualizar Tracker com progresso parcial
2. **Informar usuário:** "Task {ID} em progresso - X de Y itens concluídos"
3. **Ao retomar:** Verificar status atual no Flyee antes de continuar

### ❌ O Que NUNCA Fazer

1. ❌ **Encerrar conversa** sem atualizar tracker
2. ❌ **Marcar como Concluído** sem verificar se TODOS os itens foram resolvidos
3. ❌ **Esquecer de registrar** a task inicialmente (Fase 2)
4. ❌ **Pular o resumo final** com descrição das alterações

### ✅ Verificação de Conclusão Correta

Quando o usuário perguntar "verificar task" ou "checar Flyee":

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