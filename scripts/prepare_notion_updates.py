import re
import json

stories_file = r"c:\mobile-apps\Tanavitrine-refactor\docs\design\USER-STORIES-tanavitrine.md"

# =============================================================================
# AUTO-FILL MAPPINGS (Configurado para preencher propriedades automaticamente)
# =============================================================================

# Categoria baseada no Agente responsável
AGENT_TO_CATEGORIA = {
    "frontend-specialist": ["Frontend", "UI/UX"],
    "backend-specialist": ["Backend", "API"],
    "mobile-developer": ["Mobile", "Frontend"],
    "devops-engineer": ["DevOps", "Infra"],
    "security-auditor": ["Backend", "Security"],
    "debugger": ["Debug"],
    "orchestrator": ["Planejamento"],
}

# Pontos (Story Points) baseado na Estimativa
ESTIMATE_TO_PONTOS = {
    "S": 2,      # Pequeno: ~2-4 horas
    "Pequeno": 2,
    "M": 3,      # Médio: ~1 dia
    "Médio": 3,
    "L": 5,      # Grande: ~2-3 dias
    "Grande": 5,
    "XL": 8,     # Muito Grande: ~1 semana
    "Muito Grande": 8,
}

def get_categoria(agent: str) -> list:
    """Retorna lista de categorias baseado no agente."""
    agent_key = agent.lower().replace(" ", "-").split(",")[0].strip()
    for key, cats in AGENT_TO_CATEGORIA.items():
        if key in agent_key or agent_key in key:
            return cats
    return ["Outros"]

def get_pontos(estimate: str) -> int:
    """Retorna story points baseado na estimativa."""
    return ESTIMATE_TO_PONTOS.get(estimate, 3)  # Default: 3 (Médio)

# =============================================================================

with open(stories_file, "r", encoding="utf-8") as f:
    content = f.read()

tasks = {}
current_task = None

lines = content.split('\n')
for line in lines:
    m = re.match(r"^### (\d+\.\d+) (.+)", line)
    if m:
        if current_task:
            tasks[current_task['id']] = current_task
        
        current_task = {
            'id': m.group(1),
            'title': m.group(2).strip(),
            'content': [],
            'priority': 'MUST',
            'estimate': 'S',
            'agent': 'frontend-specialist'
        }
    elif current_task:
        current_task['content'].append(line)
        
        if "**Priority:**" in line:
            current_task['priority'] = line.split("**Priority:**")[1].strip()
        if "**Estimate:**" in line:
            current_task['estimate'] = line.split("**Estimate:**")[1].strip()
        if "**Agent:**" in line:
            current_task['agent'] = line.split("**Agent:**")[1].strip()

if current_task:
    tasks[current_task['id']] = current_task


# Map IDs
id_map = {
    "1.1": "2f585c5d-674f-8197-b32d-f99f7ffb50f1",
    "1.2": "2f585c5d-674f-81e8-b30c-ddd044d9eb98",
    "1.3": None, # Missing
    "1.4": "2f585c5d-674f-81d2-97d1-e338327b726e",
    "2.1": "2f585c5d-674f-81c1-9e0a-c3e1edc7a4f5",
    "2.2": None, # Missing
    "2.3": "2f585c5d-674f-81af-b6cb-cbab1bb7baab",
    "2.4": "2f585c5d-674f-8125-a959-e4e107f681cf",
    "3.1": "2f585c5d-674f-8187-aee7-e3221446c62d",
    "3.2": "2f585c5d-674f-810d-8bc9-c6c6dec7c912",
    "3.3": "2f585c5d-674f-81ad-a998-e3e130d079f6",
    "3.4": "2f585c5d-674f-81c4-a90a-ec4f6c17fa9d",
    "4.1": "2f585c5d-674f-815f-a86f-d0ac2596a813",
    "4.2": "2f585c5d-674f-8127-9b26-fe632f7cf868",
    "4.3": "2f585c5d-674f-818f-b7cd-fcfa7a741161",
    "5.1": "2f585c5d-674f-81e7-8502-e9ec941d66d7",
    "5.2": "2f585c5d-674f-81f2-8d28-e3a2ad8a50e9",
    "6.1": "2f585c5d-674f-8161-a7f9-e9d9cf1d6b56",
    "6.2": "2f585c5d-674f-810b-a67a-d7b65a46cd32",
    "6.3": "2f585c5d-674f-81ca-991d-faadb4d963bd",
    "7.1": "2f585c5d-674f-81ee-90c1-cde84fb6bdca",
    "7.2": "2f585c5d-674f-8166-8fc5-d2d0eadfae04",
    "7.3": "2f585c5d-674f-819e-bc52-c5fc085a7cd7",
    "8.1": "2f585c5d-674f-813d-9e84-c7718b219226",
    "8.2": None # Missing
}


DATABASE_ID = "2df85c5d-674f-80f6-8086-fdbce0dec151"

UPDATES = []
CREATES = []

for tid, tdata in tasks.items():
    description = "\n".join(tdata['content']).strip()
    
    props = {
        # Propriedades originais
        "Prioridade": {"select": {"name": tdata['priority']}},
        "Estimativa": {"select": {"name": tdata['estimate']}},
        "Agente": {"select": {"name": tdata['agent'].replace(" + ", ",").split(",")[0].strip()}},
        "Descrição": {"rich_text": [{"text": {"content": description[:1900]}}]},
        "TDD Ref": {"rich_text": [{"text": {"content": tdata.get('tdd_ref', 'N/A')}}]},
        
        # AUTO-FILL: Novas propriedades (configurado em 2026-01-27)
        "Categoria": {"multi_select": [{"name": cat} for cat in get_categoria(tdata['agent'])]},
        "Pontos": {"number": get_pontos(tdata['estimate'])},
        "% Progresso": {"number": 0},  # Sempre começa em 0%
    }
    
    # Improve parsing to capture extra fields if possible, or just stick to basics.
    # The 'parse' loop above was simple. Let's just use what we have.
    

    if tid in id_map and id_map[tid]:
        page_id = id_map[tid]
        UPDATES.append({"page_id": page_id, "properties": props})
    else:
        # For creation we need Title and Parent
        create_props = props.copy()
        create_props["Nome da tarefa"] = {"title": [{"text": {"content": f"{tid} {tdata['title']}"}}]}
        create_props["Status"] = {"status": {"name": "Backlog"}}
        CREATES.append({"parent": {"database_id": DATABASE_ID}, "properties": create_props})

# Output JSON file with updates and creates
with open("notion_updates.json", "w", encoding="utf-8") as f:
    json.dump({"updates": UPDATES, "creates": CREATES}, f, indent=2, ensure_ascii=False)

print(f"✅ Generated {len(UPDATES)} updates and {len(CREATES)} creates")
print(f"📊 Properties auto-filled: Categoria, Pontos, % Progresso")
