---
description: Workflow completo de descoberta a produção. Brainstorm → TDD → Design System → Validação → Tarefas no Notion. Fluxo automatizado e contínuo. Suporta busca dinâmica de database.
---

# /discovery - Da Ideia à Execução (Automático)

$ARGUMENTS

**Arguments:**

| Flag | Descrição | Exemplo |
|------|-----------|---------|
| `--from-demand` | Importa dados de proposta aprovada no Notion | `--from-demand "Nome da Proposta"` |
| `--from-project` | Analisa projeto existente para gerar TDD | `--from-project "c:\path\to\project"` |
| `--from-figma` | Importa Design System do Figma existente | `--from-figma "https://figma.com/file/..."` |
| `--no-design` | Pula geração de Design System | `--no-design` |
| `--no-notion` | Pula criação de tasks no Notion | `--no-notion` |
| `--no-infra` | Pula definição de infraestrutura | `--no-infra` |
| `--notion-db` | Especifica database do Notion | `--notion-db "Tasks Database"` |

---

## 🎯 PROPÓSITO

Workflow **unificado e automatizado** que transforma uma ideia em tarefas executáveis no Notion.
Totalmente dinâmico e adaptável ao contexto do projeto.

---

## 🔴 FLUXO AUTOMATIZADO

### Fase 0: INTEGRAÇÃO COM /demand (Se --from-demand)
... (Fases 0 a 4.6 permanecem inalteradas, focando na integração Notion) ...

---

### Fase 5: NOTION INTEGRATION (Automático após aprovação)

> [!CAUTION]
> **REGRA BLOQUEANTE:** Você **NÃO PODE** usar IDs de database hardcoded. Deve SEMPRE executar a Fase 5.1 (DISCOVERY & VALIDATION) para encontrar o database correto do projeto atual.

#### Fase 5.1: DISCOVERY & VALIDATION (Pre-flight) 🔴 OBRIGATÓRIO

**Trigger:** Usuário aprova User Stories

**Agente Responsável:** `orchestrator` (Validador de integração)
**Skills:** `api-patterns`, `brainstorming` (feedback de erro)

**Ações:**

1. **Discover Database:**
   *   Se flag `--notion-db` informada: Buscar por name exato.
   *   Se não: Buscar por "Tarefas", "Tasks", "Daily", "Sprint".
   ```
   API-post-search:
   - query: "{query}"
   - filter: { "value": "database" }
   ```

2.  **Validate Schema & Map:**
    *   Ao encontrar, validar schema e mapear propriedades **dinamicamente**:
    *   `Status` (Status) -> Guardar options (ex: To Do / Doing / Done)
    *   `Prioridade` (Select) -> Guardar options real (ex: P0/P1 ou Alta/Baixa)
    *   `Estimativa` (Select) -> Guardar options real (ex: XS/S/M ou 1/2/3)
    
3.  **Check "Tempo Gasto":**
    *   Verificar se propriedade existe.
    *   Se não: Perguntar se deseja criar (opcional).

4. **Decisão Automática:**
   - **❌ Falha:** Se não encontrar database ou schema incompatível (sem Status/Title) -> **NOTIFICAR USUÁRIO**.
   - **✅ Sucesso:** Guardar `{DATABASE_ID}` e `{SCHEMA_MAP}` para Fase 5.2.

**Mensagem de Sucesso (Obrigatória no plano):**
```
✅ NOTION DISCOVERY PASSED

Database: {nome_encontrado}
ID: {DATABASE_ID}

Mapeamento:
- Status: Usando "Backlog"
- Prioridade: Usando "High", "Medium", "Low"
```

---

#### Fase 5.2: TASK CREATION (Execution)

**Trigger:** Discovery = PASS

**Ações (Para CADA User Story):**
1. Ler documento `USER-STORIES-{nome}.md`
2. **Passo 1 - Criar página dinamicamente:**
   ```
   API-post-page:
   - parent: { database_id: "{DATABASE_ID_ENCONTRADO}" }
   - properties: {
       "Título": { title: ... },
       "Status": { status: { name: "{STATUS_MAPPED}" } },
       "Prioridade": { select: { name: "{PRIORITY_MAPPED}" } },
       // ... outras props mapeadas
     }
   ```
3. **Passo 2 - Adicionar corpo (OBRIGATÓRIO):**
   ```
   API-patch-block-children:
   - block_id: { id retornado do passo 1 }
   - children: [ heading_2, paragraph, formatted_text... ]
   ```

---

## 🔧 EXAMPLE REQUESTS

**Exemplo Dinâmico (Busca e Criação):**
```json
// Busca
POST API-post-search { "query": "Tarefas", "filter": { "value": "database" } }
// Retorna ID: "b7e8..."

// Criação
POST API-post-page
{
  "parent": { "database_id": "b7e8..." },
  "properties": { 
     // Propriedades adaptadas ao schema retornado
  }
}
```

> [!TIP]
> **Nunca assuma IDs.** Se o `/enhance` ou `/log` já rodaram e encontraram um ID, você pode (e deve) reutilizá-lo para consistência.
