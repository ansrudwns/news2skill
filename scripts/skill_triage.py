"""
skill_triage.py — External Skill Quarantine Gate (MVP)

Usage:
  python scripts/skill_triage.py --query "keyword"
      Scan all .md files under external_skills/ whose name or content matches
      the keyword. Prints audit results. Dry-run, no changes made.

  python scripts/skill_triage.py --file external_skills/foo.md
      Audit a single file. Dry-run, no changes made.

  python scripts/skill_triage.py --file external_skills/foo.md --import-approved
      Audit then import (if P0/P1 clean) into .agents/external_approved/skills/.
      Updates INDEX.json atomically. Logs rejects to rejected.log.

Safety rules enforced:
  - Target must reside under external_skills/ (no ../ traversal, no symlinks).
  - P0 or P1 findings → hard reject even with --import-approved.
  - P2 findings → warning only, import proceeds.
  - AGENTS.md is never touched by this script.
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import date, datetime, timezone
from pathlib import Path

# Resolve project root (one level above scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXTERNAL_DIR = PROJECT_ROOT / "external_skills"
APPROVED_DIR = PROJECT_ROOT / ".agents" / "external_approved"
SKILLS_DIR   = APPROVED_DIR / "skills"
INDEX_PATH   = APPROVED_DIR / "INDEX.json"
REJECTED_LOG = APPROVED_DIR / "rejected.log"

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
from utils import audit_text, AUDIT_RULES, _LEVEL_ORDER


# ---------------------------------------------------------------------------
# Path safety
# ---------------------------------------------------------------------------

def resolve_safe(raw: str) -> Path:
    """
    Resolve *raw* to an absolute path and verify it is inside EXTERNAL_DIR.
    Raises SystemExit on any traversal or symlink escape.
    """
    target = Path(raw).resolve()
    try:
        target.relative_to(EXTERNAL_DIR.resolve())
    except ValueError:
        _die(f"Path '{raw}' is outside allowed directory '{EXTERNAL_DIR}'.\n"
             f"Only files under external_skills/ may be analysed.")
    if target.is_symlink():
        _die(f"Symlinks are not allowed: '{raw}'")
    return target


def _die(msg: str) -> None:
    print(f"\n[ERROR] {msg}")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Summary extractor (no LLM)
# ---------------------------------------------------------------------------

def extract_summary(content: str) -> str:
    """
    Return a short summary by:
      1. Reading the value of a 'description:' frontmatter key, OR
      2. Taking the first H1 heading + up to 3 non-empty lines after it.
    Max ~150 words.
    """
    # Try frontmatter description field
    fm_match = re.search(r'^description:\s*(.+)', content, re.MULTILINE)
    if fm_match:
        return fm_match.group(1).strip()[:400]

    # Fallback: first H1 + following lines
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
        return " ".join(summary_lines)[:400]

    return "(no summary available)"


# ---------------------------------------------------------------------------
# Slug
# ---------------------------------------------------------------------------

def slugify(name: str) -> str:
    """Convert a filename stem to a safe lowercase slug."""
    slug = re.sub(r"[^\w\s-]", "", name).strip().lower()
    slug = re.sub(r"[\s_]+", "_", slug)
    return slug


# ---------------------------------------------------------------------------
# Audit reporting
# ---------------------------------------------------------------------------

def print_audit_report(filepath: Path, result: dict) -> None:
    max_risk = result["max_risk"]
    findings = result["findings"]

    risk_label = {
        "P0": "[P0 HARD FAIL]",
        "P1": "[P1 HARD FAIL]",
        "P2": "[P2 WARNING]",
        None: "[CLEAN]",
    }[max_risk]

    print(f"\n{'='*60}")
    print(f"File    : {filepath.relative_to(PROJECT_ROOT)}")
    print(f"Result  : {risk_label}")

    if findings:
        print(f"Findings ({len(findings)}):")
        for f in findings:
            print(f"  {f['level']:2s}  keyword='{f['keyword']}'")
            if f["snippet"]:
                print(f"        snippet: {f['snippet']}")
    else:
        print("No audit issues found.")
    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# INDEX.json helpers
# ---------------------------------------------------------------------------

def load_index() -> list[dict]:
    if INDEX_PATH.exists():
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []
    return []


def save_index(entries: list[dict]) -> None:
    """Atomic write: write to temp file then replace."""
    APPROVED_DIR.mkdir(parents=True, exist_ok=True)
    tmp = INDEX_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    os.replace(tmp, INDEX_PATH)


def upsert_index(entry: dict) -> None:
    entries = load_index()
    # Replace existing entry for the same path
    entries = [e for e in entries if e.get("path") != entry["path"]]
    entries.append(entry)
    save_index(entries)


# ---------------------------------------------------------------------------
# rejected.log helper
# ---------------------------------------------------------------------------

def log_rejection(source_path: Path, findings: list[dict]) -> None:
    APPROVED_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    reasons = "; ".join(f"{f['level']}:'{f['keyword']}'" for f in findings
                        if _LEVEL_ORDER.get(f["level"], 99) <= 1)
    line = f"[{ts}] REJECTED {source_path.relative_to(PROJECT_ROOT)} | {reasons}\n"
    with open(REJECTED_LOG, "a", encoding="utf-8") as fh:
        fh.write(line)
    print(f"\n[REJECTED] Logged to {REJECTED_LOG.relative_to(PROJECT_ROOT)}")


# ---------------------------------------------------------------------------
# Provenance header
# ---------------------------------------------------------------------------

def build_provenance_header(source_path: Path, risk_level: str,
                            warnings: list[str]) -> str:
    rel = str(source_path.relative_to(PROJECT_ROOT)).replace("\\", "/")
    warn_yaml = json.dumps(warnings)
    return (
        f"---\n"
        f"source_path: {rel}\n"
        f"imported_at: {date.today().isoformat()}\n"
        f"risk_level: {risk_level}\n"
        f"warnings: {warn_yaml}\n"
        f"---\n"
        f"<!-- Original external skill content below -->\n"
    )


# ---------------------------------------------------------------------------
# Strip existing frontmatter from original content
# ---------------------------------------------------------------------------

def strip_frontmatter(content: str) -> str:
    """Remove leading --- ... --- block if present."""
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            return content[end + 4:].lstrip("\n")
    return content


# ---------------------------------------------------------------------------
# Core actions
# ---------------------------------------------------------------------------

def do_query(keyword: str, limit: int = 5) -> None:
    """Search external_skills/ for files matching keyword (name or content)."""
    if not EXTERNAL_DIR.exists():
        _die(f"'{EXTERNAL_DIR.relative_to(PROJECT_ROOT)}' directory not found.\n"
             "Create it and place external skill .md files inside.")

    keyword_lower = keyword.lower()
    matches = []
    for md in sorted(EXTERNAL_DIR.rglob("*.md")):
        if md.is_symlink():
            continue
        try:
            content = md.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        score = 0
        if keyword_lower in md.name.lower():
            score += 10

        for line in content.splitlines():
            if line.startswith("#") and keyword_lower in line.lower():
                score += 5
                break

        if keyword_lower in content.lower():
            score += 1

        if score > 0:
            matches.append((score, md, content))

    if not matches:
        print(f"\nNo files found matching '{keyword}' under {EXTERNAL_DIR.relative_to(PROJECT_ROOT)}/")
        return

    matches.sort(key=lambda x: (-x[0], x[1].name))
    total_found = len(matches)
    matches = matches[:limit]

    print(f"\nFound {total_found} file(s) matching '{keyword}'. Showing top {len(matches)}:\n")
    for score, md, content in matches:
        result = audit_text(content)
        print_audit_report(md, result)
        summary = extract_summary(content)
        print(f"Summary : {summary}\n")


def do_analyse(filepath: Path) -> dict:
    """Audit a single file and print results. Returns audit result dict."""
    if not filepath.exists():
        _die(f"File not found: '{filepath}'")
    if not filepath.suffix.lower() == ".md":
        _die(f"Only .md files are supported: '{filepath}'")

    content = filepath.read_text(encoding="utf-8", errors="replace")
    result  = audit_text(content)
    print_audit_report(filepath, result)
    summary = extract_summary(content)
    print(f"Summary : {summary}")
    return result


def do_import(filepath: Path, result: dict) -> None:
    """
    Import filepath into .agents/external_approved/skills/ if audit passes.
    P0/P1 → hard reject + log. P2 → warning, proceed.
    """
    max_risk = result["max_risk"]
    findings = result["findings"]

    # Hard fail
    hard_fail_findings = [f for f in findings if _LEVEL_ORDER.get(f["level"], 99) <= 1]
    if hard_fail_findings:
        print(f"\n[IMPORT BLOCKED] {filepath.name} has P0/P1 findings. Import refused.")
        log_rejection(filepath, hard_fail_findings)
        return

    # P2 warnings — proceed with annotation
    p2_warnings = [f["keyword"] for f in findings if f["level"] == "P2"]
    risk_level  = "Low" if not p2_warnings else "Medium"

    # Read original, strip its frontmatter, prepend provenance header
    original = filepath.read_text(encoding="utf-8", errors="replace")
    body = strip_frontmatter(original)
    header = build_provenance_header(filepath, risk_level, p2_warnings)
    final_content = header + body

    # Destination
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    slug = slugify(filepath.stem) + ".md"
    dest = SKILLS_DIR / slug

    # Collision: append timestamp
    if dest.exists():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = SKILLS_DIR / f"{slugify(filepath.stem)}_{ts}.md"

    dest.write_text(final_content, encoding="utf-8")
    print(f"\n[IMPORTED] {filepath.relative_to(PROJECT_ROOT)} -> {dest.relative_to(PROJECT_ROOT)}")

    # Update INDEX.json
    summary = extract_summary(body)
    title_match = re.search(r'^#\s+(.+)', body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filepath.stem

    entry = {
        "title":       title,
        "summary":     summary[:300],
        "path":        str(dest.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "source_path": str(filepath.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "risk_level":  risk_level,
        "warnings":    p2_warnings,
        "imported_at": date.today().isoformat(),
    }
    upsert_index(entry)
    print(f"[INDEX]    INDEX.json updated.")

    if p2_warnings:
        print(f"[WARNING]  P2 keywords detected: {p2_warnings}")
        print("           Review the imported file before use in production tasks.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    # Ensure stdout handles Unicode properly on Windows
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(
        description="External skill quarantine gate. Dry-run by default."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--query", metavar="KEYWORD",
        help="Search external_skills/ for files matching keyword (dry-run)."
    )
    group.add_argument(
        "--file", metavar="PATH",
        help="Audit a single .md file inside external_skills/."
    )
    parser.add_argument(
        "--import-approved", action="store_true",
        help="After audit, import the file if it passes (P0/P1 free). "
             "Has no effect without --file. P0/P1 always hard-blocked."
    )
    parser.add_argument(
        "--limit", type=int, default=5,
        help="Maximum number of query results to display (default: 5)."
    )
    args = parser.parse_args()

    if args.query:
        do_query(args.query, args.limit)
        return

    # --file path
    safe_path = resolve_safe(args.file)
    result    = do_analyse(safe_path)

    if args.import_approved:
        do_import(safe_path, result)
    else:
        print("\n[DRY-RUN] Pass --import-approved to copy this file into "
              ".agents/external_approved/skills/")


if __name__ == "__main__":
    main()
