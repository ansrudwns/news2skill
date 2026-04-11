import os
import shutil
import glob
import re
import hashlib
from datetime import datetime
from dotenv import load_dotenv
import sys

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

def get_secret_key() -> str:
    key = os.getenv("AGENT_PRIVATE_SIGNATURE_KEY")
    if not key:
        print("🚨 CRITICAL ERROR: AGENT_PRIVATE_SIGNATURE_KEY not found in .env. Halting to prevent insecure supply chain.")
        import sys
        sys.exit(1)
    return key

def generate_file_hash(filepath: str) -> str:
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

import json

def verify_commit_safety_audit_mode(filepath: str) -> bool:
    """Audit-only mode: Verifies .intoto.json SLSA provenance and rejects legacy/missing."""
    sig_path = filepath + ".intoto.json"
    legacy_sig = filepath + ".sig"
    
    if os.path.exists(legacy_sig):
        print(f"🚨 AUDIT BLOCK: Legacy .sig file detected for {os.path.basename(filepath)}. Possible Downgrade Attack! Rejecting.")
        return False
        
    if not os.path.exists(sig_path):
        print(f"🚨 AUDIT REJECT: No .intoto.json provenance found for {os.path.basename(filepath)}. Strict rejection active.")
        return False
        
    try:
        with open(sig_path, 'r', encoding='utf-8') as f:
            attestation = json.load(f)
            
        payload_str = json.dumps(attestation["payload"], sort_keys=True)
        public_key = get_secret_key() 
        expected_signature = hashlib.sha256((payload_str + public_key).encode()).hexdigest()
            
        if attestation["signature"] == expected_signature:
            builder_id = attestation["payload"]["predicate"]["builder"]["id"]
            print(f"🔒 VERIFIED PROVENANCE: {os.path.basename(filepath)} is authentically audited by [{builder_id}].")
            return True
        else:
            print(f"🚨 AUDIT ALERT: Provenance Signature mismatch! {os.path.basename(filepath)} may be compromised.")
            return False
    except Exception as e:
        print(f"⚠️ AUDIT WARNING: Could not parse .intoto.json for {os.path.basename(filepath)}. Error: {e}")
        return False

def extract_metadata(filepath):
    description = "No description provided."
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'description:\s*(.+)', content)
            if match:
                description = match.group(1).strip()
    except Exception as e:
        pass
    return description

def update_agents_index(track_type, name, description, dest_path):
    agents_file = "AGENTS.md"
    if not os.path.exists(agents_file):
        return
    
    with open(agents_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # Check if already exists to prevent duplicate lines
    if any(name in line for line in lines):
        return

    new_lines = []
    inserted = False
    
    if track_type == "skill":
        target_header = "### [STANDARD MODE]"
    elif track_type == "diary":
        target_header = "## Track B:"
    elif track_type == "archive":
        target_header = "## Track F:"
    else:
        target_header = "## Track C:" # Backlog
        
        if not any(line.startswith(target_header) for line in lines):
            lines.append("\n## Track C: Research Backlog\n")

    for line in lines:
        new_lines.append(line)
        if line.startswith(target_header) and not inserted:
            formatted_entry = f"- **{name}**: {description} (Path: `{dest_path}`)\n"
            new_lines.append(formatted_entry)
            inserted = True
            
    with open(agents_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def main():
    staging_dir = os.path.join(".agents", "staging")
    if not os.path.exists(staging_dir):
        print("✅ Staging directory not found. Nothing to commit.")
        return

    files = glob.glob(os.path.join(staging_dir, "draft_*.md"))
    if not files:
        print("✅ No valid drafts to commit in staging.")
        return

    for file in files:
        basename = os.path.basename(file)

        # [Phase 3] Strict Verification Enforcement
        is_safe = verify_commit_safety_audit_mode(file)
        if not is_safe:
            print(f"❌ REJECTED: {basename} failed supply-chain verification. Dropping from staging.")
            try:
                os.remove(file)
                if os.path.exists(file + ".intoto.json"):
                    os.remove(file + ".intoto.json")
            except:
                pass
            continue

        is_skill = basename.startswith("draft_skill_")
        is_diary = basename.startswith("draft_diary_")
        is_backlog = basename.startswith("draft_backlog_")
        is_archive = basename.startswith("draft_archive_")
        
        if not (is_skill or is_diary or is_backlog or is_archive):
            continue
            
        track_type = "skill" if is_skill else ("diary" if is_diary else ("archive" if is_archive else "backlog"))
        folder = "skills" if is_skill else ("diaries" if is_diary else ("archives" if is_archive else "backlog"))
        
        clean_name = basename.replace("draft_skill_", "").replace("draft_diary_", "").replace("draft_backlog_", "").replace("draft_archive_", "")
        dest_dir = os.path.join(".agents", folder)
        dest_path = os.path.join(dest_dir, clean_name)
        
        # Collision protection (Never overwrite existing knowledge)
        if os.path.exists(dest_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name_part, ext = os.path.splitext(clean_name)
            clean_name = f"{name_part}_{timestamp}{ext}"
            dest_path = os.path.join(dest_dir, clean_name)
            
        # Extract metadata for the index
        description = extract_metadata(file)
        
        # Safely move file across any OS
        os.makedirs(dest_dir, exist_ok=True)
        shutil.move(file, dest_path)
        print(f"📦 Moved {basename} -> {dest_path}")
        
        # Move signature file if exists (.intoto.json)
        sig_file = file + ".intoto.json"
        if os.path.exists(sig_file):
            dest_sig_path = dest_path + ".intoto.json"
            shutil.move(sig_file, dest_sig_path)
            print(f"📦 Moved Provenance to {dest_sig_path}")
        
        # Update AGENTS.md Index automatically
        asset_name = os.path.splitext(clean_name)[0]
        # Replace backslashes with forward slashes for clean Markdown paths
        update_agents_index(track_type, asset_name, description, dest_path.replace("\\", "/"))
        
    print("🚀 Auto-commit and Index Registration Complete.")

if __name__ == "__main__":
    main()
