---
description: Six-axis evaluation schema (Trigger / Thresholds / DO-DON'T / Failure Mode / Cross-Skill Edges / Self-Verification) that any new skill draft MUST answer before promotion out of staging.
---
# Architectural Diary: Skill Quality Schema
> Evaluator Score: pending — diary, not yet scored.

## Premise
The 2026-04-25 audit surfaced a pattern: legacy skills in `.agents/skills/` describe **what** they do (mechanism) and **why** they exist (rationale) but rarely encode the operational boundary conditions an executor needs at call-time. A skill that says "use aggressive regex on MCP returns" does not tell the agent *when not to*, *what counts as too aggressive*, or *what the failure looks like when the regex eats a legitimate payload*. This diary defines the minimum schema every new or refactored skill must satisfy before `auto_commit.py` is allowed to promote it from `staging/` into `.agents/skills/`.

## The Six Operational Axes
A skill is "deployable" only if its body answers **all six** of the following. Missing axes are an audit finding (`audit_index.py` extension — see below).

### 1. Trigger (When does this fire?)
A precise condition — not a vibe. Bad: "use this when context is heavy". Good: "engage when prompt token usage > 0.80 of model window, OR when the planner anticipates >180s wall-clock for the remaining plan".

### 2. Thresholds (What numbers govern it?)
Every quantitative knob in the skill must be named and given a default. If the skill says "if overlap is high", it must say *high = 0.8*. Numbers without units are rejected.

### 3. DO / DON'T (Scope boundary)
At least one DO and one DON'T, expressed as imperatives the agent can match against a candidate action. Example for `ClawGuard`:
- DO regex-sanitize MCP/web payloads at the `tool_call` input boundary.
- DON'T regex-parse LLM output (Defensive_Execution_Protocol Rule 2 forbids it).

### 4. Failure Mode (What does it look like when this skill is wrong?)
The single highest-leverage axis. The skill must describe at least one *concrete observable* that means "this skill misfired" — not "things go badly". Example: "If `ClawGuard` rejects more than 5% of MCP payloads in a single session, the regex is over-eager; revisit the keyword list rather than auto-tuning it."

### 5. Cross-Skill Edges (What does it interact with?)
Named references to at least the upstream and downstream skill/diary. Without this, the skill is an island and the agent cannot route around it. Edges should appear as `See: Defensive_Execution_Protocol §Rule 3, SnapState §Resumption`.

### 6. Self-Verification (How does the agent confirm it ran correctly?)
A check the agent itself can run *after* invoking the skill, before declaring the step done. Examples:
- "After `K_Token_Merging`, the merged tensor's L2 norm must be within ±15% of the pre-merge mean."
- "After a `migrate_legacy_provenance` run, `audit_index.py --json` must report 0 `missing_provenance` items."

## Why Six and Not Three or Twelve
Three is too few — the most common existing failure (mechanism described, boundary missing) survives a 3-axis schema. Twelve is too many — anything beyond six gets skipped on a Friday afternoon and the schema rots. Six is the smallest schema that catches the four observed legacy failure classes: missing trigger, magic numbers, scope creep, and "skill that nobody can tell whether it ran".

## Integration with the Pipeline

### `audit_index.py` extension
A new check, `placeholder_skill_axis`, will scan every `.agents/skills/*.md` and `.agents/diaries/*.md`, parse H2 headings, and flag files missing any of the six required headings (or their close synonyms). This runs at the same severity level as `placeholder_frontmatter`.

### `sign_drafts.py` admission gate
`auto_commit.py` already requires a passing `utils.audit_text()` score. We extend admission so a draft in `staging/` that does not satisfy the six-axis schema receives a P1 finding (`schema_incomplete`) — high enough to block promotion, low enough that a legitimate work-in-progress can be saved without losing context.

### Workflow companion
The new `.agents/workflows/skill-deepen.md` workflow (created in this same migration) walks an author through the six axes in order and exits by writing a draft into `staging/` for review.

## Reference Examples (after enrichment)
The three skills enriched alongside this diary serve as canonical examples of the schema in use:
- `Karpathy_Strict_Mode` — strict-mode execution discipline.
- `Skeptical_Memory` — distrust default for retrieved long-term memory.
- `Adversarial_Verification` — pre-commit dialectic check.

Each will demonstrate a different shape of the six axes (numeric-heavy, boundary-heavy, verification-heavy) so future authors can pattern-match.

## Open Questions
1. Should self-verification be machine-checkable (a small Python predicate stored alongside the skill) or natural-language only? Initial bias: natural-language for v1, machine-checkable for v2 once we see which skills actually need automated post-checks.
2. How does the schema interact with `[RESEARCH MODE]` skills (e.g. `IG_Search_RL`) where thresholds are still being characterized? Provisional answer: research-mode skills may declare a threshold as `tentative: <range>` instead of a single value, and `audit_index.py` should treat that as compliant.

## Implementation Path
This diary is the source-of-truth for the `skill-deepen` workflow and the `audit_index.py` schema check. Promote out of staging once `audit_index.py` ships the `placeholder_skill_axis` rule and at least one skill has been refactored against the schema end-to-end.
