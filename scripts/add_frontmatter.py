import os
import re

target_dirs = [".agents/skills", ".agents/diaries", ".agents/archives", ".agents/backlog"]

def extract_summary(content: str) -> str:
    lines = content.splitlines()
    summary_lines = []
    capturing = False
    for line in lines:
        if line.startswith("# ") and not capturing:
            summary_lines.append(line.lstrip("# ").strip())
            capturing = True
            continue
        if capturing:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                summary_lines.append(stripped)
            if len(summary_lines) >= 4:  # heading + 3 lines
                break
    
    if summary_lines:
        # Escape quotes to prevent breaking YAML
        return " ".join(summary_lines)[:400].replace('"', "'")
    return "Legacy migrated asset."

def fix_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if there's a description frontmatter
    if re.search(r'^description:\s*(.+)', content, re.MULTILINE):
        return False
        
    print(f"Adding description to: {filepath}")
    
    summary = extract_summary(content)
    
    # Check if it has a frontmatter block
    if content.startswith("---\n"):
        # Insert description after the first ---
        new_content = content.replace("---\n", f"---\ndescription: \"{summary}\"\n", 1)
    else:
        # Add frontmatter block at the top
        new_content = f"---\ndescription: \"{summary}\"\n---\n" + content
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

modified = 0
for d in target_dirs:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.md'):
                if fix_frontmatter(os.path.join(root, file)):
                    modified += 1

print(f"Total modified: {modified}")
