import os
import sys
from dotenv import load_dotenv


def get_secret_key() -> str:
    """Retrieves the SLSA cryptographic signature key securely."""
    load_dotenv()
    key = os.getenv("AGENT_PRIVATE_SIGNATURE_KEY")
    if not key:
        print("CRITICAL ERROR: AGENT_PRIVATE_SIGNATURE_KEY not found in .env.")
        print("Run setup.bat to generate a unique cryptographic ID.")
        sys.exit(1)
    return key


# ---------------------------------------------------------------------------
# Static audit ruleset  (substring matching, case-sensitive)
# ---------------------------------------------------------------------------
# P0 — Hard Fail: active shell / filesystem destruction patterns
# P1 — Hard Fail: network exfiltration / obfuscation / prompt-injection
# P2 — Warning only: potentially dangerous but context-dependent
# ---------------------------------------------------------------------------

AUDIT_RULES: dict[str, list[str]] = {
    "P0": [
        "os.system",
        "subprocess.Popen",
        "subprocess.run",
        "shutil.rmtree",
        "Invoke-WebRequest",
        "powershell",
        "rm -rf",
        "Remove-Item -Recurse",
        "git reset --hard",
    ],
    "P1": [
        "requests.post",
        "urllib.request.urlopen",
        "curl ",
        "import base64",
        "b64decode",
        "ignore previous instructions",
        "read .env",
        "API_KEY",
    ],
    "P2": [
        "os.remove",
        "os.rename",
        "git push",
        "rewrite entire file",
        "large refactor",
        "must use bash",
        "grep only",
    ],
}

_LEVEL_ORDER = {"P0": 0, "P1": 1, "P2": 2}


def audit_text(content: str) -> dict:
    """
    Scan *content* for AUDIT_RULES matches.

    Returns:
        {
            "max_risk": "P0" | "P1" | "P2" | None,
            "findings": [
                {"level": "P0", "keyword": "os.system", "snippet": "...line..."},
                ...
            ]
        }
    """
    findings: list[dict] = []

    for level, keywords in AUDIT_RULES.items():
        for kw in keywords:
            if kw in content:
                snippet = ""
                for line in content.splitlines():
                    if kw in line:
                        snippet = line.strip()[:120]
                        break
                findings.append({"level": level, "keyword": kw, "snippet": snippet})

    if not findings:
        return {"max_risk": None, "findings": []}

    max_risk = min(findings, key=lambda f: _LEVEL_ORDER[f["level"]])["level"]
    return {"max_risk": max_risk, "findings": findings}
