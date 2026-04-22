import os
import re

target_dirs = [".agents/skills", ".agents/diaries", ".agents/archives", ".agents/backlog"]

def fix_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if there's a description frontmatter
    if re.search(r'^description:\s*(.+)', content, re.MULTILINE):
        return False
        
    print(f"Adding description to: {filepath}")
    
    # Check if it has a frontmatter block
    if content.startswith("---\n"):
        # Insert description after the first ---
        new_content = content.replace("---\n", "---\ndescription: Legacy migrated asset.\n", 1)
    else:
        # Add frontmatter block at the top
        new_content = "---\ndescription: Legacy migrated asset.\n---\n" + content
        
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
