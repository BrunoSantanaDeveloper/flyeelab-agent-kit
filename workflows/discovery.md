---
description: Workflow completo de descoberta a produção. Brainstorm → TDD → Design System → Validação → Tarefas no Notion. Fluxo automatizado e contínuo. Suporta busca dinâmica de database.
skills: notion-task-patterns
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

## 🔀 QUANDO USAR `/discovery` vs `/new-project`?

> [!TIP]
> **Escolha o workflow certo:**

| Situação | Use | Por quê? |
|----------|-----|----------|
| Ideia clara, preciso de **documentação formal** (PRD + TDD) | `/new-project` | Fluxo completo com aprovações |
| Ideia clara, quero ir **rápido** sem PRD | `/discovery` ou `/new-project --quick` | Direto para TDD + Notion |
| Tenho **proposta comercial** aprovada | `/discovery --from-demand` | Importa contexto da proposta |
| Tenho **código legado** para documentar | `/discovery --from-project` | Engenharia reversa |
| Tenho **Figma** pronto | `/discovery --from-figma` | Importa Design System |

> [!NOTE]
> `/discovery` é equivalente a `/new-project --quick` com integração nativa ao Notion.
> Se você precisa apenas de TDD + Tasks rapidamente, use `/discovery`.

---

## 🔴 FLUXO AUTOMATIZADO

### Fase 0: INTEGRAÇÃO COM /demand (Se --from-demand)
... (Fases 0 a 4.6 permanecem inalteradas, focando na integração Notion) ...

---

### Fase 0.1: REVERSE ENGINEERING (Se --from-project)

> [!TIP]
> **Para fluxo completo de projeto legado**, use `/legacy-project [path]`.
> Esta fase é executada automaticamente como parte daquele workflow.

**Trigger:** `/discovery --from-project "path/to/project"`

**Agentes Envolvidos:**
- `explorer-agent` - Análise de estrutura e mapeamento
- `backend-specialist` / `frontend-specialist` / `mobile-developer` - Análise técnica conforme stack

**Ações:**

1. **Detectar Stack Tecnológica:**
   | Arquivo | Stack |
   |---------|-------|
   | `package.json` | Node.js/React/Next.js |
   | `requirements.txt` / `pyproject.toml` | Python |
   | `pubspec.yaml` | Flutter |
   | `Gemfile` | Ruby |
   | `go.mod` | Go |
   | `Cargo.toml` | Rust |

2. **Mapear Estrutura de Diretórios:**
   ```
   projeto/
   ├── src/           → Código fonte
   ├── tests/         → Testes existentes
   ├── docs/          → Documentação existente
   ├── config/        → Configurações
   └── ...
   ```

3. **Identificar Entry Points:**
   - Main files (index.js, main.py, App.tsx)
   - Rotas/Controllers
   - Componentes principais

4. **Listar Dependências:**
   - Frameworks utilizados
   - Bibliotecas principais
   - Serviços externos (APIs, DBs)

5. **Gerar Outline do Projeto:**
   ```markdown
   # CODEBASE-{projeto}.md
   
   ## Stack
   - Frontend: {framework}
   - Backend: {framework}
   - Database: {tipo}
   
   ## Estrutura
   {tree simplificado}
   
   ## Componentes Principais
   - {componente 1}: {descrição}
   - {componente 2}: {descrição}
   
   ## Fluxos Identificados
   - [ ] {fluxo 1}
   - [ ] {fluxo 2}
   ```

**Output:**
- `docs/CODEBASE-{projeto}.md` - Visão geral do projeto
- Lista de fluxos para documentar com `/document`

**Gate de Saída:**
```
[ ] Stack identificada
[ ] Estrutura mapeada
[ ] Fluxos principais listados
```

**Próximo Passo:** Para cada fluxo identificado → `/document [fluxo]`

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
       "Título": { title: [{ text: { content: "{Título da Task}" } }] },
       "ID": { rich_text: [{ text: { content: "{N.X}" } }] },
       "Épico": { select: { name: "{Nome do Épico}" } },
       "Status": { status: { name: "{STATUS_MAPPED}" } },
       "Prioridade": { select: { name: "{PRIORITY_MAPPED}" } },
       // ... outras props mapeadas
     }
   ```
   
   > **Geração de ID:** Formato `{Épico}.{Sequência}`, ex: `1.1`, `1.2`, `2.1`
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
