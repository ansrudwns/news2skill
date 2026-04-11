import os
import sys
from dotenv import load_dotenv

def get_secret_key() -> str:
    """Retrieves the SLSA cryptographic signature key securely."""
    load_dotenv()
    key = os.getenv("AGENT_PRIVATE_SIGNATURE_KEY")
    if not key:
        print("🚨 CRITICAL ERROR: AGENT_PRIVATE_SIGNATURE_KEY not found in .env.")
        print("Run setup.bat to generate a unique cryptographic ID.")
        sys.exit(1)
    return key
