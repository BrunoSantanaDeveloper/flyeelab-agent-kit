
import sys
import os
import argparse
import re

def update_task_md(file_path: str, task_id: str):
    """Updates the tabular status in task.md"""
    if not os.path.exists(file_path):
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    new_lines = []
    updated = False
    
    # Regex to match | 1 | or | 1.1 |
    # Matches: pipe, space, id, space, pipe
    # Using strict check for the ID column
    
    for line in lines:
        if line.strip().startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            # parts[0] is empty (before first pipe), parts[1] is ID
            if len(parts) > 2 and parts[1] == str(task_id):
                # Found the row. Update last column (Status)
                # Assuming standard 5-6 column layout. 
                # Let's rebuild the line carefully retaining structure if possible, 
                # or just replacing the last part.
                # Easiest: Replace the last column content.
                if "✅ Complete" not in parts[-2]: # Check status column (ignoring empty last part)
                     # Reconstruct line: replace last segment
                     # This is brittle if columns change. Let's use simple logic: replace last pipe content
                     last_pipe_index = line.rfind('|')
                     second_last_pipe = line.rfind('|', 0, last_pipe_index)
                     if second_last_pipe != -1:
                        new_line = line[:second_last_pipe] + "| ✅ Complete |"
                        new_lines.append(new_line)
                        updated = True
                        continue
        new_lines.append(line)
        
    if updated:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        print(f"✅ Updated task.md for Task {task_id}")
    return updated

def update_project_progress(file_path: str, task_id: str):
    """Updates inline status in PROJECT-PROGRESS.md e.g. #1 -> #1 ✅"""
    if not os.path.exists(file_path):
        print(f"⚠️ {file_path} not found.")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already marked
    # Pattern: #{task_id} followed by check or ✅
    # Regex: #{task_id}(?![^|\n]*✅) - negative lookahead is tricky with other text
    
    # Simple approach: Find "#{task_id}" not followed closely by "✅"
    updated_content = content
    pattern = rf"#{task_id}(?![:\s-]*✅)"
    
    # If we find specifically "#{task_id}" and it doesn't have a check next to it
    # We replace it with "#{task_id} ✅"
    # But wait, the format is "#1-#4...". 
    # If tasks are grouped "#1-#4", verifying individual task #2 is hard.
    # However, sometimes they are listed individually.
    
    # If found individual marker:
    if re.search(rf"#{task_id}\b", content):
        # Naive replacement: #{id} -> #{id} ✅
        # But we must avoid double checking
        updated_content = re.sub(rf"(#{task_id})\b(?![:\s-]*✅)", r"\1 ✅", content)
    
    if updated_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"✅ Updated PROJECT-PROGRESS.md for Task {task_id}")
        return True
    else:
        print(f"ℹ️  Task {task_id} not found or already marked in PROJECT-PROGRESS.md")
        return False

def main():
    parser = argparse.ArgumentParser(description="Automate Task Completion")
    parser.add_argument("task_id", help="Task ID (e.g. 1)")
    parser.add_argument("time_spent", help="Time spent (e.g. '1h')")
    parser.add_argument("summary", help="Summary message")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    
    args = parser.parse_args()
    
    # Update local files
    # 1. task.md (Artifact)
    # The artifact might be in a variable path, but usually we know the relative path or it's in the brain dir.
    # We will search for task.md in the current directory or standard paths.
    
    # Since we are running from root, let's try to find task.md
    task_md_path = None
    # Search recursively for task.md? No, usually in .brain or docs or root
    # For now, let's assume the user passes absolute path or we look in typical spots
    # In this environment, task.md is in the ephemeral brain dir.
    # We can try to find it using `fd` logic or just checking known artifact path provided in memory?
    # Actually, the agent knows the path. But the script doesn't.
    # Hack: Update the script to look into the 'brain' folder if it knows it, or just scan current dir and subdirs
    
    # For PROJECT-PROGRESS.md it is in docs/
    proj_progress_path = os.path.join(args.project_root, "docs", "PROJECT-PROGRESS.md")
    update_project_progress(proj_progress_path, args.task_id)

    # Output Instructions for Agent
    print(f"\n📢 ACTION REQUIRED: Execute Notion Tools")
    print(f"----------------------------------------")
    print(f"TASK ID: {args.task_id}")
    print(f"TIME: {args.time_spent}")
    print(f"SUMMARY: {args.summary}")
    print(f"----------------------------------------")
    print("Please run 'mcp_notion-mcp-server_API-patch-page' and 'create-a-comment'")

if __name__ == "__main__":
    main()
