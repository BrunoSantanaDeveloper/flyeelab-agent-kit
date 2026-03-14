---
description: Test generation and test running command. Creates and executes tests for code.
---

# /test - Test Generation and Execution

$ARGUMENTS

---

## Purpose

This command generates tests, runs existing tests, or checks test coverage.

**Agentes Envolvidos:**
- `test-engineer` - Geração e execução de testes
- `backend-specialist` / `frontend-specialist` / `mobile-developer` - Para testes específicos de domínio
- `debugger` - Para análise de testes falhando

---

## Sub-commands

```
/test                - Run all tests
/test [file/feature] - Generate tests for specific target
/test coverage       - Show test coverage report
/test watch          - Run tests in watch mode
```

---

## Behavior

### Generate Tests

When asked to test a file or feature:

1. **Analyze the code**
   - Identify functions and methods
   - Find edge cases
   - Detect dependencies to mock

2. **Generate test cases**
   - Happy path tests
   - Error cases
   - Edge cases
   - Integration tests (if needed)

3. **Write tests**
   - Use project's test framework (Jest, Vitest, etc.)
   - Follow existing test patterns
   - Mock external dependencies

---

## Output Format

### For Test Generation

```markdown
## 🧪 Tests: [Target]

### Test Plan
| Test Case | Type | Coverage |
|-----------|------|----------|
| Should create user | Unit | Happy path |
| Should reject invalid email | Unit | Validation |
| Should handle db error | Unit | Error case |

### Generated Tests

`tests/[file].test.ts`

[Code block with tests]

---

Run with: `npm test`
```

### For Test Execution

```
🧪 Running tests...

✅ auth.test.ts (5 passed)
✅ user.test.ts (8 passed)
❌ order.test.ts (2 passed, 1 failed)

Failed:
  ✗ should calculate total with discount
    Expected: 90
    Received: 100

Total: 15 tests (14 passed, 1 failed)
```

### 🔔 FLYEE BRIDGE EMIT (Condicional)

> Se `.agent/flyee-bridge/config.json` existe E `enabled: true`:

```bash
python .agent/flyee-bridge/bridge.py emit "dev.test_run" '{"passed": {N_passed}, "failed": {N_failed}, "skipped": {N_skipped}, "total": {N_total}, "target": "{file_or_feature}"}'
```

> Se bridge não configurado → Pular silenciosamente.

---

## Examples

```
/test src/services/auth.service.ts
/test user registration flow
/test coverage
/test fix failed tests
```

---

## Test Patterns

### Unit Test Structure

```typescript
describe('AuthService', () => {
  describe('login', () => {
    it('should return token for valid credentials', async () => {
      // Arrange
      const credentials = { email: 'test@test.com', password: 'pass123' };
      
      // Act
      const result = await authService.login(credentials);
      
      // Assert
      expect(result.token).toBeDefined();
    });

    it('should throw for invalid password', async () => {
      // Arrange
      const credentials = { email: 'test@test.com', password: 'wrong' };
      
      // Act & Assert
      await expect(authService.login(credentials)).rejects.toThrow('Invalid credentials');
    });
  });
});
```

---

## Key Principles

- **Test behavior not implementation**
- **One assertion per test** (when practical)
- **Descriptive test names**
- **Arrange-Act-Assert pattern**
- **Mock external dependencies**

---

## ⏸️ Tratamento de Testes Skipped

> [!CAUTION]
> **Testes skipped NÃO são sucesso.** Eles representam cobertura incompleta e devem ser tratados.

### Quando há testes skipped, SEMPRE:

1. **Listar todos os testes skipped** com motivo
2. **Analisar cada um** e categorizar a ação necessária
3. **Perguntar ao usuário** qual ação tomar

### Output Format para Skipped Tests

```markdown
✅ [N] testes passaram
⏸️ [M] testes skipped:

| Teste Skipped | Motivo | Ação Sugerida |
|---------------|--------|---------------|
| [nome do teste] | [motivo do skip] | [o que fazer] |

📋 **Ação Necessária:**

❓ Deseja que eu:
1. **Implemente** os [M] testes skipped agora?
2. **Documente** como TODO na task do Notion?
3. **Ignore** (aceitar coverage atual com justificativa)?
```

### Classificação de Skipped Tests

| Tipo de Skip | Ação Recomendada |
|--------------|------------------|
| **Mock faltando** | Implementar mock e habilitar teste |
| **API externa indisponível** | Criar fake/stub e habilitar teste |
| **Edge case não mapeado** | Definir cenário com usuário |
| **Formato de resposta desconhecido** | Investigar API e implementar |
| **Dependência de ambiente** | Criar environment mock |
| **Temporariamente desabilitado** | Definir prazo para reabilitar |

### Regras para Skipped

> [!IMPORTANT]
> 1. **NUNCA ignorar silenciosamente** testes skipped
> 2. **SEMPRE perguntar** ao usuário qual ação tomar
> 3. **Se há mais de 10% de skips**, alertar como problema de cobertura
> 4. **Documentar motivo** do skip no código e na task

---

## 🔗 Notion Integration

> [!IMPORTANT]
> Após executar testes, **SEMPRE** perguntar sobre atualização do Notion.

### Se executado dentro de `/execute`:

A atualização do Notion é automática via Fase 6 do workflow `/execute`.

### Se executado standalone (`/test` direto):

Após testes passarem, perguntar:
```
✅ Testes passaram: 15/15

📋 Atualizar task no Notion?
Se estes testes são parte de uma task existente, informe o ID para atualizar:

> /task-update <id> progress "Implementar testes E2E"
```

### Mapeamento de Progresso

| Resultado | Sugestão |
|-----------|----------|
| Todos passaram (0 skipped) | `/task-update <id> progress "msg"` (+15%) |
| Todos passaram (com skipped) | **Tratar skips primeiro** ou documentar como TODO |
| Alguns falharam | Corrigir primeiro, não atualizar Notion |
| Cobertura atingida | `/task-update <id> done "msg"` (100%) |

---

## ⚠️ REGRAS

1. **Nunca atualizar Notion se testes falharem**
2. **Nunca ignorar testes skipped** - sempre perguntar ação ao usuário
3. **Sempre sugerir /task-update após sucesso** (se há task relacionada)
4. **Documentar testes skipped** como TODOs na task com prazo
5. **Se >10% skipped**, alertar como problema de cobertura
