import re
import json
import argparse
import os
import sys

# =============================================================================
# AUTO-FILL MAPPINGS (Generic defaults)
# =============================================================================

# Default category based on Agent responsible
DEFAULT_AGENT_TO_CATEGORY = {
    "frontend-specialist": ["Frontend", "UI/UX"],
    "backend-specialist": ["Backend", "API"],
    "mobile-developer": ["Mobile", "Frontend"],
    "devops-engineer": ["DevOps", "Infra"],
    "security-auditor": ["Backend", "Security"],
    "debugger": ["Debug"],
    "orchestrator": ["Planejamento"],
    "database-architect": ["Backend", "Database"],
}

# Story Points based on Estimate
ESTIMATE_TO_POINTS = {
    "S": 2,      "XS": 1,
    "Pequeno": 2,
    "M": 3,
    "Médio": 3,
    "L": 5,
    "Grande": 5,
    "XL": 8,
    "Muito Grande": 8,
}

def get_category(agent: str, custom_mapping=None) -> list:
    """Returns category list based on agent."""
    mapping = custom_mapping or DEFAULT_AGENT_TO_CATEGORY
    agent_key = agent.lower().replace(" ", "-").split(",")[0].strip()
    
    for key, cats in mapping.items():
        if key in agent_key or agent_key in key:
            return cats
    return ["Outros"]

def get_points(estimate: str) -> int:
    """Returns story points based on estimate."""
    return ESTIMATE_TO_POINTS.get(estimate, 3)

def parse_markdown_stories(file_path):
    """Simple parser for Markdown user stories if JSON not provided"""
    with open(file_path, "r", encoding="utf-8") as f:
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
        
    return tasks

def main():
    parser = argparse.ArgumentParser(description="Prepare Notion Updates from Stories")
    parser.add_argument("--input", required=True, help="Input file (Markdown stories or parsed JSON)")
    parser.add_argument("--database-id", required=True, help="Target Notion Database ID")
    parser.add_argument("--epic", required=True, help="Epic name for the tasks (e.g. 'Authentication')")
    parser.add_argument("--id-map", help="JSON file mapping Task IDs to Page IDs (for updates)")
    parser.add_argument("--output", default="notion_updates.json", help="Output JSON file")
    
    args = parser.parse_args()

    # 1. Load Tasks
    if args.input.endswith('.json'):
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Convert list to dict if needed, or assume list format
            if isinstance(data, list):
                tasks = {t['id']: t for t in data}
            else:
                tasks = data
    else:
        tasks = parse_markdown_stories(args.input)

    # 2. Load ID Map (if exists)
    id_map = {}
    if args.id_map and os.path.exists(args.id_map):
        with open(args.id_map, 'r', encoding='utf-8') as f:
            id_map = json.load(f)
    
    print(f"Loaded {len(tasks)} tasks.")
    if id_map:
        print(f"Loaded {len(id_map)} ID mappings.")

    updates = []
    creates = []

    for tid, tdata in tasks.items():
        # Handle different structures (parsed json vs markdown dict)
        description = tdata.get('description', "") 
        if not description and 'content' in tdata:
             description = "\n".join(tdata['content']).strip()

        agent = tdata.get('agent', 'Pending')
        estimate = tdata.get('estimate', 'M')
        priority = tdata.get('priority', 'Medium')
        title = tdata.get('title', f"{tid} Task")

        props = {
            "ID": {"rich_text": [{"text": {"content": str(tid)}}]},
            "Épico": {"select": {"name": args.epic}},
            "Prioridade": {"select": {"name": priority}},
            "Estimativa": {"rich_text": [{"text": {"content": estimate}}]},  # Changed to text as per ARCHITECTURE
            "Agente": {"select": {"name": agent.replace(" + ", ",").split(",")[0].strip()}},
            "Descrição": {"rich_text": [{"text": {"content": description[:1900]}}]},
            
            # Auto-fill
            "Categoria": {"multi_select": [{"name": "Feature"}]}, # Standardized to Feature
            "Pontos": {"number": get_points(estimate)},
            "% Progresso": {"number": 0},
            "Tags": {"multi_select": [{"name": cat} for cat in get_category(agent)]} # Moved technical tags to Tags
        }
        
        # Check if updating or creating
        page_id = id_map.get(tid)
        
        if page_id:
            updates.append({"page_id": page_id, "properties": props})
        else:
            create_props = props.copy()
            # Ensure title is set for creation
            if "Nome da tarefa" not in create_props:
                 create_props["Nome da tarefa"] = {"title": [{"text": {"content": title}}]}
            
            create_props["Status"] = {"status": {"name": "backlog"}}
            creates.append({"parent": {"database_id": args.database_id}, "properties": create_props})

    # Output
    output_data = {"updates": updates, "creates": creates}
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Generated {len(updates)} updates and {len(creates)} creates")
    print(f"📄 Output written to: {args.output}")

if __name__ == "__main__":
    main()
