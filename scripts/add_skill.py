"""
add_skill.py - safely register a skill in skills-lock.json.

Usage:
  python scripts/add_skill.py external_skills/open-design/skills/dashboard/SKILL.md
  python scripts/add_skill.py custom_skills/frontend-ui-design/foo.md --name frontend/foo
  python scripts/add_skill.py custom_skills/frontend-ui-design/foo.md --force

The semantic collision check is intentionally dependency-free. It combines
trigger overlap and token Jaccard similarity over the skill name, description,
and trigger text.
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOCK_PATH = PROJECT_ROOT / "skills-lock.json"
DEFAULT_THRESHOLD = 0.30


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "if",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "use",
    "when",
    "with",
    "you",
    "your",
}


def die(message: str, code: int = 1) -> None:
    print(f"[ERROR] {message}", file=sys.stderr)
    sys.exit(code)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\s/-]", "", value)
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-/")


def resolve_skill_path(raw_path: str) -> Path:
    raw = Path(raw_path)
    candidates = []
    if raw.is_absolute():
        candidates.append(raw)
    else:
        candidates.append((Path.cwd() / raw))
        candidates.append((PROJECT_ROOT / raw))

    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.exists():
            if not resolved.is_file():
                die(f"Target is not a file: {raw_path}")
            if resolved.suffix.lower() != ".md":
                die(f"Target must be a Markdown file: {raw_path}")
            return resolved

    die(f"Target file not found: {raw_path}")


def relative_to_project(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        die(f"Target must be inside project root: {PROJECT_ROOT}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_scalar(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {"'", '"'}:
        return raw[1:-1]
    return raw


def extract_frontmatter(content: str) -> dict[str, Any]:
    if not content.startswith("---"):
        return {}

    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", content, re.DOTALL)
    if not match:
        return {}

    lines = match.group(1).splitlines()
    data: dict[str, Any] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#") or line.startswith((" ", "\t")):
            i += 1
            continue

        key_match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not key_match:
            i += 1
            continue

        key = key_match.group(1)
        value = key_match.group(2).strip()

        if value in {"|", ">"}:
            block: list[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
                block.append(lines[i].strip())
                i += 1
            data[key] = "\n".join(block).strip()
            continue

        if value:
            if value.startswith("[") and value.endswith("]"):
                items = [parse_scalar(part) for part in value[1:-1].split(",") if part.strip()]
                data[key] = items
            else:
                data[key] = parse_scalar(value)
            i += 1
            continue

        values: list[str] = []
        i += 1
        while i < len(lines) and (lines[i].startswith((" ", "\t")) or not lines[i].strip()):
            item = lines[i].strip()
            if item.startswith("- "):
                values.append(parse_scalar(item[2:]))
            i += 1
        data[key] = values

    return data


def extract_fallback_summary(content: str) -> tuple[str, str]:
    lines = content.splitlines()
    title = ""
    summary: list[str] = []
    capturing = False

    for line in lines:
        if line.startswith("# ") and not title:
            title = line.lstrip("# ").strip()
            capturing = True
            continue
        if capturing:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                summary.append(stripped)
            if len(summary) >= 3:
                break

    return title, " ".join(summary)[:600]


def extract_skill_info(path: Path) -> dict[str, Any]:
    content = read_text(path)
    frontmatter = extract_frontmatter(content)
    fallback_name, fallback_description = extract_fallback_summary(content)

    raw_triggers = frontmatter.get("triggers", [])
    if isinstance(raw_triggers, str):
        triggers = [raw_triggers]
    elif isinstance(raw_triggers, list):
        triggers = [str(item) for item in raw_triggers if str(item).strip()]
    else:
        triggers = []

    name = str(frontmatter.get("name") or fallback_name or path.stem).strip()
    description = str(frontmatter.get("description") or fallback_description).strip()

    return {
        "name": name,
        "description": description,
        "triggers": triggers,
        "content": content,
    }


def tokenize(text: str) -> set[str]:
    tokens = {
        token
        for token in re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]{1,}", text.lower())
        if token not in STOP_WORDS
    }
    expanded: set[str] = set()
    for token in tokens:
        expanded.add(token)
        expanded.update(part for part in re.split(r"[-_]", token) if len(part) > 1 and part not in STOP_WORDS)
    return expanded


def semantic_text(info: dict[str, Any]) -> str:
    return " ".join([info.get("name", ""), info.get("description", ""), " ".join(info.get("triggers", []))])


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def trigger_similarity(left: list[str], right: list[str]) -> tuple[float, list[str]]:
    left_set = {trigger.strip().lower() for trigger in left if trigger.strip()}
    right_set = {trigger.strip().lower() for trigger in right if trigger.strip()}
    if not left_set or not right_set:
        return 0.0, []
    overlap = sorted(left_set & right_set)
    return len(overlap) / min(len(left_set), len(right_set)), overlap


def collision_score(new_info: dict[str, Any], existing_info: dict[str, Any]) -> dict[str, Any]:
    token_score = jaccard(tokenize(semantic_text(new_info)), tokenize(semantic_text(existing_info)))
    trigger_score, trigger_overlap = trigger_similarity(new_info["triggers"], existing_info["triggers"])
    score = max(token_score, trigger_score)
    return {
        "score": score,
        "tokenScore": token_score,
        "triggerScore": trigger_score,
        "triggerOverlap": trigger_overlap,
    }


def load_lock() -> dict[str, Any]:
    if not LOCK_PATH.exists():
        die(f"Registry not found: {LOCK_PATH}")
    try:
        data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"Could not parse skills-lock.json: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("skills"), dict):
        die("skills-lock.json must contain an object with a 'skills' object.")
    return data


def save_lock(data: dict[str, Any]) -> None:
    tmp = LOCK_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, LOCK_PATH)


def infer_name(path: Path, info: dict[str, Any]) -> str:
    rel = path.resolve().relative_to(PROJECT_ROOT)
    parts = rel.parts
    stem = path.parent.name if path.name.lower() == "skill.md" else path.stem

    if len(parts) >= 4 and parts[0] == "external_skills":
        provider = slugify(parts[1])
        return f"{provider}/{slugify(stem)}"

    if len(parts) >= 3 and parts[0] == "custom_skills":
        namespace = slugify(parts[1])
        if namespace == "frontend-ui-design":
            namespace = "frontend"
        return f"{namespace}/{slugify(stem)}"

    if info.get("name"):
        return slugify(str(info["name"]))
    return slugify(stem)


def infer_source(path: Path, explicit_source: str | None) -> tuple[str, str]:
    if explicit_source:
        source_type = "github" if "/" in explicit_source and not explicit_source.startswith("local/") else "local"
        return explicit_source, source_type

    rel = path.resolve().relative_to(PROJECT_ROOT)
    parts = rel.parts
    if parts and parts[0] == "custom_skills":
        return "local/custom_skills", "local"
    if len(parts) >= 2 and parts[0] == "external_skills":
        provider = parts[1]
        if provider == "open-design":
            return "nexu-io/open-design", "github"
        return f"external/{provider}", "external"
    return "local", "local"


def find_collisions(
    new_name: str,
    new_path: str,
    new_hash: str,
    new_info: dict[str, Any],
    registry: dict[str, Any],
    threshold: float,
) -> tuple[list[str], list[dict[str, Any]]]:
    duplicates: list[str] = []
    collisions: list[dict[str, Any]] = []

    if new_name in registry:
        duplicates.append(f"Skill name already exists: {new_name}")

    for existing_name, entry in registry.items():
        existing_path = str(entry.get("skillPath", ""))
        existing_hash = str(entry.get("computedHash", "")).strip()
        if existing_path == new_path:
            duplicates.append(f"Skill path already registered as '{existing_name}': {new_path}")
        if existing_hash and existing_hash == new_hash:
            duplicates.append(f"Skill content hash already registered as '{existing_name}'.")

        full_existing_path = PROJECT_ROOT / existing_path
        if not full_existing_path.exists() or not full_existing_path.is_file():
            continue

        existing_info = extract_skill_info(full_existing_path)
        result = collision_score(new_info, existing_info)
        if result["score"] >= threshold:
            collisions.append({
                "name": existing_name,
                "path": existing_path,
                **result,
            })

    collisions.sort(key=lambda item: item["score"], reverse=True)
    return duplicates, collisions


def print_collisions(collisions: list[dict[str, Any]], threshold: float) -> None:
    print(f"\nSemantic collision candidates (threshold: {threshold:.2f}):")
    for item in collisions:
        overlap = ", ".join(item["triggerOverlap"]) if item["triggerOverlap"] else "-"
        print(
            f"  - {item['name']} ({item['score']:.2f})\n"
            f"    path: {item['path']}\n"
            f"    token={item['tokenScore']:.2f}, trigger={item['triggerScore']:.2f}, overlap={overlap}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Register a skill in skills-lock.json with semantic collision checks.")
    parser.add_argument("skill_file", help="Path to the target .md skill file.")
    parser.add_argument("--name", help="Registry namespace/name. If omitted, inferred from path.")
    parser.add_argument("--source", help="Override source field, e.g. nexu-io/open-design or local/custom_skills.")
    parser.add_argument("--source-type", choices=["github", "local", "external"], help="Override sourceType field.")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="Collision threshold, default: 0.30.")
    parser.add_argument("--force", action="store_true", help="Register even when semantic collisions are found.")
    parser.add_argument("--dry-run", action="store_true", help="Run checks and print the proposed entry without writing.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = resolve_skill_path(args.skill_file)
    rel_path = relative_to_project(target)
    info = extract_skill_info(target)
    skill_name = slugify(args.name) if args.name else infer_name(target, info)
    skill_hash = sha256_file(target)

    lock_data = load_lock()
    registry = lock_data["skills"]

    source, inferred_source_type = infer_source(target, args.source)
    source_type = args.source_type or inferred_source_type

    duplicates, collisions = find_collisions(
        skill_name,
        rel_path,
        skill_hash,
        info,
        registry,
        args.threshold,
    )

    if duplicates:
        print("\nDuplicate registration blocked:")
        for duplicate in sorted(set(duplicates)):
            print(f"  - {duplicate}")
        return 1

    if collisions:
        print_collisions(collisions, args.threshold)
        if not args.force:
            print("\nRegistration rejected. Adjust triggers/description, merge the skills, or rerun with --force.")
            return 2
        print("\n--force supplied; semantic collision warning bypassed.")

    entry = {
        "source": source,
        "sourceType": source_type,
        "skillPath": rel_path,
        "computedHash": skill_hash,
    }

    print("\nProposed registry entry:")
    print(json.dumps({skill_name: entry}, ensure_ascii=False, indent=2))

    if args.dry_run:
        print("\nDry run complete. No changes written.")
        return 0

    registry[skill_name] = entry
    save_lock(lock_data)
    print(f"\nRegistered '{skill_name}' in {LOCK_PATH.relative_to(PROJECT_ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
