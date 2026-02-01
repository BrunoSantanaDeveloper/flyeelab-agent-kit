# Product Requirements Document (PRD)

> **Status:** [ ] Rascunho | [ ] Em Revisão | [ ] Aprovado  
> **Última Atualização:** YYYY-MM-DD  
> **Autor:** [Nome]

---

## 1. Informações Gerais

| Campo | Valor |
|-------|-------|
| **Nome do Produto** | [Nome] |
| **Owner** | [Nome/Cargo] |
| **Stakeholders** | [Nomes] |
| **Data de Criação** | [YYYY-MM-DD] |
| **Versão** | 1.0 |

---

## 2. Visão e Contexto

### 2.1 Problem Statement
> Qual problema estamos resolvendo? Para quem?

[Descreva o problema de forma clara e específica]

### 2.2 Vision Statement
> Qual é a visão de sucesso para este produto?

[Descreva a visão em 1-2 parágrafos]

### 2.3 Market Context
> Qual o contexto de mercado? Concorrentes? Oportunidades?

[Descreva o contexto de mercado]

### 2.4 Competitive Analysis
| Competidor | Forças | Fraquezas | Nossa Diferença |
|------------|--------|-----------|-----------------|
| [Comp 1] | [+] | [-] | [Diferencial] |
| [Comp 2] | [+] | [-] | [Diferencial] |

---

## 3. Target Users (Personas)

### 3.1 Persona Primária: [Nome]

| Atributo | Descrição |
|----------|-----------|
| **Perfil** | [Idade, cargo, contexto] |
| **Objetivos** | [O que quer alcançar] |
| **Frustrações** | [Pain points atuais] |
| **Comportamento** | [Como age hoje] |

> **Quote:** "[Frase que representa esta persona]"

---

### 3.2 Persona Secundária: [Nome]

| Atributo | Descrição |
|----------|-----------|
| **Perfil** | [Idade, cargo, contexto] |
| **Objetivos** | [O que quer alcançar] |
| **Frustrações** | [Pain points atuais] |
| **Comportamento** | [Como age hoje] |

> **Quote:** "[Frase que representa esta persona]"

---

## 4. User Journey

### 4.1 Current Journey (AS-IS)
> Como o usuário resolve o problema hoje?

```
[Usuário] → [Ação 1] → [Frustração] → [Ação 2] → [Resultado insatisfatório]
```

**Pain Points Identificados:**
1. [Frustração 1]
2. [Frustração 2]
3. [Frustração 3]

### 4.2 Future Journey (TO-BE)
> Como será a experiência com nosso produto?

```
[Usuário] → [Ação 1 Simplificada] → [Nosso Produto] → [Resultado desejado]
```

**Benefícios:**
1. [Benefício 1]
2. [Benefício 2]
3. [Benefício 3]

---

## 5. Success Metrics (KPIs)

| Métrica | Baseline | Target | Como Medir |
|---------|----------|--------|------------|
| [Ex: Taxa de Conversão] | [X%] | [Y%] | [Analytics/Ferramenta] |
| [Ex: NPS] | [Score] | [Score] | [Pesquisa] |
| [Ex: Tempo de Tarefa] | [Xmin] | [Ymin] | [Tracking] |

### 5.1 North Star Metric
> Qual a métrica principal que define sucesso?

**[Nome da Métrica]:** [Descrição e target]

---

## 6. Requirements

### 6.1 Functional Requirements (MVP)

| ID | Feature | Prioridade | Persona | Descrição |
|----|---------|------------|---------|-----------|
| F1 | [Nome] | P0 (Must) | [Persona] | [Descrição] |
| F2 | [Nome] | P0 (Must) | [Persona] | [Descrição] |
| F3 | [Nome] | P1 (Should) | [Persona] | [Descrição] |

### 6.2 Non-Functional Requirements

| Categoria | Requisito | Critério de Aceite |
|-----------|-----------|-------------------|
| **Performance** | [Tempo de resposta] | [< Xs] |
| **Segurança** | [Autenticação] | [OAuth 2.0 / JWT] |
| **Acessibilidade** | [WCAG] | [Nível AA] |
| **Escalabilidade** | [Usuários simultâneos] | [X users] |

### 6.3 Out of Scope (Não MVP)

> Explicitamente fora do escopo inicial:

- [ ] [Feature para fase 2]
- [ ] [Integração para depois]
- [ ] [Funcionalidade complexa]

---

## 7. Assumptions & Dependencies

### 7.1 Assumptions
> O que estamos assumindo como verdade?

1. [Assumimos que usuários têm acesso a...]
2. [Assumimos que a API X estará disponível...]
3. [Assumimos que ...]

### 7.2 Dependencies
> De quem/o que dependemos?

| Dependência | Tipo | Owner | Status |
|-------------|------|-------|--------|
| [API de Pagamentos] | Externa | [Empresa] | [ ] Confirmado |
| [Design System] | Interna | [Time] | [ ] Pronto |

---

## 8. Risks & Mitigations

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| [Usuários não adotarem] | Média | Alto | [Onboarding guiado] |
| [Integração falhar] | Baixa | Alto | [Plano B manual] |
| [Prazo não cumprido] | Alta | Médio | [MVP reduzido] |

---

## 9. Timeline & Roadmap

### 9.1 MVP Timeline

| Fase | Duração | Entrega |
|------|---------|---------|
| Discovery | [X semanas] | PRD + TDD aprovados |
| Development | [X semanas] | MVP funcional |
| Testing | [X semanas] | QA completo |
| **Launch** | [Data] | Go-live |

### 9.2 Future Phases

| Fase | Features | Estimativa |
|------|----------|------------|
| V1.1 | [Features da fase 2] | [Q2 2026] |
| V2.0 | [Features avançadas] | [Q3 2026] |

---

## 10. Approval Checklist

### Completude
- [ ] Problem Statement claro e específico
- [ ] Pelo menos 2 personas definidas
- [ ] MVP claramente delimitado
- [ ] Métricas de sucesso quantificadas
- [ ] Riscos identificados com mitigações
- [ ] Timeline definido

### Aprovações
- [ ] **Revisado por Product Owner**
- [ ] **Revisado por Stakeholder Principal**
- [ ] **Aprovado para Discovery Técnico**

---

## 11. Histórico de Alterações

| Data | Autor | Alteração |
|------|-------|-----------|
| YYYY-MM-DD | [Nome] | Criação inicial |
| YYYY-MM-DD | [Nome] | [Descrição da alteração] |

---

> **⚠️ IMPORTANTE:** Este documento é o **contrato de produto**.  
> Após aprovação, mudanças significativas devem passar por nova revisão.
