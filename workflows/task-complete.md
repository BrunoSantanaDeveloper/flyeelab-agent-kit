---
description: Workflow obrigatório para finalizar tasks. Garante sync com tracker (Flyee ou Local), logs de execução e atualização de progresso.
---

# /task-complete

> **OBRIGATÓRIO** ao finalizar qualquer task. Garante compliance com tracking patterns.
> Suporta **dois modos de tracking**: Flyee (API) ou Local (`PROJECT-PROGRESS.md`).
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
> 2. **Se Flyee:** Identificar o `page_id` da task (via `API-post-search` ou `API-query-data-source`)
> 3. **Se Local:** Identificar a linha/checkbox correspondente em `PROJECT-PROGRESS.md` (tabela de tasks)
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

**Ação Flyee:**
- Status: {anterior} → Concluído
- Tempo Gasto: {tempo}

**Tempo aproximado:** {tempo}
```

### Etapa 1.5: Resumo de Execução (OBRIGATÓRIO — NÃO PULAR)

> [!CAUTION]
> **REGRA BLOQUEANTE:** O agente DEVE produzir o Resumo de Execução ANTES de atualizar
> o Flyee. Este resumo é o que garante ao usuário **visibilidade total** sobre o que
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

### Etapa 1.7: QA Test Checklist Gate (BLOQUEANTE)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Task NÃO pode ser marcada como `completed` se `all_passed == false`.
> Esta etapa gera o checklist de testes e roda os testes automáticos.
> Leia `@[skills/qa-test-generation]` para heurísticas completas.

**Processo:**

1. **Gerar checklist** — Analisar arquivos modificados (do Resumo Etapa 1.5) + acceptance criteria:
   - Classificar cada arquivo por tipo (UI/API/Backend/Styling/SDK/Workflow)
   - Aplicar heurísticas da skill `qa-test-generation` → gerar `TestStep[]`
   - Cobrir: happy path, error cases, edge cases, boundary values, empty states
   - Salvar via bridge:
     ```bash
     python3 .agent/flyee-bridge/bridge.py --generate-tests <task_id>
     ```
   - Ou via API se bridge não configurado: `PUT /tasks/{id}` com `meta.test_checklist`

2. **Rodar testes automáticos** (type: `auto`):
   - `tsc --noEmit` → reportar resultado para steps de tipo `unit/sdk`
   - `vitest run` → reportar resultado (se configurado)
   - Playwright → reportar resultado (se configurado)
   - Para cada teste auto executado:
     ```bash
     python3 .agent/flyee-bridge/bridge.py --report-test <task_id> <step_id> passed|failed ["comment"]
     ```

3. **Listar testes manuais pendentes** → solicitar ao dev:
   ```bash
   python3 .agent/flyee-bridge/bridge.py --pending-tests <task_id>
   ```
   - Se há testes manuais pendentes → informar ao dev e **aguardar**
   - Dev pode marcar via UI (TaskDetail → tab "tests") ou CLI

4. **Verificar gate:**
   ```bash
   python3 .agent/flyee-bridge/bridge.py --test-summary <task_id>
   ```
   - Se `all_passed == true` → ✅ prosseguir para Etapa 2
   - Se `all_passed == false` → ❌ **BLOQUEAR**:
     - Listar testes falhados
     - Sugerir: `"Deseja rodar /fix-tests <task_id> para corrigir automaticamente?"`
     - Ou solicitar correção manual ao dev

> [!IMPORTANT]
> Se o dev solicitar skip dos testes (ex: hotfix urgente), o agente DEVE:
> 1. Registrar skip como comentário na task
> 2. Marcar testes pendentes como `skipped` (não `passed`)
> 3. Prosseguir com aviso: `"⚠️ Testes pulados — task marcada com quality debt"`

### Etapa 2: Atualizar Tracker

#### Se Tracker = Flyee:
```json
// Tool: Flyee API: update_task()
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
Editar `PROJECT-PROGRESS.md` — alterar `- [ ]` para `- [x]` na task correspondente na tabela de tasks.

### Etapa 2.1: 🔔 FLYEE BRIDGE EMIT (Condicional)

> Se `flyee.json` existe E `enabled: true`:

```bash
python .agent/flyee-bridge/bridge.py emit "dev.task_completed" '{"task_id": "{task_id}", "task_name": "{nome}", "time_spent": "{tempo}", "files_changed": ["{lista de arquivos}"]}'
```

> Se bridge não configurado ou `opted_out: true` → Pular silenciosamente.

### Etapa 2.5: Adicionar Nota de Conclusão (INLINE — NÃO PULAR)

> [!CAUTION]
> Os campos abaixo DEVEM ser preenchidos com os dados do **Resumo de Execução** (Etapa 1.5).
> NÃO usar placeholders genéricos. Se o Resumo de Execução não foi produzido, PARAR e voltar à Etapa 1.5.

#### Se Tracker = Flyee:
```json
// Tool: Flyee API: update_task() (output)
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
// Tool: Flyee API: update_task() (output)
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
// Tool: Flyee API: update_task() (output)
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

### Etapa 4.5: Doc Sync Gate 📄 (OBRIGATÓRIO)

> [!CAUTION]
> **REGRA:** Antes de fechar a task, o agente DEVE verificar se a documentação precisa de atualização.
> Em caso positivo, atualizar **na mesma sessão** antes de prosseguir.
> Skippable APENAS para tasks de tipo `chore`, `fix` ou `docs` sem impacto em features.

**Decision tree (executar mentalmente):**

```
Esta task entregou uma feature F-level nova (ex: F9, F10, F11)?
  └── SIM → Atualizar PRD Sec 6.1: adicionar linha na tabela de Features com status ✅
       └── É a primeira feature do sprint? → Atualizar PRD Sec 9 (Timeline): marcar sprint como Done

Esta task completou um sprint inteiro?
  └── SIM → Atualizar SDD Sec 13 (Implementation Order): marcar sprint como ✅ Done

Esta task adicionou/modificou um endpoint de API?
  └── SIM → Atualizar SDD Sec 3.2 (SDK Layer): tabela de módulos SDK

Esta task criou/modificou um documento em docs/?
  └── SIM → Atualizar docs/INDEX.md (via skill document-registry)

Nenhuma das anteriores?
  └── NÃO → Pular esta etapa ✓
```

**Verificação rápida (rodar para confirmar):**

```bash
python3 .agent/scripts/doc-sync-check.py
```

> O script mostra uma tabela de divergências entre features implementadas e documentação.
> Se output for `✅ Docs sincronizados` → prosseguir.
> Se houver divergências → corrigi-las antes de marcar a task como concluída.

**Docs afetados por tipo de mudança:**

| Tipo de mudança | Doc a atualizar | Seção |
|----------------|-----------------|-------|
| Nova feature F-level | `docs/PRD-flyee.md` | Sec 6.1 (Requirements) + Sec 9 (Timeline) |
| Sprint concluído | `docs/design/SDD-flyee.md` | Sec 13 (Implementation Order) |
| Novo endpoint SDK | `docs/design/SDD-flyee.md` | Sec 3.2 (SDK Layer) |
| Novo task status | `docs/design/SDD-flyee.md` | Sec 3.7 (Polling) + ADR-004 |
| Novo arquivo em docs/ | `docs/INDEX.md` | Tabela de documentos |

---

### Etapa 4.7: Atualizar agent_context do BREAKDOWN + RETRO 🧠

> [!IMPORTANT]
> **PROPÓSITO:** Manter o `agent_context` do BREAKDOWN como cache vivo do projeto.
> Um frontmatter desatualizado força o próximo agente a ler o documento inteiro.
> Esta etapa garante continuidade de contexto com custo mínimo de tokens.

**Decision tree:**

```
Esta task concluiu uma sprint inteira (T{N}.last)?
  └── SIM → Atualizar agent_context do BREAKDOWN:
       • Mudar Sprint {N} de 🔲 Pendente → ✅ nas seções ESTADO ATUAL + SPRINTS
       • Atualizar "X concluídas / Y pendentes" no ESTADO ATUAL
       • Verificar se algum padrão novo foi estabelecido → adicionar em PADRÕES ESTABELECIDOS

Esta task resolveu um bug ou decisão arquitetural?
  └── SIM → Registrar em docs/RETRO-{projeto}-v{N}.md:
       • Se arquivo não existe → criar com template mínimo (ver abaixo)
       • Adicionar entrada na seção ## Bugs / ## Decisões

Nenhuma das anteriores?
  └── NÃO → Pular esta etapa ✓
```

**Template mínimo para RETRO (se não existir):**

```markdown
---
doc_type: retro
doc_id: RETRO-{projeto}-v1
version: "1.0"
date: "{data}"
project: {projeto}
---

# Retrospectiva — {Projeto Nome}

## Bugs Resolvidos
<!-- {data}: {descrição do bug} → {como foi resolvido} -->

## Decisões Tomadas
<!-- {data}: {decisão} → {motivo} -->

## Padrões Estabelecidos
<!-- {data}: {padrão} -->

## O que NÃO fazer
<!-- {data}: {anti-pattern descoberto} -->
```

> [!TIP]
> O RETRO é lido via `grep -n "<keyword>" docs/RETRO-*.md` — entradas compactas
> (1-2 linhas) são preferíveis para não aumentar custo de busca.

**🔔 FLYEE BRIDGE EMIT** (se bridge `enabled: true`, skip silencioso se não):

```bash
# Se sprint concluída nesta task:
python3 .agent/flyee-bridge/bridge.py emit dev.workflow_completed \
  --payload '{"sprint": N, "name": "Sprint N — Nome", "tasks_done": X, "tasks_total": Y}'

# Reportar progresso da sprint para Project Progress do cliente:
python3 .agent/flyee-bridge/bridge.py --sprint-progress \
  --sprint N --name "Sprint N — Nome" --done X --total Y

# Se RETRO atualizado com bug/decisão/padrão, registrar como Decision:
python3 .agent/flyee-bridge/bridge.py --create-decision \
  --decision "<resumo da entrada do RETRO>" \
  --category "<architecture|refactoring|security|tech_debt>" \
  --reason "<contexto ou causa raiz>" \
  --impact "<escopo: arquivos/módulos afetados>"

# Persistir RETRO como Document no Flyee (visível para o cliente):
python3 .agent/flyee-bridge/bridge.py --persist-retro docs/RETRO-{projeto}-v1.md
```

> [!NOTE]
> Estes emits são condicionais: `flyee.json` deve existir com `enabled: true`.
> Se bridge não configurado ou `opted_out: true`: skip sem erro.
> Segue padrão dos 14 trigger points definidos em T8.4.
> `--sprint-progress` cria/atualiza Document tipo `sprint_report` (visível no frontend).
> `--persist-retro` cria/atualiza Document tipo `retro` com dedup SHA256.




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
- [ ] **Resumo de Execução produzido** (Etapa 1.5)
- [ ] **QA Test Gate passed** (Etapa 1.7)
- [ ] **Tracker atualizado** (Flyee ou Local)
- [ ] **Nota de conclusão e comentário** (Flyee) ou checkbox `[x]` (Local)
- [ ] **Doc Sync Gate** (Etapa 4.5 — `doc-sync-check.py` executado)
- [ ] **agent_context + RETRO atualizados** (Etapa 4.7 — se sprint concluída ou bug resolvido)
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
| Flyee | ✅ Sincronizado |

Prosseguindo para próxima task...
```

---

## Gatilhos Automáticos

Este workflow DEVE ser invocado quando o agente:

- Disser "task completa" ou "task concluída"
- Marcar um item como `[x]` no task.md
- Antes de iniciar uma nova task
- Ao finalizar um épico
- **ANTES de chamar `notify_user` para reportar conclusão de trabalho vinculado a uma task Flyee**

> 🔴 **REGRA:** O agente NÃO pode prosseguir para próxima task sem executar este workflow.

---

## 🛑 REGRA UNIVERSAL DE ENFORCEMENT (Anti-Bypass)

> [!CAUTION]
> **REGRA BLOQUEANTE ABSOLUTA — APLICA-SE A QUALQUER CONTEXTO:**
>
> Se o agente completou trabalho que corresponde a uma task rastreada
> (no Flyee ou em `docs/TASKS.md`), ele **DEVE** executar `/task-complete`
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
