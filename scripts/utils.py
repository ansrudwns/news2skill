import os
import re
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

# ---------------------------------------------------------------------------
# Code-block & frontmatter aware audit helpers
# ---------------------------------------------------------------------------
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_FENCE_RE = re.compile(r"```[^\n]*\n.*?```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
_ALLOWLIST_RE = re.compile(r"^\s*audit_allowlist:\s*\[(.*?)\]\s*$", re.MULTILINE)


def _extract_allowlist(content: str) -> set[str]:
    """Pull `audit_allowlist: ["foo", "bar"]` from YAML frontmatter, if any.

    A file may exempt specific keywords from hard-fail by listing them in its
    frontmatter. Allowlisted keywords still surface as P2 warnings.
    """
    fm_match = _FRONTMATTER_RE.match(content)
    if not fm_match:
        return set()
    body = fm_match.group(1)
    al_match = _ALLOWLIST_RE.search(body)
    if not al_match:
        return set()
    raw = al_match.group(1)
    return {tok.strip().strip('"').strip("'").lower() for tok in raw.split(",") if tok.strip()}


def _strip_code_regions(content: str) -> tuple[str, str]:
    """Split content into (prose, code) regions.

    Both fenced ```...``` blocks and inline `code` spans are extracted. The
    prose half is what the strict audit runs against; the code half is audited
    separately and its findings get downgraded one severity level.
    """
    code_chunks: list[str] = []

    def _harvest_fence(m: re.Match) -> str:
        code_chunks.append(m.group(0))
        return "\n"  # preserve line breaks for snippet stability

    prose = _FENCE_RE.sub(_harvest_fence, content)

    def _harvest_inline(m: re.Match) -> str:
        code_chunks.append(m.group(0))
        return " "

    prose = _INLINE_CODE_RE.sub(_harvest_inline, prose)
    return prose, "\n".join(code_chunks)


def _scan(text: str) -> list[dict]:
    """Raw substring scan against AUDIT_RULES. Returns findings list."""
    findings: list[dict] = []
    if not text:
        return findings
    text_lower = text.lower()
    for level, keywords in AUDIT_RULES.items():
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in text_lower:
                snippet = ""
                for line in text.splitlines():
                    if kw_lower in line.lower():
                        snippet = line.strip()[:120]
                        break
                findings.append({"level": level, "keyword": kw, "snippet": snippet})
    return findings


def _downgrade(level: str) -> str:
    """P0→P1, P1→P2, P2 stays P2. Used for in-code-block findings."""
    return {"P0": "P1", "P1": "P2", "P2": "P2"}[level]


def audit_text(content: str) -> dict:
    """
    Scan *content* for AUDIT_RULES matches with code-block awareness.

    Severity is graduated:
      * Findings in prose (outside code fences/spans) keep their original level.
      * Findings inside ``` ``` fences or `inline code` are downgraded one
        level (P0→P1, P1→P2, P2→P2). This stops legitimate code examples in
        skill docs from being hard-rejected, while still surfacing payloads
        that someone tried to hide inside fences.
      * Frontmatter `audit_allowlist: [...]` entries always cap at P2 (per-file
        documented exception).

    Returns:
        {
            "max_risk": "P0" | "P1" | "P2" | None,
            "findings": [
                {"level": "P0", "keyword": "os.system", "snippet": "...line...",
                 "region": "prose" | "code", "downgraded": False},
                ...
            ]
        }
    """
    allowlist = _extract_allowlist(content)
    prose, code = _strip_code_regions(content)

    raw_prose = _scan(prose)
    raw_code = _scan(code)

    findings: list[dict] = []

    for f in raw_prose:
        kw_lower = f["keyword"].lower()
        # Allowlist still demotes prose findings to P2 (deliberate exemption).
        effective = "P2" if kw_lower in allowlist and _LEVEL_ORDER[f["level"]] < _LEVEL_ORDER["P2"] else f["level"]
        findings.append({
            "level": effective,
            "keyword": f["keyword"],
            "snippet": f["snippet"],
            "region": "prose",
            "downgraded": effective != f["level"],
        })

    for f in raw_code:
        kw_lower = f["keyword"].lower()
        downgraded_level = _downgrade(f["level"])
        # Allowlist further caps to P2 (rare double-effect; idempotent for P2).
        if kw_lower in allowlist:
            downgraded_level = "P2"
        findings.append({
            "level": downgraded_level,
            "keyword": f["keyword"],
            "snippet": f["snippet"],
            "region": "code",
            "downgraded": downgraded_level != f["level"],
        })

    if not findings:
        return {"max_risk": None, "findings": []}

    max_risk = min(findings, key=lambda f: _LEVEL_ORDER[f["level"]])["level"]
    return {"max_risk": max_risk, "findings": findings}
