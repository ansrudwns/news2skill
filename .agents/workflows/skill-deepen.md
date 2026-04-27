---
description: Step-by-step workflow that walks an author from a thin/legacy skill draft to a six-axis-compliant skill, producing a file in .agents/staging/ ready for sign_drafts.py.
---
# Workflow: skill-deepen

> Goal: take any skill that fails the `Skill_Quality_Schema` six-axis check (or any new skill being authored from scratch) and produce a draft in `.agents/staging/` that passes the schema, ready for `sign_drafts.py` and `auto_commit.py` promotion.
>
> Source-of-truth schema: `.agents/diaries/Skill_Quality_Schema.md` (after promotion from staging).

## When to run
- The output of `audit_index.py` flags a skill with `placeholder_skill_axis`.
- Authoring a new skill from scratch.
- A diary or backlog entry has matured to the point of becoming a callable skill.

## When NOT to run
- The skill is `[RESEARCH MODE]` and explicitly tagged as exploratory; thresholds may legitimately be tentative. Run only the axis 1 / 3 / 4 sub-steps and mark the rest as `tentative`.
- The artefact is a diary, not a skill. Diaries are explanatory; they do not need to be callable.

## Inputs
- `<source>`: existing skill file path, or empty for greenfield.
- `<name>`: snake-or-pascal-cased name. Must equal the filename stem (per `audit_index.check_path_name_mismatch`).

## Output
- `.agents/staging/draft_skill_<name>.md` containing the six required H2 sections.

---

## Step 0 — Snapshot the source
If `<source>` exists, Read it in full. Capture:
- The current `description:` (often "Legacy migrated asset.").
- The H1 title.
- The Mechanism / Execution Rules body (this is what the original author *meant*; it is rarely what's missing).

Do not delete any existing prose yet — the schema enriches, it does not replace. The original Mechanism almost always survives into the new draft as supporting text under one of the six axes (typically axis 3 or 5).

## Step 1 — Axis 1: Trigger
Write a single paragraph or bullet block that answers "what observable conditions cause this skill to fire?". Hard rule: no vibes. Every clause must be a thing the agent can detect at runtime.

Quality gate: replace every word like "complex", "heavy", "important" with a measurable surrogate. If you cannot, the trigger is not yet operational — escalate to a diary instead.

## Step 2 — Axis 2: Thresholds
List every quantitative knob that governs the skill, with a default value and a unit. If the original draft contains "if overlap is high", convert it to `overlap > 0.8`. If a number is genuinely unknown, write `tentative: <range>` and link to the open question that resolves it.

Quality gate: 0 numbers in the body without a unit; 0 adjectives functioning as numbers.

## Step 3 — Axis 3: DO / DON'T
At least one DO and at least one DON'T, both written as imperatives. Each must be matchable by the agent against a candidate action — "DO X" rather than "DO things like X". The original Mechanism / Execution Rules from Step 0 usually slot under DO; their negations or scope-limits slot under DON'T.

Quality gate: every DO/DON'T survives the test "could the agent unambiguously decide whether a candidate action satisfies this rule?"

## Step 4 — Axis 4: Failure Mode
Describe at least one **concrete observable** that means the skill misfired. Not "things go badly" — "the regex rejects > 5% of MCP payloads in one session".

Quality gate: each observable is something the agent or a script can measure post-hoc. If the observable requires a human to judge, refine until it doesn't.

## Step 5 — Axis 5: Cross-Skill Edges
List upstream and downstream skill/diary references. Use exact names. Where there is a hard conflict (e.g. strict-mode vs. research-mode) call it out explicitly.

Quality gate: at least one upstream and one downstream named, OR an explicit "this is a leaf skill — no downstream" justification.

## Step 6 — Axis 6: Self-Verification
Provide a check the agent can run *itself* after invoking the skill. Prefer 3–4 yes/no questions the agent must answer affirmatively before declaring the step complete.

Quality gate: each check is something the agent can perform without external review.

## Step 7 — Stage and sign
Write the draft to `.agents/staging/draft_skill_<name>.md`. Do not write to `.agents/skills/` directly — `auto_commit.py` is the only path into the indexed tracks.

Run, in this order:
1. `python scripts/audit_index.py` — must report 0 new drift items attributable to this draft.
2. `python scripts/sign_drafts.py` — produces the `.intoto.json` sidecar.
3. `python scripts/auto_commit.py --dry-run` — review the diff that *would* land in `.agents/skills/`.
4. `python scripts/auto_commit.py` — promote.

If any step fails, do **not** hand-edit around the failure — return to the relevant axis step and refine.

---

## Cross-references
- Schema definition: `.agents/diaries/Skill_Quality_Schema.md`
- Audit script that enforces it: `scripts/audit_index.py` (rule `placeholder_skill_axis`)
- Provenance: `scripts/sign_drafts.py`, `scripts/auto_commit.py`
- Worked examples: `draft_skill_Karpathy_Strict_Mode.md`, `draft_skill_Skeptical_Memory.md`, `draft_skill_Adversarial_Verification.md` (all in `.agents/staging/` until promoted).

## Open questions
- Should this workflow be machine-runnable (a script that prompts for each axis and writes the draft) instead of a markdown SOP? Probably yes once the schema stabilises. For v1, keeping it as prose lets the schema evolve cheaply.
