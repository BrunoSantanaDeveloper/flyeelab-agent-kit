---
description: Add or update features with mandatory Analysis, Splitting, and Tracker sync (Flyee or Local). Supports dynamic database discovery.
skills: checkpointing-patterns, history-check-patterns, context-gathering-patterns, project-tracking-patterns, ui-ux-discovery, local-verification, integration-completeness, design-system-enforcement

---

# /new-task - Structured Improvement Workflow

$ARGUMENTS

**Flags:**

| Flag | Descrição |
|------|-----------|
| `--tdd` | Modo **TDD obrigatório** (testes antes do código) |
| `--resume` | **Retomar** de onde parou |
| `--backlog` | **Apenas registro**: Cria a task no Flyee e encerra (não inicia implementação) |
| `--skip-history` | Pular consulta de histórico (não recomendado) |

---

## 🛑🛑🛑 MANDATORY EXECUTION PROTOCOL (READ FIRST) 🛑🛑🛑

> [!CAUTION]
> **HALT.** Você DEVE completar TODAS as etapas abaixo **ANTES** de escrever qualquer linha de código.
> Pular qualquer etapa = **VIOLAÇÃO GRAVE**. O workflow inteiro será considerado inválido.
> **NENHUMA EXCEÇÃO.** Nem urgência, nem simplicidade, nem pedido do usuário justifica pular.

### 📋 CHECKLIST OBRIGATÓRIO (Executar em ordem, mostrar evidência)

**O agente DEVE executar cada comando e mostrar o output ao usuário:**

```
🛑 /new-task GOVERNANCE GATE

[ ] 1. FLYEE DETECTION: Executei `cat flyee.json` e verifiquei se existe?
       → Se não existe: INFORMAR usuário e perguntar se deseja configurar
       → Se existe mas enabled:false: INFORMAR que tracking está desativado

[ ] 2. FLYEE TASK CRIADA: Executei `bridge.py --create-task` e obtive o ID?
       → ID da task: ___________
       → Se falhou: RETRY 1x → Se falhou novamente: INFORMAR usuário

[ ] 3. HISTORY CHECK: Consultei tasks anteriores no Flyee relacionadas à demanda?
       → Tasks encontradas: ___ (ou "Nenhuma")
       → Lições aplicáveis: ___ (ou "Nenhuma")

[ ] 4. CONTEXT CHECK: Verifiquei docs/INDEX.md e docs/flows/ para contexto?
       → Documentação encontrada: ___ (ou "Nenhuma → perguntar ao usuário")

❌ QUALQUER ITEM DESMARCADO → NÃO INICIAR IMPLEMENTAÇÃO
✅ TODOS MARCADOS → Prosseguir para código
```

> [!CAUTION]
> **ANTI-SKIP RULES:**
> - ❌ "É uma task simples" → NÃO é motivo para pular. Tasks simples TAMBÉM devem ser rastreadas.
> - ❌ "O usuário pediu para ir direto" → NÃO é motivo. Informar o usuário que o gate é obrigatório.
> - ❌ "Já sei o que fazer" → NÃO é motivo. O registro no Flyee serve para rastreabilidade, não para planejamento.
> - ❌ "Vou registrar depois" → PROIBIDO. A task DEVE ser criada ANTES da implementação.

### ⚡ ORDEM DE EXECUÇÃO OBRIGATÓRIA

```
1. cat flyee.json                              → Detectar Flyee
2. bridge.py --create-task                     → Criar task no Flyee
3. Flyee API: search tasks relacionadas        → History check
4. Verificar docs/INDEX.md + docs/flows/       → Context check
5. ════════════════════════════════════════════
   ↓↓↓ SOMENTE APÓS 1-4 COMPLETOS ↓↓↓
6. Implementar código
7. /task-complete                               → Fechar task
```

> [!CAUTION]
> **SE O AGENTE CHEGAR AO PASSO 6 SEM TER EXECUTADO 1-4:**
> O agente DEVE parar IMEDIATAMENTE, voltar, e executar os passos faltantes.
> Código escrito sem task rastreada = trabalho perdido.

---

## 🎯 PROPÓSITO

Workflow para melhorias e correções que exige **Análise Prévia** e **Registro no Tracker** (Flyee ou Local).
Totalmente dinâmico: adapta-se ao projeto atual buscando o contexto correto.

> [!IMPORTANT]
> **Tracker-aware:** Lê `PROJECT-PROGRESS.md` → `Tracker de Tasks` para determinar
> se cria tasks via Flyee API ou em `docs/TASKS.md`.

---

## 💾 SISTEMA DE CHECKPOINTING

> **Skill:** `project-tracking-patterns`
>
> O workflow mantém estado em dois lugares:
> - Arquivo local: `docs/NEW-TASK-PROGRESS.md`
> - Tracker remoto: Flyee Task
>
> **Retomada:** Ao executar `/new-task --resume`, o agente carrega o arquivo de progresso, busca a task no Flyee e continua da fase pendente.

---

## 🚫 FLUXO: PRE-CHECK → HISTORY → DISCOVER → ANALYSE → TRACK → EXECUTE → VERIFY

> [!CAUTION]
> **REGRA DE OURO:** NUNCA use IDs fixos. Sempre busque o contexto do projeto atual.
> **Cada transição de fase exige que a fase anterior tenha sido COMPLETADA com evidência.**

---

### 🚨 Fase -2: PRE-START CHECK (Gate de Finalização)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Esta é a PRIMEIRA ação ao iniciar o workflow.
> Verificar se há tasks "Em andamento" antes de criar/iniciar nova.

**Ações OBRIGATÓRIAS (executar e mostrar output):**

1. **Detectar Flyee:**
   ```bash
   cat flyee.json 2>/dev/null || echo "⚠️ flyee.json não encontrado"
   ```
   → Se não existe: **PARAR** e perguntar ao usuário se deseja configurar.

2. **Verificar tasks abertas:**
   ```bash
   python3 .agent/flyee-bridge/bridge.py --search-context "status em andamento"
   ```
   → Se houver tasks em andamento: Perguntar se deseja finalizar primeiro.
   → Se usuário quiser finalizar: Executar `/task-complete` antes de prosseguir.

**Gate de Saída Fase -2:**
```
[ ] flyee.json verificado (mostrar output)
[ ] Tasks em andamento verificadas
❌ Se desmarcado → NÃO prosseguir para Fase -1
```

---

### 🕵️ Fase -1: HISTORY CHECK (Aprender com o passado)

> **Skill:** `history-check-patterns`
>
> **Objetivo:** Consultar histórico de tarefas relacionadas à demanda para evitar repetir erros e adotar padrões já definidos.
> **Ação:** Executar a busca de histórico descrita no skill.

**Gate de Saída Fase -1:**
```
[ ] History check executado (mostrar output ou "Nenhum histórico")
[ ] Lições identificadas e anotadas
❌ Se desmarcado → NÃO prosseguir para Fase 0
```

---

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

**Gate de Saída Fase 1:**
```
[ ] Complexidade avaliada
[ ] Estratégia de split definida
[ ] Estimativa definida
❌ Se desmarcado → NÃO prosseguir para Fase 2
```

---

### 📝 Fase 2: TRACKING (Flyee)

> [!CAUTION]
> **BLOQUEADOR ABSOLUTO:** Esta fase DEVE ser concluída ANTES de qualquer implementação.

**Ação:** Usar `bridge.py` para criar a task no Flyee.

```bash
# 1. Criar a task
python3 .agent/flyee-bridge/bridge.py --create-task --name "{nome}" --type implement_feature --description "{detalhes}" --priority normal

# 2. Persistir Plano Arquitetural (OBRIGATÓRIO)
python3 .agent/flyee-bridge/bridge.py --persist-plan "implementation_plan.md" --task-id <id>
```

> [!IMPORTANT]
> **STOP GATE (--backlog):** Se `--backlog` foi utilizado, **ENCERRA AQUI**. Informe o link da task ao usuário.

**Gate de Saída Fase 2:**
```
[ ] Task criada via bridge.py (ID obtido)
[ ] Se --backlog: encerrou aqui
❌ Se task NÃO foi criada → CRIAR AGORA antes de Fase 3
```

---

### 💻 Fase 3: EXECUTION (Code)

> **Skills ativas:** `tdd-workflow`, `design-system-enforcement`, `ui-validation`

> [!CAUTION]
> **🛑 CHECKPOINT:** Verifique que as Fases -2 a 2 foram CONCLUÍDAS. 
> É terminantemente proibido codar sem uma Task ID do Flyee em mãos.

**Ação:** Implementar as mudanças delegando responsabilidades aos skills especialistas:

| Sub-fase | Skill | O que |
|----------|-------|-------|
| 🔴 **3.0 Context Gather** | `context-gathering-patterns` | (Opcional) Re-ler requisitos detalhados listados na Fase 0 |
| **3.1 Lógica/Backend** | `tdd-workflow` | Implementar TDD: RED → GREEN → REFACTOR. Seguir regras Anti-Mock. |
| **3.2 UI Components** | `design-system-enforcement` | Se houver UI, extrair tokens do MASTER.md e garantir Premium Styling e Responsividade. |
| **3.3 UI Check** | `ui-validation` | Se alterou UI, rodar validação automatizada de antipatterns Visuais. |

**Gate de Saída Fase 3:**
```
[ ] Lógica implementada (Testada se --tdd)
[ ] UI aderente ao Design System (se aplicável)
❌ Se pendente → NÃO prosseguir
```

---

### ✅ Fase 4: VERIFICATION & COMPLETION (Workflow Delegation)

> **Workflow:** `/task-complete`
> **Skill:** `project-tracking-patterns`

**Ação Final:**

1.  **Document Refresh:** Busque documentações antigas impactadas e atualize (local e no Flyee).
2.  **Coverage:** Se `--tdd`, garanta mínimo de 80% coverage localmente.
3.  **Completion:** Execute `/task-complete`. ESTA É A ÚNICA FORMA AUTORIZADA DE FECHAR TASKS.

> [!CAUTION]
> 🚫 **ANTI-PATTERN PROIBIDO:** `API-patch-page` solto para fechar a Task sem comentários ou detalhes.
> ✅ **OBRIGATÓRIO:** Workflow `/task-complete` fará os 8 steps de encerramento, incluindo o Log de Execução e o tempo gasto.

**Gate Final:**
```
[ ] `/task-complete` excutado
[ ] Documentação técnica ou guias atualizados
```

### ⚠️ Checklist de Finalização (OBRIGATÓRIO)

**Antes de ENCERRAR a conversa ou resposta, o agente DEVE verificar:**

- [ ] **Fase 2 executada?** Task criada no Flyee com ID registrado?
- [ ] **Fase 3 concluída?** Todas as alterações implementadas?
- [ ] **Doc Refresh executado?** Docs impactados verificados e atualizados (local + Flyee)?
- [ ] **Fase 4 executada?** 
  - [ ] Workflow `/task-complete` invocado para finalizar a task no sistema?

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