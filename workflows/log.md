---
description: Registrar trabalho já concluído no Flyee. Suporta busca dinâmica de database.
skills: project-tracking-patterns
---

# /log - Registrar Trabalho Retroativo

$ARGUMENTS

---

## 🎯 PROPÓSITO

Registrar no Tracker trabalhos já concluídos (**Retroativo**).
Adapta-se a qualquer projeto buscando o database automaticamente.

---

## 📋 SINTAXE

```bash
/log <tipo> "<descrição>" [opções]
```

---

## 🔴 FLUXO: DISCOVER → ANALYSE → TRACK

> [!NOTE]
> Não use IDs fixos. O agente deve descobrir o ambiente.

---

### 🔍 Fase 0: DISCOVERY (Setup)

**Ação:** Encontrar onde registrar.

**Agente Envolvido:** `explorer-agent`

1.  **Buscar Database:**
    *   Procure por "Tarefas", "Tasks", "Daily" ou similar.
    ```
    Use: Flyee API: list_tasks()
    query: "Tarefas"
    filter: { "value": "database" }
    ```

2.  **Validar "Tempo Gasto":**
    *   Analise o schema do banco encontrado.
    *   Se `Tempo Gasto` não existir:
        > 🛑 **PARE E PERGUNTE:** "Propriedade 'Tempo Gasto' não encontrada no banco '{Nome}'. Deseja criar?"
        *   Sim -> Crie.
        *   Não -> Prossiga sem ela.

---

### ✅ Fase 1: ANALYSE & EXTRACT

**Objetivo:** Coletar dados do contexto (Chat/Arquivos).

**Agentes Envolvidos:**
- `project-planner` - Categorização e estimativa
- `backend-specialist` / `frontend-specialist` / `mobile-developer` - Conforme domínio do trabalho

1.  **Extrair:** Tipo (`fix`, `feat`), Descrição e **Tempo**.
2.  **Perguntar:** Se o tempo não foi informado, pergunte.

---

### ✅ Fase 2: TRACK (Flyee)

**Ação:** Criar Task já concluída.

**Agente Envolvido:** `project-planner`

> [!IMPORTANT]
> **SKILL OBRIGATÓRIA:** Seguir Flyee API para criação de tasks.
> Ver seção "➕ CRIAR TASK (2 ETAPAS OBRIGATÓRIAS)" - usar template "Log".

> [!CAUTION]
> **2 ETAPAS OBRIGATÓRIAS:**
> 1. `API-post-page` → Criar task com Status "Concluído"
> 2. `API-patch-block-children` → Adicionar corpo (template Log)

**Resultado:**
```
✅ LOG REGISTRADO (Database: {Nome Encontrado})
📄 Body: ✅ Adicionado
🔗 Link: [Flyee]
```

---

## ⚠️ REGRAS

1.  **Busca Dinâmica:** Se a busca retornar múltiplos bancos, LISTE e PEÇA para o usuário escolher. Não adivinhe.
2.  **Consistência:** Se você já encontrou o ID no passo anterior (`/enhance` ou outra chamada), pode reutilizá-lo para evitar buscas repetidas na mesma sessão.
