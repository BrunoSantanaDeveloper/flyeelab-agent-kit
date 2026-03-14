# Flyee Bridge — .agent → Flyee Platform Integration

O `flyee-bridge` conecta o runtime `.agent` à plataforma Flyee, enviando eventos estruturados de desenvolvimento.

## Setup

```bash
python .agent/flyee-bridge/bridge.py --setup
```

Você será perguntado:
1. **Se deseja integrar** com a plataforma Flyee (pode recusar)
2. **API URL** do backend Flyee
3. **Project ID** (UUID do projeto)
4. **API Key** (obtida em Settings → API Keys na plataforma)

A configuração é salva em `.agent/flyee-bridge/config.json` e **não será solicitada novamente**.

## Uso

```bash
# Testar conectividade
python .agent/flyee-bridge/bridge.py --test

# Emitir evento manualmente
python .agent/flyee-bridge/bridge.py emit "dev.task_completed" '{"task": "T1.1"}'

# Reconfigurar
python .agent/flyee-bridge/bridge.py --setup
```

## Eventos Suportados

| Evento | Quando é Emitido |
|--------|-----------------|
| `dev.workflow_started` | Workflow `/execute`, `/enhance` ou `/task-update start` iniciado |
| `dev.workflow_completed` | `/discovery` cria tasks no Notion |
| `dev.task_completed` | `/task-complete`, `/execute` ou `/enhance` conclui task |
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
- **Sem dependências:** Usa apenas stdlib Python (urllib)

## Integração com Workflows

Os workflows do `.agent` têm instruções `🔔 FLYEE BRIDGE EMIT` que chamam o bridge automaticamente.
O bridge verifica silenciosamente se está configurado — se não, **pula sem erro**.

## Arquivo de Configuração

```json
{
  "api_url": "http://localhost:8001",
  "project_id": "uuid-do-projeto",
  "api_key": "sua-api-key",
  "enabled": true,
  "opted_out": false,
  "fallback_file": ".agent/flyee-bridge/events.jsonl"
}
```
