---
description: Consultar status de uma task no Notion. Verifica progresso, subitens e se está concluída.
---

# /check-task - Verificar Status de Task

$ARGUMENTS

**Arguments:**

| Argumento | Descrição | Exemplo |
|-----------|-----------|---------|
| `<busca>` | Título, ID parcial ou termo de busca | `/check-task "autenticação"` |
| `--subitems` | Mostrar checklist de subitens | `/check-task 1.1 --subitems` |
| `--history` | Mostrar histórico de comentários | `/check-task "login" --history` |

---

## 🎯 PROPÓSITO

Consultar o status de uma task específica no Notion **sem iniciar execução**.

Útil para:
- Verificar se uma task foi concluída
- Checar progresso e subitens pendentes
- Validar antes de dar continuidade

---

## 📌 COMO IDENTIFICAR UMA TASK

### Convenção de Identificação

As tasks usam o **título** como identificador, geralmente com padrão:

```
{Épico}.{Sequência} - {Descrição}
```

**Exemplos:**
- `1.1 - Implementar autenticação OAuth`
- `2.3 - Criar componente de listagem`
- `Adicionar filtro de busca` (sem número)

### Formas de Buscar

| Método | Exemplo | O que busca |
|--------|---------|-------------|
| **ID parcial** | `/check-task 1.1` | Título contendo "1.1" |
| **Nome parcial** | `/check-task "autenticação"` | Título contendo "autenticação" |
| **Nome completo** | `/check-task "1.1 - Implementar..."` | Match exato |

> [!TIP]
> **Onde encontrar o ID?**
> - No Notion: é o início do título da task
> - No TDD: seção de breakdown lista tasks com IDs
> - No relatório do `/discovery`: mostra IDs criados

---

## 🔴 FLUXO

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    BUSCAR    │───▶│   ANALISAR   │───▶│   REPORTAR   │
│   (Notion)   │    │   (Status)   │    │  (Resultado) │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

### Fase 1: BUSCAR TASK

**Trigger:**
```
/check-task <busca>
```

**Ações:**
1. Buscar no Notion:
   ```
   Use: mcp_notion-mcp-server_API-post-search
   query: "{busca}"
   filter: { "property": "object", "value": "page" }
   ```

2. **Se encontrar múltiplas:**
   ```
   🔍 MÚLTIPLAS TASKS ENCONTRADAS
   
   | # | Título | Status | % |
   |---|--------|--------|---|
   | 1 | 1.1 - Autenticação OAuth | Em Progresso | 50% |
   | 2 | 1.2 - Autenticação JWT | Concluído | 100% |
   
   Qual você quer verificar? (digite o número)
   ```

3. **Se não encontrar:**
   ```
   ❌ TASK NÃO ENCONTRADA
   
   Nenhuma task com "{busca}" foi encontrada.
   
   💡 Dica: Verifique se o termo está correto ou use parte do título.
   ```

---

### Fase 2: ANALISAR TASK

**Trigger:** Task encontrada (única ou selecionada)

**Ações:**
1. Recuperar propriedades da task:
   ```
   Use: mcp_notion-mcp-server_API-retrieve-a-page
   page_id: {task_id}
   ```

2. Extrair dados:
   - Título
   - Status
   - Última edição
   - Categoria
   - Prioridade
   - Última edição

3. Se `--subitems`: Recuperar corpo da página:
   ```
   Use: mcp_notion-mcp-server_API-get-block-children
   block_id: {task_id}
   ```
   - Contar itens marcados `[x]` vs `[ ]`

4. Se `--history`: Recuperar comentários:
   ```
   Use: mcp_notion-mcp-server_API-retrieve-a-comment
   block_id: {task_id}
   ```

---

### Fase 3: REPORTAR STATUS

**Ações:**

1. **Task CONCLUÍDA (100%):**
   ```
   ✅ TASK CONCLUÍDA
   
   📋 Título: 1.1 - Implementar autenticação OAuth
   📊 Status: Concluído
   📈 Progresso: 100%
   📅 Concluída em: 2026-01-15
   
   Esta task está totalmente finalizada.
   ```

2. **Task EM PROGRESSO (1-99%):**
   ```
   🟡 TASK EM PROGRESSO
   
   📋 Título: 2.3 - Criar componente de listagem
   📊 Status: Em Progresso
   📈 Progresso: 65%
   🎯 Categoria: Feature
   
   📝 Subitens:
   - [x] Criar estrutura base
   - [x] Implementar filtros
   - [ ] Adicionar paginação
   - [ ] Testes unitários
   
   Pendente: 2 de 4 itens
   ```

3. **Task NÃO INICIADA (0%):**
   ```
   ⏳ TASK NÃO INICIADA
   
   📋 Título: 3.1 - Integrar pagamento
   📊 Status: A Fazer
   📈 Progresso: 0%
   🎯 Prioridade: P0
   
   Use `/execute 3.1` para iniciar esta task.
   ```

---

## 📋 EXEMPLOS DE USO

```bash
# Verificar task por ID parcial
/check-task 1.1

# Buscar por nome
/check-task "autenticação"

# Ver detalhes com subitens
/check-task 2.3 --subitems

# Ver histórico de comentários
/check-task "login" --history

# Combinar flags
/check-task 1.1 --subitems --history
```

---

## 🔗 INTEGRAÇÃO COM OUTROS WORKFLOWS

| Após `/check-task` | Comando Sugerido | Quando usar |
|-------------------|------------------|-------------|
| Task não iniciada | `/execute {id}` | Iniciar execução |
| Task em progresso | `/task-update {id} progress "msg"` | Atualizar progresso |
| Task com bug | `/debug` | Investigar problema |
| Task incompleta | `/enhance --resume` | Continuar trabalho |

---

## 📊 Propriedades Lidas

| Propriedade | Obrigatória | Descrição |
|-------------|-------------|-----------|
| Título | ✅ | Identificação da task |
| Status | ✅ | Não iniciado / Em andamento / Concluído |
| Última edição | ✅ | Data/hora da última modificação (automático) |
| Categoria | ❌ | Feature, Melhoria, Bug, etc. |
| Prioridade | ❌ | P0, P1, P2, P3 |
| last_edited_time | ❌ | Data da última edição |

---

## 🔴 REGRAS

1. **Apenas consulta** - Este workflow NÃO modifica a task
2. **Busca flexível** - Aceita ID (1.1), nome parcial ou completo
3. **Múltiplos resultados** - Pergunta ao usuário qual verificar
4. **Sem execução** - Para executar, use `/execute`
