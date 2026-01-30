---
description: Document existing flows and processes for testing and future implementations
---

# /document

> Documentar fluxos e processos existentes para servir como referência em testes e novas implementações.

## When to Use

- Documentar um processo/fluxo existente no projeto
- Criar base para criação de testes automatizados
- Orientar futuras implementações relacionadas
- Onboarding de novos desenvolvedores

## Prerequisites

- [ ] Projeto existente com código funcionando
- [ ] Conhecimento do fluxo a ser documentado (ou acesso ao código)

---

## 🚫 FLUXO: DISCOVER → ANALYZE → GENERATE → CROSS-REFERENCE

---

### 📚 Fase 0: DISCOVERY (Contexto)

**Objetivo:** Identificar documentações existentes e estrutura do projeto.

**Agente Envolvido:** `explorer-agent`

1. **Verificar Index:**
   - Checar `docs/INDEX.md` para documentações existentes
   - Identificar documentos relacionados ao fluxo

2. **Analisar Codebase:**
   - Localizar arquivos envolvidos no fluxo
   - Mapear dependências e integrações

---

### 🔍 Fase 1: ANÁLISE TÉCNICA

**Objetivo:** Entender profundamente o fluxo.

**Agentes Envolvidos:**
- `backend-specialist` - Para fluxos de API/serviços
- `frontend-specialist` - Para fluxos de UI/componentes
- `mobile-developer` - Para fluxos mobile (React Native/Flutter)
- `debugger` - Para entender comportamento e edge cases

1. **Mapear Componentes:**
   | Tipo | O que buscar |
   |------|--------------|
   | API/Routes | Endpoints envolvidos |
   | Services | Lógica de negócio |
   | Models | Estruturas de dados |
   | UI | Componentes visuais |
   | Events | Eventos disparados |

2. **Identificar Fluxo:**
   - Entrada → Processamento → Saída
   - Validações aplicadas
   - Tratamento de erros

3. **Levantar Dependências:**
   - Serviços externos
   - Outros fluxos que este afeta
   - Outros fluxos que afetam este

---

### 📝 Fase 2: GERAÇÃO DO DOCUMENTO

**Objetivo:** Criar documentação estruturada.

**Agente Envolvido:** `documentation-writer` (fallback: agente da Fase 1)

**Template Obrigatório:**

```markdown
# {Nome do Fluxo}

> {Descrição breve do propósito do fluxo}

## Visão Geral

[Diagrama Mermaid do fluxo - sequência ou flowchart]

## Componentes Envolvidos

| Arquivo | Responsabilidade | Linha/Função Principal |
|---------|------------------|------------------------|
| `path/to/file.ts` | Descrição | `functionName()` |

## Fluxo Detalhado

### 1. {Etapa 1}
- Descrição
- Validações
- Possíveis erros

### 2. {Etapa 2}
...

## Regras de Negócio

| Regra | Descrição | Onde Aplicada |
|-------|-----------|---------------|
| RN-01 | ... | `file.ts:L42` |

## Casos de Teste Essenciais

### Happy Path
- [ ] {Cenário de sucesso 1}
- [ ] {Cenário de sucesso 2}

### Edge Cases
- [ ] {Caso limite 1}
- [ ] {Caso limite 2}

### Error Cases
- [ ] {Cenário de erro 1}
- [ ] {Cenário de erro 2}

## Dependências

### Este fluxo afeta:
- {Outro fluxo/módulo}

### Este fluxo é afetado por:
- {Outro fluxo/módulo}

## Documentos Relacionados

- [{Doc relacionado 1}](./outro-doc.md)
- [{Doc relacionado 2}](../architecture/sistema.md)
```

**Salvar em:** `docs/flows/{nome-do-fluxo}.md`

---

### 🔗 Fase 3: CROSS-REFERENCE

**Objetivo:** Manter consistência entre documentações.

**Agente Envolvido:** `project-planner` (para visão sistêmica)

1. **Atualizar INDEX:**
   ```markdown
   Adicionar entrada em docs/INDEX.md:
   
   | Fluxo | Descrição | Última Atualização |
   |-------|-----------|-------------------|
   | [{nome}](./flows/{nome}.md) | {desc} | {data} |
   ```

2. **Linkar Documentos Relacionados:**
   - Adicionar referência nos docs existentes que se relacionam
   - Garantir links bidirecionais

3. **Notificar:**
   - Informar quais documentos foram atualizados

---

## Output

| Artefato | Local |
|----------|-------|
| Documentação do fluxo | `docs/flows/{nome-do-fluxo}.md` |
| Index atualizado | `docs/INDEX.md` |
| Docs relacionados atualizados | Links bidirecionais |

---

## Examples

```bash
# Documentar fluxo de cadastro de produtos
/document cadastro de produtos

# Documentar fluxo de autenticação
/document autenticação OAuth

# Documentar processo de pagamento
/document checkout e pagamento
```
