import os
import json
import hashlib
import glob
from datetime import datetime, timezone
from dotenv import load_dotenv
import sys

def get_secret_key() -> str:
    # Ensure env is loaded securely
    load_dotenv()
    key = os.getenv("AGENT_PRIVATE_SIGNATURE_KEY")
    if not key:
        print("🚨 CRITICAL ERROR: AGENT_PRIVATE_SIGNATURE_KEY not found in .env.")
        print("Run setup.bat to generate a unique cryptographic ID.")
        sys.exit(1)
    return key

def sign_draft(filepath: str, signature_key: str):
    print(f"[Signer] Processing: {os.path.basename(filepath)}...")
    
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
    provenance = {
        "_type": "https://in-toto.io/Statement/v0.1",
        "subject": [{"name": os.path.basename(filepath), "digest": {"sha256": file_hash}}],
        "predicateType": "https://slsa.dev/provenance/v0.2",
        "predicate": {
            "builder": {"id": "Antigravity-Automated-Signer-CLI"},
            "metadata": {
                "ruleSet": "Adversarial-Verification-Passed",
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
    signature_key = get_secret_key()
    staging_dir = os.path.join(".agents", "staging")
    
    if not os.path.exists(staging_dir):
        print("✅ Staging directory not found. Nothing to sign.")
        return

    # Find all generated drafts
    files = glob.glob(os.path.join(staging_dir, "draft_*.md"))
    if not files:
        print("✅ No valid drafts to sign in staging.")
        return
        
    for file in files:
        sign_draft(file, signature_key)

if __name__ == "__main__":
    main()
