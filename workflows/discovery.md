---
description: Workflow completo de descoberta a produção. Brainstorm → TDD → Design System → Validação → Tarefas no Notion. Fluxo automatizado e contínuo.
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

```
┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐    ┌────────────┐
│ BRAINSTORM │───▶│  TDD AUTO  │───▶│   DESIGN   │───▶│  VALIDATE  │───▶│  APPROVE   │───▶│   NOTION   │
│  (Socratic)│    │  (Generate)│    │   SYSTEM   │    │  (Review)  │    │  (Human)   │    │   (Tasks)  │
└────────────┘    └────────────┘    └────────────┘    └────────────┘    └────────────┘    └────────────┘
                                           ↓
                                  design-system/MASTER.md
```

---

## 🔴 FLUXO AUTOMATIZADO

### Fase 0: INTEGRAÇÃO COM /demand (Se --from-demand)

**Trigger:** Comando executado com `--from-demand "Nome da Proposta"`

**Ações:**
1. Buscar proposta aprovada no Notion database "Propostas Comerciais"
2. Verificar se Status = "Aprovado"
3. Se NÃO aprovado:
   ```
   ⚠️ PROPOSTA NÃO APROVADA
   
   A proposta "[Nome]" ainda não foi aprovada.
   Status atual: [Status]
   
   Aguarde aprovação do cliente antes de iniciar o discovery.
   ```
4. Se APROVADO, extrair dados e pré-preencher:
   
   | Campo Proposta | Pré-preenche |
   |----------------|--------------|
   | Problema a Ser Resolvido | Nível 1 - Qual problema |
   | Must-have (MVP) | Nível 1 - O que é essencial |
   | Nice-to-have | Nível 1 - O que NÃO entra |
   | Stack | Nível 1 - Tecnologias |
   | Prazo Desejado | Nível 8 - Timeline |
   | Risco | Nível 1 - Riscos |
   | Qtd Telas | Nível 3 - Páginas |

5. Pular perguntas já respondidas na proposta
6. Informar usuário quais dados foram importados:
   ```
   ✅ DADOS IMPORTADOS DA PROPOSTA

   📄 Proposta: [Nome]
   💰 Valor: R$ XX.XXX
   
   Dados pré-preenchidos:
   - ✓ Problema/Contexto
   - ✓ MVP definido
   - ✓ Stack tecnológica
   - ✓ Prazo
   
   Continuando com perguntas complementares...
   ```

---

### Fase 0.5: REVERSE ENGINEERING (Se --from-project)

**Trigger:** Comando executado com `--from-project "path/to/project"`

> 🔄 Esta fase analisa um projeto existente para gerar TDD automaticamente.

**Agentes por Sub-fase:**

| Sub-fase | Agente Lead | Skill | Ação |
|----------|-------------|-------|------|
| 0.1 | `orchestrator` | `architecture` | Ler config files (`package.json`, `CODEBASE.md`, `ARCHITECTURE.md`) |
| 0.2 | `orchestrator` | `architecture` | Mapear estrutura de pastas e detectar padrões |
| 0.3 | `backend-specialist` | `database-design` | Extrair entidades (models, types, schemas, interfaces) |
| 0.4 | `frontend-specialist` | `frontend-design` | Identificar rotas, páginas e componentes |
| 0.5 | `backend-specialist` | `api-patterns` | Mapear integrações (APIs externas, DBs, serviços) |
| 0.6 | `orchestrator` | `plan-writing` | Consolidar dados e gerar TDD draft |
| 0.7 | `frontend-specialist` | `tailwind-patterns` | Extrair design tokens do código (cores, tipografia, spacing) |

---

#### 📂 Sub-fase 0.1: Leitura de Configurações

**Ações:**
1. Ler `package.json` (ou equivalente) para identificar:
   - Nome do projeto
   - Stack tecnológica (dependências)
   - Scripts disponíveis
2. Ler `CODEBASE.md` se existir
3. Ler `ARCHITECTURE.md` se existir
4. Ler `.env.example` para identificar variáveis de ambiente

**Output:** Metadados do projeto (nome, stack, padrões)

---

#### 📂 Sub-fase 0.2: Mapeamento de Estrutura

**Ações:**
1. Listar diretórios principais (`src/`, `app/`, `pages/`, `components/`, etc.)
2. Identificar padrões arquiteturais:
   - Monorepo vs Single Repo
   - Feature-based vs Layer-based
   - Client/Server separation
3. Detectar frameworks (Next.js, React Native, Express, etc.)

**Output:** Estrutura do projeto + padrões identificados

---

#### 📂 Sub-fase 0.3: Extração de Entidades

**Ações:**
1. Buscar arquivos de modelo/schema:
   - `*.model.ts`, `*.schema.ts`, `*.entity.ts`
   - Prisma schema, TypeORM entities, Mongoose models
   - GraphQL types, Zod schemas
2. Extrair para cada entidade:
   - Nome
   - Campos (nome, tipo, obrigatório)
   - Relacionamentos
   - Status atual (se documentado)

**Output:** Lista de entidades com campos e relacionamentos

---

#### 📂 Sub-fase 0.4: Identificação de Rotas/Páginas

**Ações:**
1. Buscar arquivos de rota:
   - Next.js: `app/*/page.tsx`, `pages/*.tsx`
   - React Router: `routes.ts`, `Router.tsx`
   - Express: `*.routes.ts`, `router.ts`
2. Extrair para cada rota:
   - Path
   - Método (GET/POST/etc.)
   - Parâmetros
   - Componente/Handler associado
3. Identificar fluxos de navegação

**Output:** Mapa de rotas + componentes

---

#### 📂 Sub-fase 0.5: Mapeamento de Integrações

**Ações:**
1. Identificar conexões de banco de dados:
   - Prisma, TypeORM, Mongoose, Drizzle
   - Connection strings em `.env.example`
2. Identificar APIs externas:
   - fetch/axios calls
   - SDK imports (Stripe, Supabase, Firebase, etc.)
3. Identificar serviços:
   - Auth providers
   - Storage providers
   - Email/SMS providers

**Output:** Lista de integrações externas

---

#### 📂 Sub-fase 0.6: Geração de TDD Draft

**Ações:**
1. Consolidar dados das sub-fases anteriores
2. Mapear para seções do TDD:
   
   | Dado Extraído | Seção TDD |
   |---------------|-----------|
   | Stack tecnológica | Informações Gerais |
   | Estrutura de pastas | Arquitetura |
   | Entidades | Entidades e Schema |
   | Rotas/Páginas | Fluxo Técnico |
   | Integrações | Recursos e APIs Externas |
   
3. Gerar arquivo `docs/design/TDD-{nome}.md` com dados pré-preenchidos
4. Marcar seções não identificadas como `⚠️ REQUER VALIDAÇÃO`

**Output:** TDD draft gerado

---

#### 📂 Sub-fase 0.7: Extração de Design Tokens (Se projeto tem UI)

**Agente:** `frontend-specialist` (Lead) + `mobile-developer` (se mobile)

**Skill:** `frontend-design`, `tailwind-patterns`

**Ações:**
1. Buscar arquivos de configuração de design:
   
   | Arquivo | Framework | Tokens Extraídos |
   |---------|-----------|------------------|
   | `tailwind.config.js` | Tailwind | colors, spacing, fonts, screens |
   | `tailwind.config.ts` | Tailwind | colors, spacing, fonts, screens |
   | `globals.css` / `index.css` | CSS | `:root` variables |
   | `theme.ts` / `theme.js` | Styled/Emotion | theme object |
   | `tokens.ts` / `tokens.js` | Custom | design tokens |
   | `colors.ts` / `palette.ts` | Custom | color definitions |
   | `typography.ts` | Custom | font definitions |
   | `app.json` / `*.xcassets` | React Native/iOS | brand colors |

2. Para cada fonte encontrada, extrair:

   **Cores:**
   ```
   - Nome do token (primary, secondary, accent)
   - Valor hex (#XXXXXX)
   - Uso (background, text, border)
   ```

   **Tipografia:**
   ```
   - Font family (Inter, Roboto, etc.)
   - Font weights usados
   - Tamanhos (sm, base, lg, xl)
   ```

   **Espaçamento:**
   ```
   - Spacing scale (4, 8, 16, 24, 32)
   - Padding/margin patterns
   - Gap patterns
   ```

   **Sombras:**
   ```
   - Shadow definitions
   - Elevation levels
   ```

3. Analisar componentes existentes para inferir padrões:
   - Border-radius padrão
   - Transition durations
   - Z-index scale

---

#### 📂 Sub-fase 0.7.1: Geração do MASTER.md

**Ações:**
1. Criar estrutura `design-system/{projeto}/`
2. Gerar `MASTER.md` com tokens extraídos:

   ```markdown
   # Design System Master File

   **Project:** {nome}
   **Source:** Code Extraction (Reverse Engineering)
   **Generated:** {data}

   ---

   ## Global Rules

   ### Color Palette
   | Role | Hex | CSS Variable |
   |------|-----|--------------|
   | Primary | `#XXXXXX` | `--color-primary` |
   | ... | ... | ... |

   ### Typography
   - **Heading Font:** {extraído}
   - **Body Font:** {extraído}

   ### Spacing Variables
   | Token | Value | Usage |
   |-------|-------|-------|
   | `--space-sm` | `8px` | ... |
   | ... | ... | ... |
   ```

3. Identificar e marcar tokens não encontrados como `⚠️ NÃO ENCONTRADO`
4. Adicionar seção de Anti-Patterns baseada em padrões detectados

---

#### 📊 Mensagem ao Usuário

```
✅ ANÁLISE DO PROJETO CONCLUÍDA

📁 Projeto: [path/to/project]
📦 Stack: [React, Node.js, PostgreSQL, ...]
📊 Entidades encontradas: XX
📄 Rotas/Páginas: XX
🔌 Integrações: XX
🎨 Design Tokens: XX extraídos

TDD Draft: docs/design/TDD-{nome}.md
Design System: design-system/{nome}/MASTER.md

Seções pré-preenchidas:
- ✓ Stack tecnológica
- ✓ Entidades e campos
- ✓ Rotas e navegação
- ✓ Integrações externas
- ✓ Design Tokens (cores, tipografia, spacing)

Seções que precisam de validação:
- ⚠️ Contexto e Motivação
- ⚠️ MVP Scope (revisar prioridades)
- ⚠️ Regras de Negócio

Continuando com brainstorm para gaps identificados...
```

---

### Fase 1: BRAINSTORM (Automático)

**Trigger:** Início do comando

**Agentes por Nível:**

| Nível | Agente Lead | Colaboradores | Skill |
|-------|-------------|---------------|-------|
| 1. Visão Geral | `orchestrator` | - | `brainstorming` |
| 2. Entidades | `backend-specialist` | `database-architect` | `database-design` |
| 3. Fluxos/UI | `frontend-specialist` | `mobile-developer` | `frontend-design` |
| 3.5. Regras UI | `frontend-specialist` | `product-owner` | `frontend-design` |
| 4. Monetização | `product-manager` | `backend-specialist` | `api-patterns` |
| 5. Métricas | `product-owner` | `backend-specialist` | `testing-patterns` |
| 6. Dashboard | `frontend-specialist` | `backend-specialist` | `frontend-design` |
| 7. Onboarding | `product-owner` | `frontend-specialist` | `brainstorming` |
| 8. Infraestrutura | `devops-engineer` | `security-auditor` | `deployment-procedures` |

**Ações:**
1. Ativar skill `brainstorming`
2. Para cada nível, invocar agente lead para gerar perguntas contextuais
3. Fazer perguntas em **8 níveis**:

---

#### 📋 Nível 1: Visão Geral (Obrigatório)

| Pergunta | Propósito |
|----------|-----------|
| 🎯 Qual problema você está resolvendo? | Contexto e motivação |
| 👥 Quem são os usuários? (tipos) | Personas e roles |
| 📦 O que é essencial no MVP? | Escopo do MVP |
| ❌ O que NÃO entra no MVP? | Fora de escopo |
| ⚠️ Quais riscos você enxerga? | Riscos conhecidos |
| 🔧 Tecnologias preferidas? | Stack técnica |
| 🎨 Qual estilo visual? | Para Design System |
| 🖼️ Tem referências visuais/prints? | **CRÍTICO:** Upload agora! |

---

#### 📋 Nível 2: Entidades e Campos (Obrigatório para projetos com dados)

Para cada **entidade principal** identificada no MVP:

| Pergunta | Exemplo |
|----------|---------|
| Quais são as entidades principais? | Usuário, Produto, Pedido |
| Quais campos são obrigatórios em [Entidade]? | Nome, email, senha |
| Quais campos são opcionais? | Foto, bio, CNPJ |
| Existe cadastro em etapas? Quais? | Etapa 1: dados, Etapa 2: endereço |
| Quais status/estados a entidade pode ter? | Ativo, inativo, pendente |

---

#### 📋 Nível 3: Fluxos e Interações (Obrigatório para projetos com UI)

| Pergunta | Propósito |
|----------|-----------|
| Quais são as páginas principais? | Definir navegação |
| Quais filtros existem na listagem/busca? | Campos de filtro |
| Quais dados são capturados em cada interação? | Analytics, leads |
| Quais ações o usuário pode fazer? | CRUD, contato, compra |
| Existe fluxo de aprovação/moderação? | Workflows internos |

---

#### 📋 Nível 3.5: Regras de Interface e Conversão (CRÍTICO para UI)

> Perguntar sobre "barreiras" e regras visuais que impactam o negócio

| Pergunta | Propósito |
|----------|-----------|
| 🔒 Existe conteúdo bloqueado? (ex: login para ver preço) | Regras de acesso |
| 🧱 O contato é direto ou tem barreira (Lead Wall)? | Regra de conversão (Ex: Modal antes do Whats) |
| 🦶 O que é obrigatório no Rodapé e Header? | Links legais e navegação |
| 🔍 Filtros são visíveis ou escondidos (sidebar/modal)? | UX de busca |

---

#### 📋 Nível 4: Monetização e Regras de Negócio (Se aplicável)

> Perguntar se o projeto tem modelo de monetização (SaaS, freemium, assinatura, etc.)

| Pergunta | Propósito |
|----------|-----------|
| Qual o modelo de monetização? | Assinatura, freemium, one-time |
| Quais planos existem? (nomes e preços) | Estrutura de pricing |
| Quais limites por plano? | Produtos, usuários, storage |
| Quais features são exclusivas por plano? | Destaques, analytics, suporte |
| Existe ranking/prioridade por plano? | Visibilidade no catálogo |
| Existe trial/período gratuito? | Onboarding |

---

#### 📋 Nível 5: Métricas e Tracking (Se aplicável)

> Perguntar se o projeto precisa rastrear eventos/métricas

| Pergunta | Propósito |
|----------|-----------|
| Quais eventos precisam ser rastreados? | Lista de eventos |
| Quais métricas por plano/tier? | Diferenciação de analytics |
| O que define um "lead" ou conversão? | Definição de KPI |
| Métricas influenciam ranking? | Lógica de ordenação |
| Agregação em tempo real ou batch? | Arquitetura de dados |
| Requisitos de LGPD/privacidade? | Compliance |

---

#### 📋 Nível 6: Área Logada e Dashboard (Se aplicável)

> Perguntar sobre funcionalidades da área autenticada

| Pergunta | Propósito |
|----------|-----------|
| Quais seções existem no dashboard? | Navegação interna |
| Quais dados o usuário pode ver? | Permissões de leitura |
| Quais ações o usuário pode fazer? | CRUD, configurações |
| Existe diferença de acesso por plano? | Features gated |
| Quais formulários existem? | Inputs e validações |
| Existe área admin separada? | Backoffice |

---

#### 📋 Nível 7: Onboarding/Cadastro (Se aplicável)

> Perguntar sobre fluxo de cadastro de usuários/clientes

| Pergunta | Propósito |
|----------|-----------|
| Existe wizard de cadastro? Quantas etapas? | Estrutura do fluxo |
| Quais dados são coletados em cada etapa? | Campos por step |
| Conta é criada antes ou depois dos dados? | Ordem lógica |
| Precisa escolher plano durante cadastro? | Monetização inline |
| Upload de mídia no cadastro? | Storage requirements |
| Quais validações por campo? | Frontend + Backend |
| O que acontece após finalizar? | Redirect, email, etc. |
| Dados persistem se abandonar? | State management |

---

#### 📋 Nível 8: Infraestrutura e Ambientes (Obrigatório)

> Perguntar sobre ambientes de desenvolvimento e deploy

| Pergunta | Propósito |
|----------|-----------|
| 🌍 Quais ambientes você precisa? (dev/staging/prod) | Estrutura de ambientes |
| 🚀 Qual plataforma de hospedagem? (Vercel/Railway/VPS) | Decisão de infra |
| 🔄 Deploy automático ou manual? | Estratégia de CI/CD |
| 🔑 Quais variáveis de ambiente por ambiente? | Gestão de secrets |
| 📊 Precisa de monitoramento? (logs, APM, alertas) | Observabilidade |
| 🗄️ Banco de dados separado por ambiente? | Isolamento de dados |
| 🔒 Requisitos de segurança por ambiente? (SSL, WAF) | Compliance |
| 💰 Qual orçamento mensal de infra? | Constraints de custo |

---

3. Documentar respostas estruturadas
4. Se usuário pular pergunta, marcar como `⚠️ INDEFINIDO` no TDD

**Output:** Contexto estruturado + especificações para TDD completo

---

### Fase 2: TDD GENERATION (Automático)

**Trigger:** Após brainstorm completo

**Agentes por Seção do TDD:**

| Seção TDD | Agente Responsável | Fonte (Nível Brainstorm) |
|-----------|-------------------|--------------------------|
| Contexto e Motivação | `orchestrator` | Nível 1 |
| Glossário e Termos | `orchestrator` | Todos os níveis |
| Entidades e Schema | `backend-specialist` + `database-architect` | Nível 2 |
| Fluxos de Navegação | `frontend-specialist` | Nível 3 |
| Regras de Negócio | `product-manager` | Nível 3.5 + 4 |
| MVP Scope | `product-owner` | Nível 1 |
| Fora de Escopo | `product-owner` | Nível 1 |
| Riscos e Mitigações | `security-auditor` | Nível 1 + 8 |
| Métricas e KPIs | `product-owner` | Nível 5 |
| Área Admin | `backend-specialist` | Nível 6 |

**Skills:** `plan-writing`, `architecture`, `database-design`

**Ações:**
1. Usar template de `.agent/templates/tdd-template.md`
2. Cada agente preenche sua seção com respostas do brainstorm:
   - `orchestrator` → Contexto, Motivação, Glossário
   - `backend-specialist` → Entidades, Schema, API Contracts
   - `frontend-specialist` → Navegação, Componentes, Filtros
   - `product-manager` → Regras de negócio, Monetização
   - `product-owner` → MVP, Fora de Escopo, Métricas
   - `security-auditor` → Riscos, Compliance, Segurança
3. Salvar em `docs/design/TDD-{nome}.md`

**Output:** TDD preenchido automaticamente com contribuição de cada especialista

---

### Fase 2.5: DESIGN SYSTEM (Automático)

**Trigger:** Após TDD gerado (se projeto tem UI)

**Agentes (por tipo de projeto):**

| Tipo Projeto | Agente Lead | Skill Primária |
|--------------|-------------|----------------|
| Web App | `frontend-specialist` | `frontend-design` |
| Mobile App | `mobile-developer` | `mobile-design` |
| Híbrido | `frontend-specialist` + `mobile-developer` | Ambas |

**Skills:** `frontend-design`, `mobile-design`, `tailwind-patterns`

**Ações:**
1. Identificar tipo de projeto (Web/Mobile/Híbrido)
2. Agente lead extrai keywords do TDD:
   - Tipo de produto (SaaS, e-commerce, etc.)
   - Indústria (moda, fintech, etc.)
   - Estilo desejado (se informado)
   - Referências visuais (se fornecidas)
3. `frontend-specialist` ou `mobile-developer` executa workflow `/ui-ux-pro-max`:
   ```bash
   python3 .agent/.shared/ui-ux-pro-max/scripts/search.py "{keywords}" --design-system --persist -p "{nome-projeto}"
   ```
4. Validar output contra regras do agent (Purple Ban, Template Ban, etc.)
5. Salvar output em `design-system/MASTER.md`

**Output:** Design System completo com:
- Paleta de cores (validada por especialista)
- Tipografia (fonts)
- Estilos visuais
- Anti-patterns a evitar
- Tokens CSS/Tailwind

**Skip:** Se usuário informar `--no-design` ou projeto não tiver UI

---

### Fase 2.6: FIGMA IMPORT (Se --from-figma)

**Trigger:** Comando executado com `--from-figma "https://figma.com/file/..."`

> 🎨 Esta fase importa um Design System já desenvolvido no Figma e documenta no formato `MASTER.md`.

**Agentes:**

| Agente | Skill | Responsabilidade |
|--------|-------|------------------|
| `frontend-specialist` (Lead) | `frontend-design` | Coordenar extração e validação |
| `mobile-developer` | `mobile-design` | Validar tokens mobile (se aplicável) |

---

#### 🎨 Sub-fase 2.6.1: Coleta de Informações do Figma

**Ações:**
1. Solicitar ao usuário:
   - Link do Figma (file ou design system)
   - Nome do projeto
   - Tipo de projeto (Web/Mobile/Híbrido)
2. Se disponível link de Dev Mode, usar para extrair tokens
3. Se não, solicitar screenshots/exports das seguintes seções:
   - **Colors:** Paleta de cores do Figma
   - **Typography:** Fontes e tamanhos
   - **Spacing:** Grid e espaçamentos
   - **Components:** Botões, cards, inputs, modals

**Perguntas ao Usuário:**
```
🎨 IMPORTAÇÃO DO FIGMA

Para documentar seu Design System, preciso das seguintes informações:

1. 📎 Link do Figma: [obrigatório]
2. 🔑 Tem acesso ao Dev Mode? [Sim/Não]
3. 📱 Tipo de projeto: [Web / Mobile / Híbrido]

Se não tiver Dev Mode, faça export das seções:
- Colors (screenshot da paleta)
- Typography (screenshot das fontes)
- Components (screenshot dos principais componentes)
```

---

#### 🎨 Sub-fase 2.6.2: Extração de Tokens

**Ações por Seção:**

| Seção | Dados a Extrair | Destino MASTER.md |
|-------|-----------------|-------------------|
| **Colors** | Cores (nome, hex, uso) | `## Color Palette` |
| **Typography** | Fontes, pesos, tamanhos | `## Typography` |
| **Spacing** | Grid, gaps, paddings | `## Spacing Variables` |
| **Shadows** | Elevações, blur, spread | `## Shadow Depths` |
| **Buttons** | Estados, border-radius, padding | `## Component Specs > Buttons` |
| **Cards** | Border-radius, shadow, padding | `## Component Specs > Cards` |
| **Inputs** | Border, focus state, padding | `## Component Specs > Inputs` |
| **Modals** | Overlay, border-radius, padding | `## Component Specs > Modals` |

**Formato de Extração (por cor):**
```markdown
| Role | Hex | CSS Variable |
|------|-----|--------------|
| Primary | `#XXXXXX` | `--color-primary` |
| Secondary | `#XXXXXX` | `--color-secondary` |
| ...
```

---

#### 🎨 Sub-fase 2.6.3: Geração do MASTER.md

**Ações:**
1. Usar estrutura compatível com `/ui-ux-pro-max`:
   ```
   design-system/
   ├── {projeto}/
   │   ├── MASTER.md          ← Tokens globais
   │   └── pages/
   │       ├── home.md        ← Overrides por página
   │       └── dashboard.md
   ```

2. Preencher MASTER.md com dados extraídos:
   - `## Global Rules > Color Palette`
   - `## Global Rules > Typography`
   - `## Global Rules > Spacing Variables`
   - `## Global Rules > Shadow Depths`
   - `## Component Specs`
   - `## Style Guidelines`
   - `## Anti-Patterns`
   - `## Pre-Delivery Checklist`

3. Adicionar metadata:
   ```markdown
   **Project:** {nome}
   **Source:** Figma Import
   **Figma Link:** {link}
   **Generated:** {data}
   ```

4. Validar contra regras do agent:
   - Purple Ban check
   - Contrast ratio check
   - Font pairing validation

---

#### 🎨 Sub-fase 2.6.4: Documentação de Páginas (Opcional)

**Se usuário fornecer páginas específicas no Figma:**

1. Para cada página, criar `design-system/{projeto}/pages/{pagina}.md`
2. Documentar overrides específicos:
   - Cores diferentes da paleta global
   - Componentes únicos da página
   - Layout específico

**Formato:**
```markdown
# Page: {Nome da Página}

> **OVERRIDE:** Este arquivo sobrescreve regras do MASTER.md para esta página.

## Color Overrides
[tokens específicos]

## Component Overrides
[specs específicas]
```

---

#### 📊 Mensagem ao Usuário (Output)

```
✅ DESIGN SYSTEM IMPORTADO DO FIGMA

📁 Figma: {link}
📂 Salvo em: design-system/{projeto}/MASTER.md

Tokens extraídos:
- ✓ X cores documentadas
- ✓ X fontes mapeadas
- ✓ X componentes especificados
- ✓ X espaçamentos definidos

Páginas documentadas:
- ✓ home.md
- ✓ dashboard.md (se aplicável)

⚠️ Validações:
- ✓ Contrast ratio OK
- ✓ Font pairing OK
- ⚠️ [avisos se houver]

Próximo: Fase 2.7 (Infraestrutura) ou Fase 3 (Validação)
```

---

#### 🔄 Compatibilidade com /ui-ux-pro-max

Esta fase é **100% compatível** com o workflow `/ui-ux-pro-max`:

| Recurso | Fase 2.5 (Gerar) | Fase 2.6 (Importar) |
|---------|------------------|---------------------|
| Output | `design-system/MASTER.md` | `design-system/MASTER.md` |
| Estrutura | Mesma | Mesma |
| Pages override | Suportado | Suportado |
| Anti-patterns | Gerados | Validados |
| Checklist | Incluído | Incluído |

**Diferença:**
- **Fase 2.5:** Gera Design System do zero via keywords
- **Fase 2.6:** Importa Design System existente do Figma

**Skip:** Se `--from-figma` não for informado (usa Fase 2.5 padrão)

---

### Fase 2.7: INFRASTRUCTURE DEFINITION (Automático)

**Trigger:** Após TDD gerado (se projeto precisa de deploy)

**Agentes:** `devops-engineer` (lead) + `security-auditor` (secrets) + `backend-specialist` (DB per env)

**Skills:** `deployment-procedures`, `architecture`, `vulnerability-scanner`

**Ações:**
1. Extrair respostas do Nível 8 do brainstorm
2. `devops-engineer` define:
   - Seleção de plataforma (decision tree)
   - Estratégia de CI/CD
   - Plano de rollback
   - Zero-downtime strategy
3. `security-auditor` valida:
   - Secrets management strategy
   - Env vars sensíveis identificadas
   - Compliance requirements
4. `backend-specialist` confirma:
   - DB isolation per environment
   - Connection strings strategy
5. Gerar seção "Infraestrutura" no TDD:
   - Ambientes definidos
   - Variáveis por ambiente
   - Estratégia de CI/CD
   - Plano de rollback
6. Atualizar `docs/design/TDD-{nome}.md` com seção de infra

**Output:** TDD atualizado com:
- Diagrama de ambientes
- Tabela de env vars por ambiente
- Pipeline de deploy definido
- Estratégia de rollback documentada
- Secrets management validado

**Skip:** Se usuário informar `--no-infra` ou projeto não precisar de deploy

---

### Fase 3: VALIDATION (🔴 OBRIGATÓRIO - NÃO PULAR)

> ⚠️ **REGRA CRÍTICA:** Esta fase é BLOQUEANTE. NÃO oferecer opções que pulem a validação.

**Trigger:** Após TDD gerado E aprovado pelo usuário

**Agentes:**

| Agente | Responsabilidade |
|--------|------------------|
| `tdd-reviewer` (Lead) | Validação geral do TDD |
| `security-auditor` | Validar seção de riscos e compliance |
| `backend-specialist` | Validar seção de entidades e API |
| `frontend-specialist` | Validar seção de navegação e UI |
| `devops-engineer` | Validar seção de infraestrutura |

**Skills:** `tdd-validation`, `architecture`, `code-review-checklist`

**Ações:**
1. `tdd-reviewer` lidera a validação
2. Cada agente valida sua seção:
   - `security-auditor` → Riscos, LGPD, Secrets
   - `backend-specialist` → Entidades, Schema, API contracts
   - `frontend-specialist` → Navegação, Componentes, Filtros
   - `devops-engineer` → Ambientes, CI/CD, Rollback
3. Gerar relatório de completude consolidado
4. Identificar itens INDEFINIDO por seção

**Output:** Relatório de validação com score por seção

**Mensagem obrigatória:**
```
🔍 EXECUTANDO VALIDAÇÃO DO TDD...

Isso é obrigatório antes de criar tasks.
```

---

### Fase 4: HUMAN APPROVAL (Gate)

**Trigger:** Após validação (não antes!)

**Agente Responsável:** `orchestrator` (Facilitador)
**Skill:** `brainstorming` (Feedback loop)

**Ações:**
1. **PARAR e mostrar ao usuário:**
   - TDD gerado
   - Relatório de validação
   - Score de completude
   - Itens que precisam de decisão
2. Aguardar aprovação explícita

**Gate:**
```
🛑 AGUARDANDO APROVAÇÃO HUMANA

TDD: docs/design/TDD-{nome}.md
Validation Score: XX%
Blockers: [lista]

Responda:
- "aprovar" → Continua para Design System / Notion
- "revisar" → Volta para edição
- "cancelar" → Para o workflow
```

> ⚠️ **NUNCA** perguntar ao usuário se quer pular direto para tasks.
> A validação DEVE ter sido executada antes de qualquer próximo passo.

---

### Fase 4.5: PRODUCT OWNER - User Stories (🔴 OBRIGATÓRIO)

> ⚠️ **REGRA:** Esta fase é OBRIGATÓRIA antes de criar tasks no Notion.

**Trigger:** Após TDD aprovado e Design System gerado

**Agentes:** `product-owner` (Lead) + `product-manager` (Review)

**Skills:** `plan-writing`, `tdd-workflow`, `documentation-templates`

**Ações:**
1. Ler seção "Detalhamento da Solução" do TDD
2. Para cada task do TDD, gerar:
   - **User Story** no formato: "As a [Persona], I want [Action], so that [Benefit]"
   - **Acceptance Criteria** no formato Gherkin (Given/When/Then)
   - **Prioridade** usando MoSCoW (Must/Should/Could/Won't)
   - **Estimativa** usando T-shirt sizing (XS/S/M/L/XL)
   - **Agente recomendado** para implementação
   - **Verificação** como validar conclusão
3. Gerar documento `docs/design/USER-STORIES-{nome}.md`

**Output Format por Task:**

```markdown
## [Número] [Nome da Task]

**User Story:**
> As a [persona], I want to [action], so that [benefit].

**Acceptance Criteria:**
- [ ] **Given** [context] **When** [action] **Then** [outcome]
- [ ] **Given** [context] **When** [action] **Then** [outcome]

**Priority:** [MUST | SHOULD | COULD | WON'T]
**Estimate:** [XS | S | M | L | XL]
**Agent:** [backend-specialist | frontend-specialist | etc.]
**TDD Ref:** Seção X.X
**Parallelizable:** [Sim | Não]
**Dependencies:** [Lista de tasks dependentes]

**Verification:**
- [ ] [Como verificar que está pronto]
```

**Gate:**
```
🛑 USER STORIES GERADAS

Documento: docs/design/USER-STORIES-{nome}.md
Total: XX stories
Must: XX | Should: XX | Could: XX

Responda:
- "aprovar" → Continua para criar tasks no Notion
- "ajustar" → Editar prioridades ou AC
```

---

### Fase 5: NOTION INTEGRATION (Automático após aprovação)

#### Fase 5.1: INFRA CHECK (Pre-flight Validation)

**Trigger:** Usuário aprova User Stories

**Agente Responsável:** `orchestrator` (Validador de integração)
**Skills:** `api-patterns`, `brainstorming` (feedback de erro)

**Ações:**
1. **Retrieve Database:** Usar `API-retrieve-a-data-source` no database alvo.
2. **Validate Schema:** Verificar existência e tipo das propriedades obrigatórias:
   - `Status` (Status)
   - `Priority` (Select options: P0, P1, P2)
   - `Estimate` (Select options: XS, S, M, L, XL)
   - `Agent` (Select)
   - `TDD Ref` (Text/RichText)
   - `Parallelizable` (Checkbox)
3. **Decisão Automática:**
   - **❌ Falha:** Se colunas estiverem faltando ou incorretas → **NOTIFICAR USUÁRIO** e aguardar correção.
   - **✅ Sucesso:** Se tudo estiver correto → Prosseguir para Fase 5.2.

**Mensagem de Erro (Exemplo):**
```
⚠️ ERRO DE SCHEMA NO NOTION
O Database selecionado não é compatível.
Faltam as colunas: [Priority, Estimate]
Por favor, ajuste o database e tente novamente.
```

---

#### Fase 5.2: TASK CREATION (Execution)

**Trigger:** Infra Check = PASS

**Agentes:**

| Agente | Responsabilidade |
|--------|------------------|
| `product-owner` (Lead) | Supervisionar criação e priorização |
| `orchestrator` | Executar chamadas MCP |

**Skills:** `api-patterns`, `documentation-templates`

**Ações:**
1. Ler documento `USER-STORIES-{nome}.md`
2. `orchestrator` executa para cada User Story:
   - Criar página no Notion via MCP
   - **Título:** Nome da task
   - **Descrição:** User Story + Acceptance Criteria
   - **Properties:** Mapear valores para o schema validado
3. `product-owner` confirma criação de todas as tasks

**MCP Integration:**
```
Usar: notion-mcp-server
API: API-retrieve-a-data-source (Pre-flight check)
API: API-post-page (Criar task com propriedades)
API: API-patch-block-children (Adicionar conteúdo formatado ao corpo)
API: API-post-search (Buscar/Validar database)
```

> [!IMPORTANT]
> **Propriedades vs. Corpo da Página:**
> - Propriedades (`rich_text`) **NÃO renderizam Markdown**. Use-as apenas para metadados curtos.
> - O corpo da página **renderiza formatação**. Use `patch-block-children` para inserir headings, listas e parágrafos formatados.

**Output:** Tarefas criadas no Notion com estrutura:

```
📁 TDD: {Nome do Projeto}
├── 📋 Task 1: Setup Infraestrutura
├── 📋 Task 2: Criar Entidade X
├── 📋 Task 3: Integração com API
└── 📋 Task 4: Testes E2E
```

---

## 📋 NOTION TASK STRUCTURE

Cada task criada no Notion terá (vindo do documento USER-STORIES):

| Campo | Destino | Fonte |
|-------|---------|-------|
| **Título** | Propriedade `title` | TDD |
| **Status** | Propriedade `status` (Backlog) | Default |
| **Prioridade** | Propriedade `select` (P0/P1/P2) | MoSCoW |
| **Estimativa** | Propriedade `select` (XS-XL) | T-shirt sizing |
| **Agente** | Propriedade `select` | Fase 4.5 |
| **TDD Ref** | Propriedade `rich_text` | TDD |
| **Parallelizable** | Propriedade `checkbox` | Dependências |
| **User Story** | 📄 **Corpo da página** (heading + paragraph) | Fase 4.5 |
| **Acceptance Criteria** | 📄 **Corpo da página** (bulleted_list) | Fase 4.5 |
| **Verification** | 📄 **Corpo da página** (bulleted_list) | Fase 4.5 |

---

## 🔧 CONFIGURAÇÃO NECESSÁRIA

### Notion Database

Para funcionar, você precisa de um database no Notion com estas propriedades:

| Propriedade | Tipo | Obrigatório | Uso |
|-------------|------|-------------|-----|
| Nome da tarefa | Title | ✅ | Título da task |
| Status | Status | ✅ | Backlog, In Progress, Done |
| Prioridade | Select (P0/P1/P2) | ✅ | MoSCoW mapeado |
| Estimativa | Select (XS/S/M/L/XL) | 🟡 | T-shirt |
| Agente | Select | 🟡 | Especialista recomendado |
| TDD Ref | Text | 🟡 | Link/seção do TDD |
| Parallelizable | Checkbox | 🟡 | Pode rodar em paralelo? |
| Fase | Select | 🟡 | Fase do roadmap |

> [!TIP]
> **Descrição (rich_text) é OPCIONAL.** O conteúdo formatado (User Story, ACs) vai no **corpo da página** via `patch-block-children`.

### MCP Server

Certifique-se que `notion-mcp-server` está configurado e conectado.

---

## 🚀 USAGE

### Comando Único (Faz Tudo)

```bash
/discovery meu projeto de delivery
```

**O que acontece:**
1. IA faz perguntas sobre o projeto (Brainstorm)
2. Você responde
3. TDD é gerado automaticamente
4. Design System é gerado (se UI)
5. TDD é validado (tdd-reviewer)
6. Você aprova o TDD
7. **Product Owner gera User Stories + AC** ← NOVO
8. Você aprova as User Stories
9. Tarefas detalhadas são criadas no Notion


---

### A partir de Design System do Figma

```bash
/discovery meu projeto --from-figma "https://figma.com/file/..."
```

**O que acontece:**
1. IA solicita informações do Figma (link, Dev Mode, tipo)
2. Extrai tokens: cores, tipografia, espaçamentos, componentes
3. Gera `design-system/MASTER.md` no formato padrão
4. Valida tokens (contrast, font pairing)
5. Fluxo normal continua (Validação → User Stories → Notion)

---

### A partir de Projeto Existente (Reverse Engineering)

```bash
/discovery --from-project "c:\path\to\project"
```

**O que acontece:**
1. IA analisa estrutura do projeto (package.json, pastas, código)
2. Extrai entidades, rotas, integrações automaticamente
3. Gera TDD draft pré-preenchido
4. Brainstorm foca apenas nos gaps identificados
5. Fluxo normal continua (Design System → Validação → Notion)

---

### Com Notion Database Específico

```bash
/discovery meu projeto --notion-db "Tasks Database"
```

---

## 📊 EXEMPLO COMPLETO

```
Usuário: /discovery app de delivery

IA: 🧠 Iniciando Discovery...

───────────────────────────────────
📋 FASE 1: BRAINSTORM
───────────────────────────────────

🎯 Qual problema você está resolvendo?
> Restaurantes pequenos não têm app próprio de delivery

👥 Quem são os usuários?
> Donos de restaurante e clientes finais

📦 O que é essencial no MVP?
> Cardápio, carrinho, pedido, notificação

⚠️ Que riscos você enxerga?
> Integração com pagamento, tempo real

🔧 Tecnologias preferidas?
> React Native, Node.js, PostgreSQL

───────────────────────────────────
📄 FASE 2: TDD GERADO
───────────────────────────────────

[OK] TDD criado: docs/design/TDD-delivery-app.md

───────────────────────────────────
✅ FASE 3: VALIDAÇÃO
───────────────────────────────────

Score: 85%
Blockers: 0
Warnings: 2 (Tratamento de erro, Retry strategy)

───────────────────────────────────
🛑 FASE 4: APROVAÇÃO
───────────────────────────────────

Revise o TDD e responda:
- "aprovar" → Criar tasks no Notion
- "revisar" → Voltar para edição

Usuário: aprovar

───────────────────────────────────
📌 FASE 5: NOTION
───────────────────────────────────

[OK] Criando tasks no Notion...

✅ Task criada: Setup Infraestrutura
✅ Task criada: Database Schema
✅ Task criada: API de Cardápio
✅ Task criada: App Mobile - Cardápio
✅ Task criada: Carrinho de Compras
✅ Task criada: Integração Pagamento
✅ Task criada: Notificações Push
✅ Task criada: Testes E2E

[DONE] 8 tasks criadas no Notion!
Link: [Seu Notion Database]
```

---

## 🔴 REGRAS

1. **Brainstorm é obrigatório** - Não pular perguntas
2. **TDD é gerado automaticamente** - Baseado nas respostas
3. **Validação é automática** - Mas mostra resultado
4. **Aprovação é humana** - Gate obrigatório
5. **Notion é automático** - Após aprovação

---

## 🔗 SKILLS E AGENTS UTILIZADOS

| Componente | Fase | Uso |
|------------|------|-----|
| `orchestrator` | Fase 0.5 + 1.1 + 2 | Reverse eng., visão geral, coordenação e TDD Contexto |
| `backend-specialist` | Fase 0.5 + 1.2 + 2 | Reverse eng. entidades, campos e TDD Schema |
| `frontend-specialist` | Fase 0.5 + 1.3-1.6 + 2 + 2.5 | Reverse eng. rotas, UI, Dashboard, TDD Nav e Design System |
| `architecture` | Fase 0.5 + 2.7 | Análise de estrutura e decisões arquiteturais |
| `backend-specialist` | Fase 1.2 + 2 | Entidades, campos e TDD Schema |
| `database-architect` | Fase 1.2 + 2 | Schema, relacionamentos e TDD DB |
| `frontend-specialist` | Fase 1.3-1.6 + 2 + 2.5 | UI, Dashboard, TDD Nav e Design System |
| `mobile-developer` | Fase 1.3 + 2.5 | Fluxos mobile e Design System |
| `product-manager` | Fase 1.4 + 2 | Regras de negócio e TDD Monetização |
| `product-owner` | Fase 1.5-1.7 + 2 + 4.5 | Métricas, User Stories e TDD MVP |
| `brainstorming` | Fase 1 | Perguntas Socráticas |
| `database-design` | Fase 1.2 + 2 | Design de schema |
| `frontend-design` | Fase 0.7 + 1.3-1.6 + 2.5 | Design tokens extraction e design de interfaces |
| `plan-writing` | Fase 2 | Escrita estruturada do TDD |
| `tdd-template` | Fase 2 | Estrutura do TDD |
| `mobile-design` | Fase 2.5 + 2.6 | Design mobile e validação Figma |
| `tailwind-patterns` | Fase 0.7 + 2.5 | Extração e geração de tokens de design |
| `ui-ux-pro-max` | Fase 2.5 + 2.6 | Design System Generator e Figma Import |
| `deployment-procedures` | Fase 2.7 | Decisões de plataforma e rollback |
| `architecture` | Fase 2.7 | Decisões arquiteturais de infra |
| `vulnerability-scanner` | Fase 2.7 | Validação de secrets |
| `devops-engineer` | Fase 1.8 + 2.7 | TDD Infraestrutura e ambientes |
| `security-auditor` | Fase 1.8 + 2.7 + 2 | Secrets, compliance e TDD Riscos |
| `tdd-reviewer` | Fase 3 | Validação do TDD |
| `tdd-validation` | Fase 3 | Algoritmo de score |
| `tdd-workflow` | Fase 4.5 | Metodologia TDD para User Stories |
| `documentation-templates` | Fase 4.5 | Formatação de documentos |
| `notion-mcp-server` | Fase 5 | Criação de tasks |

---

## ⚡ QUICK START

```bash
# Fluxo completo automatizado (com Design System)
/discovery nome do meu projeto

# A partir de projeto existente (Reverse Engineering)
/discovery --from-project "c:\path\to\project"

# Importar Design System do Figma
/discovery meu projeto --from-figma "https://figma.com/file/..."

# Combinar projeto existente + Figma
/discovery --from-project "c:\path" --from-figma "https://figma.com/file/..."

# Sem Design System (apenas TDD + Notion)
/discovery nome do projeto --no-design

# Sem Notion (apenas TDD + Design)
/discovery nome do projeto --no-notion

# Especificar database do Notion
/discovery nome --notion-db "Meu Database"
```
