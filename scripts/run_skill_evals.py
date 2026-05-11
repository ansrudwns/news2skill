"""
run_skill_evals.py - evaluate external-approved skill selection.

This is a deterministic baseline for the pull-based skill store. It ranks
entries from .agents/external_approved/INDEX.json against prompts in
.agents/evals/tasks.json and reports top-k retrieval quality.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INDEX = PROJECT_ROOT / ".agents" / "external_approved" / "INDEX.json"
DEFAULT_TASKS = PROJECT_ROOT / ".agents" / "evals" / "tasks.json"

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "before",
    "by",
    "current",
    "directory",
    "file",
    "files",
    "for",
    "from",
    "git",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "json",
    "list",
    "me",
    "of",
    "on",
    "or",
    "object",
    "pretty",
    "print",
    "repository",
    "so",
    "show",
    "small",
    "status",
    "that",
    "the",
    "this",
    "tell",
    "to",
    "using",
    "valid",
    "with",
}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"[ERROR] Could not parse {path}: {exc}") from exc


def skill_id(entry: dict[str, Any]) -> str:
    raw = entry.get("id") or entry.get("name") or Path(str(entry.get("path", ""))).stem or entry.get("title")
    return normalize_id(str(raw))


def normalize_id(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^\w\s/-]", "", value)
    value = re.sub(r"[\s_]+", "-", value)
    return value.strip("-/")


def tokens(text: str) -> list[str]:
    raw_tokens = re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]{1,}", text.lower())
    expanded: list[str] = []
    for token in raw_tokens:
        if token not in STOP_WORDS:
            expanded.append(token)
        for part in re.split(r"[-_]", token):
            if len(part) > 1 and part not in STOP_WORDS:
                expanded.append(part)
    return expanded


def vectorize(text: str) -> Counter[str]:
    return Counter(tokens(text))


def cosine(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    overlap = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in overlap)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def skill_text(entry: dict[str, Any]) -> str:
    fields = [
        str(entry.get("id", "")),
        str(entry.get("name", "")),
        str(entry.get("title", "")),
        str(entry.get("description", "")),
        str(entry.get("summary", "")),
        str(entry.get("source", "")),
    ]
    return " ".join(field for field in fields if field)


def rank_skills(prompt: str, skills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prompt_vec = vectorize(prompt)
    ranked = []
    for entry in skills:
        sid = skill_id(entry)
        score = cosine(prompt_vec, vectorize(skill_text(entry)))
        if sid in prompt.lower():
            score += 0.25
        ranked.append({
            "id": sid,
            "path": entry.get("path", ""),
            "score": round(score, 6),
        })
    ranked.sort(key=lambda item: (-item["score"], item["id"]))
    return ranked


def evaluate(
    tasks: list[dict[str, Any]],
    skills: list[dict[str, Any]],
    top_k: int,
    abstain_threshold: float,
) -> dict[str, Any]:
    results = []
    top1_hits = 0
    topk_hits = 0
    all_expected_hits = 0
    abstain_hits = 0
    positive_total = 0
    negative_total = 0

    for task in tasks:
        expected = [normalize_id(item) for item in task.get("expected_skills", [])]
        ranked = rank_skills(str(task.get("prompt", "")), skills)
        top1_score = ranked[0]["score"] if ranked else 0.0
        should_abstain = top1_score < abstain_threshold
        selected = [] if should_abstain else ranked[:top_k]
        selected_ids = [item["id"] for item in selected]

        hit_ids = [item for item in expected if item in selected_ids]
        is_negative = not expected
        positive_total += int(not is_negative)
        negative_total += int(is_negative)

        top1_hit = bool(expected and ranked and not should_abstain and ranked[0]["id"] in expected)
        topk_hit = bool(hit_ids)
        all_hit = bool(expected) and all(item in selected_ids for item in expected)
        abstain_hit = bool(is_negative and should_abstain)

        top1_hits += int(top1_hit)
        topk_hits += int(topk_hit)
        all_expected_hits += int(all_hit)
        abstain_hits += int(abstain_hit)

        results.append({
            "id": task.get("id", ""),
            "category": task.get("category", ""),
            "expected": expected,
            "top1": ranked[0] if ranked else None,
            "selected": selected,
            "abstained": should_abstain,
            "top1Hit": top1_hit,
            "topKHit": topk_hit,
            "allExpectedHit": all_hit,
            "abstainHit": abstain_hit,
            "missingExpected": [item for item in expected if item not in selected_ids],
        })

    total = len(tasks)
    summary = {
        "tasks": total,
        "positiveTasks": positive_total,
        "negativeTasks": negative_total,
        "topK": top_k,
        "abstainThreshold": abstain_threshold,
        "top1Accuracy": round(top1_hits / positive_total, 4) if positive_total else 0.0,
        "topKRecall": round(topk_hits / positive_total, 4) if positive_total else 0.0,
        "allExpectedRecall": round(all_expected_hits / positive_total, 4) if positive_total else 0.0,
        "negativeAbstainAccuracy": round(abstain_hits / negative_total, 4) if negative_total else 0.0,
    }
    return {"summary": summary, "results": results}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate external-approved skill retrieval quality.")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX, help="Path to external approved INDEX.json.")
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS, help="Path to eval tasks JSON.")
    parser.add_argument("--top-k", type=int, default=3, help="Number of recommended skills to score per task.")
    parser.add_argument(
        "--abstain-threshold",
        type=float,
        default=0.10,
        help="Do not recommend a skill when the top score is below this threshold.",
    )
    parser.add_argument("--json", action="store_true", help="Print full JSON results.")
    parser.add_argument("--fail-under-top1", type=float, help="Fail if top-1 accuracy is below this threshold.")
    parser.add_argument("--fail-under-topk", type=float, help="Fail if top-k recall is below this threshold.")
    parser.add_argument("--fail-under-abstain", type=float, help="Fail if negative abstain accuracy is below this threshold.")
    return parser.parse_args()


def print_report(report: dict[str, Any]) -> None:
    summary = report["summary"]
    print("Skill eval baseline")
    print(f"Tasks: {summary['tasks']}")
    print(f"Positive tasks: {summary['positiveTasks']}")
    print(f"Negative tasks: {summary['negativeTasks']}")
    print(f"Top-k: {summary['topK']}")
    print(f"Abstain threshold: {summary['abstainThreshold']:.3f}")
    print(f"Top-1 accuracy: {summary['top1Accuracy']:.2%}")
    print(f"Top-k recall: {summary['topKRecall']:.2%}")
    print(f"All-expected recall: {summary['allExpectedRecall']:.2%}")
    print(f"Negative abstain accuracy: {summary['negativeAbstainAccuracy']:.2%}")
    print()
    for result in report["results"]:
        top1 = result["top1"] or {"id": "-", "score": 0}
        is_negative = not result["expected"]
        if is_negative:
            marker = "PASS" if result["abstainHit"] else "MISS"
        else:
            marker = "PASS" if result["topKHit"] else "MISS"
        expected = ", ".join(result["expected"]) if result["expected"] else "none"
        abstained = " abstained" if result["abstained"] else ""
        print(f"{marker} {result['id']}: top1={top1['id']} ({top1['score']:.3f}) expected=[{expected}]{abstained}")
        if result["missingExpected"]:
            print(f"  missing: {', '.join(result['missingExpected'])}")


def main() -> int:
    args = parse_args()
    if args.top_k <= 0:
        print("[ERROR] --top-k must be positive.", file=sys.stderr)
        return 1

    skills = load_json(args.index)
    tasks = load_json(args.tasks)
    if not isinstance(skills, list) or not isinstance(tasks, list):
        print("[ERROR] Index and tasks files must both contain JSON arrays.", file=sys.stderr)
        return 1

    report = evaluate(tasks, skills, args.top_k, args.abstain_threshold)
    if args.json:
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print_report(report)

    summary = report["summary"]
    if args.fail_under_top1 is not None and summary["top1Accuracy"] < args.fail_under_top1:
        return 2
    if args.fail_under_topk is not None and summary["topKRecall"] < args.fail_under_topk:
        return 2
    if args.fail_under_abstain is not None and summary["negativeAbstainAccuracy"] < args.fail_under_abstain:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
