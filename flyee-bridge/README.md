# Flyee Bridge — .agent → Flyee Platform Integration

O `flyee-bridge` conecta o runtime `.agent` à plataforma Flyee, enviando eventos estruturados de desenvolvimento e registrando documentação automaticamente.

## Setup Completo (Interativo)

```bash
python .agent/flyee-bridge/bridge.py --setup
```

O setup guia você em **4 passos**:

### Passo 1: Autenticação
- **API URL** do backend Flyee (default: `https://flyee-api.flyeelab.com`)
- **API Key** (obtida em Settings → API Keys na plataforma)

### Passo 2: Seleção ou Criação de Projeto
- Lista projetos existentes na plataforma
- Permite selecionar um existente **ou criar um novo**
- Ao criar novo, sugere nome baseado no diretório ou `PROJECT-PROGRESS.md`

### Passo 3: Registro de Documentação
- Escaneia `docs/` buscando documentos conhecidos (PRD, TDD, Breakdown, etc.)
- Registra automaticamente na plataforma via API
- Exibe relatório com status de cada documento

### Passo 4: Salvar Configuração
- Salva em `flyee.json` — **não será solicitado novamente**

## Comandos

```bash
# Setup completo (autentica, cria/seleciona projeto, registra docs)
python .agent/flyee-bridge/bridge.py --setup

# Testar conectividade
python .agent/flyee-bridge/bridge.py --test

# Listar projetos na plataforma
python .agent/flyee-bridge/bridge.py --list-projects

# Registrar docs existentes (após setup)
python .agent/flyee-bridge/bridge.py --register-docs

# Emitir evento manualmente
python .agent/flyee-bridge/bridge.py emit "dev.task_completed" '{"task": "T1.1"}'
```

## Eventos Suportados

| Evento | Quando é Emitido |
|--------|-----------------|
| `dev.workflow_started` | Workflow `/execute`, `/new-task` ou `/task-update start` iniciado |
| `dev.workflow_completed` | `/discovery` cria tasks no Notion |
| `dev.task_completed` | `/task-complete`, `/execute` ou `/new-task` conclui task |
| `dev.test_run` | `/test` executa testes (com resultado) |
| `dev.deploy_completed` | `/deploy` concluído com sucesso |
| `dev.deploy_failed` | `/deploy` falhou |
| `dev.decision_detected` | `/new-project` aprova PRD ou TDD |
| `dev.file_changed` | Reservado para futuro (git hooks) |

## Comportamento

- **Condicional:** Eventos só são enviados se `enabled: true` no config
- **Opt-out:** Se o usuário recusar na configuração, `opted_out: true` e nunca mais pergunta
- **Retry:** 3 tentativas com backoff exponencial (1s, 2s, 4s)
- **Fallback:** Se API indisponível, grava em `events.jsonl` local
- **Sem dependências:** Usa apenas stdlib Python (urllib, json, glob, re)

## Integração com Workflows

Os workflows do `.agent` têm instruções `🔔 FLYEE BRIDGE EMIT` que chamam o bridge automaticamente.

Adicionalmente, os workflows `/new-project` e `--resume` possuem o **FLYEE BRIDGE CHECK** que:
1. Verifica se o bridge está configurado
2. Se não: pergunta ao usuário se deseja configurar
3. Executa setup completo (projeto + docs) se confirmado

## Mapeamento de Documentos (scan automático)

| Padrão de Arquivo | Tipo Flyee | Descrição |
|-------------------|-----------|-----------|
| `docs/PRD-*.md` | `prd` | Product Requirements Document |
| `docs/design/TDD-*.md` | `tdd` | Technical Design Document |
| `docs/BREAKDOWN-*.md` | `other` | Task Breakdown |
| `docs/PROJECT-PROGRESS.md` | `other` | Project Progress tracking |

## Arquivo de Configuração

```json
{
  "api_url": "https://flyee-api.flyeelab.com",
  "project_id": "uuid-do-projeto",
  "api_key": "sua-api-key",
  "enabled": true,
  "opted_out": false,
  "fallback_file": ".agent/flyee-bridge/events.jsonl"
}
```
