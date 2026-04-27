"""
audit_index.py — AGENTS.md ↔ Filesystem ↔ Provenance 3-way Consistency Checker

Runs READ-ONLY. Does not modify anything.
"""

import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGENTS_FILE = PROJECT_ROOT / "AGENTS.md"
AGENTS_DIR = PROJECT_ROOT / ".agents"

PLACEHOLDER_DESCRIPTIONS = {
    "Legacy migrated asset.",
    "No description provided.",
    "",
}

SIGNED_TRACKS = {
    "skills":   AGENTS_DIR / "skills",
    "diaries":  AGENTS_DIR / "diaries",
    "backlog":  AGENTS_DIR / "backlog",
    "archives": AGENTS_DIR / "archives",
}

UNSIGNED_TRACKS = {
    "reports":          AGENTS_DIR / "reports",
    "staging":          AGENTS_DIR / "staging",
    "research_proposals": AGENTS_DIR / "backlog" / "research_proposals",
    "external_approved": AGENTS_DIR / "external_approved" / "skills",
}

_AGENTS_ENTRY_RE = re.compile(
    r"^\s*[-*]\s+\*\*([^*]+?)\*\*:\s*(.+?)\s*\(Path:\s*`([^`]+)`\)\s*$",
    re.MULTILINE,
)
_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_DESCRIPTION_RE = re.compile(r"^\s*description:\s*[\"']?(.+?)[\"']?\s*$", re.MULTILINE)


def parse_agents_index():
    if not AGENTS_FILE.exists():
        return []
    text = AGENTS_FILE.read_text(encoding="utf-8")
    out = []
    for m in _AGENTS_ENTRY_RE.finditer(text):
        name, desc, path = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        desc = desc.strip('"').strip("'")
        out.append({"name": name, "description": desc, "path": path})
    return out


def extract_frontmatter_description(file_path):
    if not file_path.exists() or not file_path.is_file():
        return None
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return None
    fm = _FRONTMATTER_RE.match(text)
    if not fm:
        return None
    desc_match = _DESCRIPTION_RE.search(fm.group(1))
    if not desc_match:
        return None
    return desc_match.group(1).strip()


def check_dead_links(entries):
    issues = []
    for e in entries:
        rel = e["path"].replace("\\", "/").rstrip("/")
        target = PROJECT_ROOT / rel
        if not target.exists():
            issues.append({"type": "dead_link", "name": e["name"], "path": e["path"],
                           "detail": "AGENTS.md cites a path that does not exist on disk."})
    return issues


def check_path_name_mismatch(entries):
    issues = []
    for e in entries:
        rel = e["path"].replace("\\", "/").rstrip("/")
        target = PROJECT_ROOT / rel
        if not target.exists() or target.is_dir():
            continue
        stem = target.stem
        if stem != e["name"]:
            issues.append({"type": "name_path_mismatch", "name": e["name"], "path": e["path"],
                           "detail": f"Index name '{e['name']}' != filename stem '{stem}'."})
    return issues


def check_orphans(entries):
    indexed_paths = {e["path"].replace("\\", "/").rstrip("/") for e in entries}
    unsigned_dirs = [d for d in UNSIGNED_TRACKS.values() if d.exists()]
    issues = []
    for track_name, track_dir in SIGNED_TRACKS.items():
        if not track_dir.exists():
            continue
        for md in track_dir.rglob("*.md"):
            if any(md.is_relative_to(ud) for ud in unsigned_dirs):
                continue
            rel = md.relative_to(PROJECT_ROOT).as_posix()
            if rel not in indexed_paths:
                issues.append({"type": "orphan", "track": track_name, "path": rel,
                               "detail": "File exists but is not registered in AGENTS.md."})
    return issues


def check_provenance(entries):
    issues = []
    for e in entries:
        rel = e["path"].replace("\\", "/").rstrip("/")
        target = PROJECT_ROOT / rel
        if not target.exists() or target.is_dir():
            continue
        if not any(target.is_relative_to(td) for td in SIGNED_TRACKS.values()):
            continue
        intoto = target.with_suffix(target.suffix + ".intoto.json")
        legacy = target.with_suffix(target.suffix + ".sig")
        if legacy.exists():
            issues.append({"type": "legacy_sig", "name": e["name"], "path": rel,
                           "detail": "Legacy .sig sidecar present."})
        if not intoto.exists():
            issues.append({"type": "missing_provenance", "name": e["name"], "path": rel,
                           "detail": "No .intoto.json sidecar found."})
    return issues


def check_descriptions(entries):
    issues = []
    for e in entries:
        rel = e["path"].replace("\\", "/").rstrip("/")
        target = PROJECT_ROOT / rel
        if e["description"] in PLACEHOLDER_DESCRIPTIONS:
            issues.append({"type": "placeholder_index_description", "name": e["name"], "path": rel,
                           "detail": f"AGENTS.md description is placeholder: '{e['description']}'."})
        if target.exists() and target.is_file():
            fm_desc = extract_frontmatter_description(target)
            if fm_desc is None or fm_desc in PLACEHOLDER_DESCRIPTIONS:
                issues.append({"type": "placeholder_frontmatter", "name": e["name"], "path": rel,
                               "detail": f"Frontmatter description is missing/placeholder: '{fm_desc}'."})
    return issues


def check_lab_collisions():
    lab_dir = AGENTS_DIR / "laboratory"
    if not lab_dir.exists():
        return []
    prefixes = {}
    for child in lab_dir.iterdir():
        if not child.is_dir():
            continue
        m = re.match(r"^(\d+)_", child.name)
        if not m:
            continue
        prefixes.setdefault(m.group(1), []).append(child.name)
    issues = []
    for pref, names in prefixes.items():
        if len(names) > 1:
            issues.append({"type": "lab_prefix_collision", "prefix": pref, "names": sorted(names),
                           "detail": f"{len(names)} laboratory directories share prefix '{pref}_'."})
    return issues


def check_lab_orphans():
    lab_dir = AGENTS_DIR / "laboratory"
    if not lab_dir.exists():
        return []
    issues = []
    for child in lab_dir.iterdir():
        if child.is_file():
            issues.append({"type": "lab_orphan_file", "name": child.name,
                           "path": child.relative_to(PROJECT_ROOT).as_posix(),
                           "detail": "Stray file at laboratory root."})
    return issues


def run_audit():
    entries = parse_agents_index()
    issues = []
    issues += check_dead_links(entries)
    issues += check_path_name_mismatch(entries)
    issues += check_orphans(entries)
    issues += check_provenance(entries)
    issues += check_descriptions(entries)
    issues += check_lab_collisions()
    issues += check_lab_orphans()
    grouped = {}
    for i in issues:
        grouped.setdefault(i["type"], []).append(i)
    return {"total_entries": len(entries), "total_issues": len(issues), "by_type": grouped}


def print_report(report, quiet_clean):
    n = report["total_issues"]
    total = report["total_entries"]
    if n == 0:
        if not quiet_clean:
            print(f"[audit_index] OK -- {total} indexed entries, 0 drift detected.")
        return
    print(f"[audit_index] {n} drift items detected across {total} indexed entries.\n")
    for issue_type, items in report["by_type"].items():
        print(f"## {issue_type}  ({len(items)} item{'s' if len(items)!=1 else ''})")
        for it in items:
            label = it.get("name") or it.get("path") or it.get("prefix", "?")
            detail = it.get("detail", "")
            print(f"  - {label}: {detail}")
        print()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--quiet-clean", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    report = run_audit()
    if args.json:
        flat = [it for items in report["by_type"].values() for it in items]
        json.dump({"summary": {"total_entries": report["total_entries"],
                               "total_issues": report["total_issues"]},
                   "issues": flat}, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print_report(report, quiet_clean=args.quiet_clean)
    return 1 if report["total_issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
