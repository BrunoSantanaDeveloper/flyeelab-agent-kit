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

---

## 🔀 QUANDO USAR `/document` vs `/legacy-project`?

> [!TIP]
> **Escolha o workflow certo:**

| Situação | Use | Por quê? |
|----------|-----|----------|
| Documentar **UM fluxo** específico | `/document [fluxo]` | Focado, rápido |
| Documentar **PROJETO INTEIRO** | `/legacy-project [path]` | Análise completa + TDD reverso |
| Apenas **analisar estrutura** | `/discovery --from-project` | Mapeamento inicial |
| **Modernizar** projeto legado | `/legacy-project` → tasks | Fluxo completo |

> [!NOTE]
> `/document` é chamado internamente pelo `/legacy-project` na Phase 2.
> Use `/document` standalone quando precisar documentar apenas um fluxo isolado.

---

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

### 🔒 Fase 2.5: CODE-TRUTH VALIDATION (OBRIGATÓRIO)

**Objetivo:** Garantir que TODA afirmação técnica no doc corresponde ao código real.

> [!CAUTION]
> **NÃO salvar o documento sem executar esta validação.**
> Esta fase existe para impedir que documentação descreva estado planejado como se fosse
> estado atual (ex: documentar "gateway Pagar.me ativo" quando o código tem Cielo).

**Checklist de Validação:**

1. **Para cada integração/gateway/API externa mencionada:**
   - [ ] Arquivo/classe existe no codebase? (`find_by_name` / `grep_search`)
   - [ ] Está registrado no enum/config correspondente?
   - [ ] Se descrito como "ativo/implementado" → código NÃO é stub/mock?
   - [ ] Se descrito como "planejado" → marcado com `⏳ PLANEJADO` no doc?

2. **Para cada arquivo/componente referenciado:**
   - [ ] Path existe?
   - [ ] Funções/métodos citados existem na assinatura real?

3. **Para cada enum/constante/config:**
   - [ ] Valor confirmado contra o fonte real?

**Se detectar divergência entre doc e código:**
- Separar em seções distintas: `## Estado Atual` vs `## Estado Planejado`
- Marcar estado planejado com `> ⏳ **Ainda não implementado no código**`
- Registrar divergência como débito técnico

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

### 📢 Fase 4: PUBLICAÇÃO NO FLYEE

**Objetivo:** Publicar documentação no Flyee para acesso sem repositório.

> [!IMPORTANT]
> **SKILL:** Seguir Flyee API → seção "DOCUMENTATION DATABASES" OBRIGATORIAMENTE.

#### 4.1 — Documentação Técnica (SEMPRE)

1. Buscar database "Documentação Técnica" (skill → "DATABASE 1")
2. Verificar upsert (doc já existe?)
3. Criar/atualizar página com template correto
4. Preencher propriedades: Nome, Módulo, Tipo=Fluxo, Status, Arquivo Local

#### 4.2 — Manual do Usuário (SE fluxo de usuário)

> Executar apenas se o fluxo documentado é visível para o usuário final ou operador.

1. Buscar database "Manual do Usuário" (skill → "DATABASE 2")
2. Verificar se guia correspondente já existe
3. Gerar versão em linguagem acessível (sem código, sem componentes)
4. Criar/atualizar página com template de guia do usuário
5. Preencher propriedades: Nome, Seção, Status, Público-alvo

> [!TIP]
> Se o fluxo é puramente backend (ex: cron jobs, migrations), pular 4.2.
> Se o fluxo tem interface visível (ex: checkout, login), executar 4.2.

---

## Output

| Artefato | Local |
|----------|-------|
| Documentação do fluxo | `docs/flows/{nome-do-fluxo}.md` |
| Index atualizado | `docs/INDEX.md` |
| Docs relacionados atualizados | Links bidirecionais |
| Página Flyee (técnica) | Database "Documentação Técnica" |
| Página Flyee (manual) | Database "Manual do Usuário" (se aplicável) |

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
