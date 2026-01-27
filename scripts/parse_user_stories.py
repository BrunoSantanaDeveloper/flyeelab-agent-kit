
import re
import json

def parse_user_stories(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    stories = []
    # Regex to find story blocks
    # Looking for ### Title then content until next ### or ---
    
    sections = re.split(r'### ', content)[1:] # Skip preamble
    
    for section in sections:
        lines = section.split('\n')
        title_line = lines[0].strip()
        
        # Extract ID and Title (e.g., "1.1 Setup Inicial Next.js")
        match = re.match(r'(\d+\.\d+)\s+(.+)', title_line)
        if not match:
            continue
            
        story_id = match.group(1)
        story_title = match.group(2)
        full_title = f"{story_id} {story_title}"
        
        # Parse fields
        body = section
        
        priority_match = re.search(r'\*\*Priority:\*\*\s*(.+)', body)
        priority = priority_match.group(1).strip() if priority_match else "Medium"
        
        estimate_match = re.search(r'\*\*Estimate:\*\*\s*(.+)', body)
        estimate = estimate_match.group(1).strip() if estimate_match else "M"
        
        agent_match = re.search(r'\*\*Agent:\*\*\s*(.+)', body)
        agent = agent_match.group(1).strip() if agent_match else "Pending"
        
        # Extract User Story and Acceptance Criteria for Description
        # We'll just grab everything from **User Story:** down to **Verification:** or ---
        desc_start = body.find('**User Story:**')
        desc_end = body.find('**Verification:**')
        if desc_end == -1:
            desc_end = body.find('---', desc_start)
        
        description = body[desc_start:desc_end].strip() if desc_start != -1 else body.strip()
        
        stories.append({
            "id": story_id,
            "title": full_title,
            "priority": priority,
            "estimate": estimate,
            "agent": agent,
            "description": description
        })
        
    return stories

if __name__ == "__main__":
    results = parse_user_stories(r"c:\mobile-apps\Tanavitrine-refactor\docs\design\USER-STORIES-tanavitrine.md")
    with open(r"c:\mobile-apps\Tanavitrine-refactor\.agent\stories.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Successfully wrote stories.json")
