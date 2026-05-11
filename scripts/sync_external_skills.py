"""
sync_external_skills.py - bulk-register safe external skills.

The script scans external_skills/**/SKILL.md, compares discovered files with
skills-lock.json, and reuses add_skill.py's single-skill extraction, hashing,
source inference, namespace inference, and collision checks. It dry-runs by
default and only updates skills-lock.json when --write is supplied.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from add_skill import (  # noqa: E402
    DEFAULT_THRESHOLD,
    LOCK_PATH,
    PROJECT_ROOT,
    extract_skill_info,
    find_collisions,
    infer_name,
    infer_source,
    load_lock,
    relative_to_project,
    save_lock,
    sha256_file,
)


EXTERNAL_DIR = PROJECT_ROOT / "external_skills"
DEFAULT_REPORT = PROJECT_ROOT / "scratch" / "external-skill-sync-report.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Safely bulk-register unlinked external skills in skills-lock.json."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Preview changes without updating the registry.")
    mode.add_argument("--write", action="store_true", help="Write safe candidates to skills-lock.json.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow semantic collisions, while still blocking exact name/path/hash duplicates.",
    )
    parser.add_argument("--provider", help="Only scan external_skills/<provider>.")
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f"Semantic collision threshold, default: {DEFAULT_THRESHOLD:.2f}.",
    )
    parser.add_argument(
        "--report",
        default=str(DEFAULT_REPORT.relative_to(PROJECT_ROOT)),
        help="JSON report path, default: scratch/external-skill-sync-report.json.",
    )
    parser.add_argument("--limit", type=int, help="Process at most N unregistered candidates.")
    parser.add_argument(
        "--fail-on-blocked",
        action="store_true",
        help="Exit with code 2 when any duplicate or collision is blocked.",
    )
    return parser.parse_args()


def normalize_lock_path(path: str) -> str:
    return path.replace("\\", "/")


def build_registered_path_set(registry: dict[str, Any]) -> set[str]:
    return {
        normalize_lock_path(str(entry.get("skillPath", "")))
        for entry in registry.values()
        if isinstance(entry, dict) and entry.get("skillPath")
    }


def ensure_inside_external(path: Path) -> bool:
    try:
        path.resolve().relative_to(EXTERNAL_DIR.resolve())
    except ValueError:
        return False
    return True


def discover_skill_files(provider: str | None) -> list[Path]:
    if not EXTERNAL_DIR.exists() or not EXTERNAL_DIR.is_dir():
        raise FileNotFoundError(f"External skills directory not found: {EXTERNAL_DIR}")

    scan_root = EXTERNAL_DIR / provider if provider else EXTERNAL_DIR
    if not scan_root.exists() or not scan_root.is_dir():
        raise FileNotFoundError(f"External skills provider not found: {scan_root}")

    files: list[Path] = []
    for path in scan_root.rglob("*"):
        if path.name.lower() != "skill.md" or not path.is_file():
            continue
        if path.is_symlink() and not ensure_inside_external(path):
            continue
        if not ensure_inside_external(path):
            continue
        files.append(path.resolve())
    return sorted(files, key=lambda item: relative_to_project(item).lower())


def make_entry(path: Path, source: str, source_type: str, computed_hash: str) -> dict[str, str]:
    return {
        "source": source,
        "sourceType": source_type,
        "skillPath": relative_to_project(path),
        "computedHash": computed_hash,
    }


def resolve_report_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def save_report(report: dict[str, Any], report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = report_path.with_suffix(report_path.suffix + ".tmp")
    tmp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, report_path)


def unique_messages(messages: list[str]) -> list[str]:
    return sorted(set(messages))


def process_already_registered(path: Path, registry: dict[str, Any]) -> dict[str, Any]:
    rel_path = relative_to_project(path)
    matched_name = ""
    matched_entry: dict[str, Any] = {}
    for name, entry in registry.items():
        if normalize_lock_path(str(entry.get("skillPath", ""))) == rel_path:
            matched_name = name
            matched_entry = entry
            break

    return {
        "status": "already_registered",
        "name": matched_name,
        "skillPath": rel_path,
        "source": matched_entry.get("source", ""),
        "sourceType": matched_entry.get("sourceType", ""),
        "computedHash": matched_entry.get("computedHash", ""),
        "duplicates": [],
        "collisions": [],
    }


def process_candidate(
    path: Path,
    registry: dict[str, Any],
    threshold: float,
    force: bool,
    write_mode: bool,
) -> dict[str, Any]:
    info = extract_skill_info(path)
    name = infer_name(path, info)
    computed_hash = sha256_file(path)
    source, source_type = infer_source(path, None)
    entry = make_entry(path, source, source_type, computed_hash)

    duplicates, collisions = find_collisions(
        name,
        entry["skillPath"],
        computed_hash,
        info,
        registry,
        threshold,
    )

    status: str
    can_register = False
    if duplicates:
        status = "blocked_duplicate"
    elif collisions and not force:
        status = "blocked_collision"
    elif collisions and force:
        status = "registered_forced" if write_mode else "would_register_forced"
        can_register = True
    else:
        status = "registered" if write_mode else "would_register"
        can_register = True

    item = {
        "status": status,
        "name": name,
        "skillPath": entry["skillPath"],
        "source": source,
        "sourceType": source_type,
        "computedHash": computed_hash,
        "duplicates": unique_messages(duplicates),
        "collisions": collisions,
    }

    if can_register:
        registry[name] = entry

    return item


def count_status(items: list[dict[str, Any]], status: str) -> int:
    return sum(1 for item in items if item["status"] == status)


def summarize(items: list[dict[str, Any]], scanned: int, already_registered: int) -> dict[str, int]:
    return {
        "scanned": scanned,
        "alreadyRegistered": already_registered,
        "candidates": scanned - already_registered,
        "wouldRegister": count_status(items, "would_register"),
        "wouldRegisterForced": count_status(items, "would_register_forced"),
        "registered": count_status(items, "registered"),
        "registeredForced": count_status(items, "registered_forced"),
        "blockedDuplicate": count_status(items, "blocked_duplicate"),
        "blockedCollision": count_status(items, "blocked_collision"),
    }


def build_report(
    mode: str,
    provider: str | None,
    threshold: float,
    items: list[dict[str, Any]],
    scanned: int,
    already_registered: int,
) -> dict[str, Any]:
    summary = summarize(items, scanned, already_registered)
    return {
        "mode": mode,
        "provider": provider,
        "threshold": threshold,
        **summary,
        "items": items,
    }


def print_summary(report: dict[str, Any], report_path: Path) -> None:
    title_mode = "write" if report["mode"] == "write" else "dry-run"
    print(f"External skill sync {title_mode}")
    print(f"Scanned: {report['scanned']}")
    print(f"Already registered: {report['alreadyRegistered']}")
    print(f"Candidates: {report['candidates']}")
    if report["mode"] == "write":
        print(f"Registered: {report['registered']}")
        print(f"Registered with force: {report['registeredForced']}")
    else:
        print(f"Would register: {report['wouldRegister']}")
        print(f"Would register with force: {report['wouldRegisterForced']}")
    print(f"Blocked by duplicate: {report['blockedDuplicate']}")
    print(f"Blocked by collision: {report['blockedCollision']}")
    print(f"Report: {relative_to_project(report_path)}")


def main() -> int:
    args = parse_args()
    write_mode = bool(args.write)
    mode = "write" if write_mode else "dry-run"
    report_path = resolve_report_path(args.report)

    try:
        lock_data = load_lock()
        registry = copy.deepcopy(lock_data["skills"])
        skill_files = discover_skill_files(args.provider)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    registered_paths = build_registered_path_set(registry)
    items: list[dict[str, Any]] = []
    already_registered = 0
    processed_candidates = 0

    try:
        for path in skill_files:
            rel_path = relative_to_project(path)
            if normalize_lock_path(rel_path) in registered_paths:
                already_registered += 1
                items.append(process_already_registered(path, registry))
                continue

            if args.limit is not None and processed_candidates >= args.limit:
                continue

            processed_candidates += 1
            items.append(
                process_candidate(
                    path=path,
                    registry=registry,
                    threshold=args.threshold,
                    force=args.force,
                    write_mode=write_mode,
                )
            )

        scanned = len(skill_files)
        if args.limit is not None:
            scanned = already_registered + processed_candidates

        report = build_report(
            mode=mode,
            provider=args.provider,
            threshold=args.threshold,
            items=items,
            scanned=scanned,
            already_registered=already_registered,
        )

        save_report(report, report_path)

        if write_mode:
            lock_data["skills"] = registry
            save_lock(lock_data)

        print_summary(report, report_path)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    blocked = report["blockedDuplicate"] + report["blockedCollision"]
    if blocked and (write_mode or args.fail_on_blocked):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
