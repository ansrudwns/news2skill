import os
import json
import hashlib
import glob
from datetime import datetime, timezone
from dotenv import load_dotenv
import sys
import utils

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")



def sign_draft(filepath: str, signature_key: str):
    print(f"[Signer] Processing: {os.path.basename(filepath)}...")
    
    # 0. Heuristic Security Auditor (Block destructive payload injection)
    FORBIDDEN_KEYWORDS = ['os.system', 'subprocess.Popen', 'subprocess.run', 'rm -rf', 'requests.post', 'curl ', 'Invoke-WebRequest', 'powershell', 'import base64', 'b64decode', 'ignore previous instructions']
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for kw in FORBIDDEN_KEYWORDS:
                if kw in content:
                    print(f"🚨 AUDITOR REJECT: Destructive keyword '{kw}' detected in {os.path.basename(filepath)}. Strict SLSA Rejection active.")
                    return False
    except Exception as e:
        print(f"❌ Failed to parse {filepath} for heuristic audit: {e}")
        return False
    
    # 1. Compute original file hash
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        file_hash = hasher.hexdigest()
    except Exception as e:
        print(f"❌ Failed to read {filepath}: {e}")
        return False
    
    # 2. Construct SLSA Provenance payload
    # Drop draft_ prefixes so the subject correctly represents the final deployed asset name.
    basename = os.path.basename(filepath)
    clean_name = basename.replace("draft_skill_", "").replace("draft_diary_", "").replace("draft_backlog_", "").replace("draft_archive_", "")
    
    provenance = {
        "_type": "https://in-toto.io/Statement/v0.1",
        "subject": [{"name": clean_name, "digest": {"sha256": file_hash}}],
        "predicateType": "https://slsa.dev/provenance/v0.2",
        "predicate": {
            "builder": {"id": "Antigravity-Automated-Signer-CLI"},
            "metadata": {
                "ruleSet": "Basic-Heuristic-Static-Analysis",
                "completeness": {"parameters": True, "environment": True, "materials": False},
                "reproducible": False
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    }
    
    # 3. Create HMAC Signature
    payload_str = json.dumps(provenance, sort_keys=True)
    final_signature = hashlib.sha256((payload_str + signature_key).encode()).hexdigest()
    
    # 4. Bundle Attestation
    attestation = {
        "payload": provenance,
        "signature": final_signature
    }

    # 5. Output .intoto.json
    sig_path = filepath + ".intoto.json"
    try:
        with open(sig_path, 'w', encoding='utf-8') as f:
            json.dump(attestation, f, indent=2)
        print(f"🔒 ✅ [ATTESTED]: SLSA Provenance generated -> {sig_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to write signature target {sig_path}: {e}")
        return False

def main():
    signature_key = utils.get_secret_key()
    staging_dir = os.path.join(".agents", "staging")
    
    if not os.path.exists(staging_dir):
        print("✅ Staging directory not found. Nothing to sign.")
        return

    # Find all generated drafts
    files = glob.glob(os.path.join(staging_dir, "draft_*.md"))
    if not files:
        print("✅ No valid drafts to sign in staging.")
        return
        
    has_failure = False
    for file in files:
        success = sign_draft(file, signature_key)
        if not success:
            has_failure = True
            
    if has_failure:
        print("🚨 One or more drafts failed validation or signing.")
        sys.exit(1)

if __name__ == "__main__":
    main()
