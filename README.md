# Antigravity AI R&D Knowledge Pipeline

A hybrid automated and human-in-the-loop knowledge harness that aggregates global AI trends and distills them into rigorously defined executable **Skills** and architectural **Diaries**.

## Project Overview
This repository is a personal AI R&D knowledge management system built around the concept of an **Agentic Ouroboros** — a pipeline that feeds its own outputs back as better context for future work. Instead of manually tracking AI developments, the system uses hybrid Python crawlers and an LLM agent (Antigravity) to fetch breakthroughs, process them in an isolated Laboratory, track their provenance, and deploy them as localized context assets.

Cloud automation handles data collection. Human approval gates control what gets absorbed into the knowledge base.

## 🔐 Provenance & Audit
The system defends against LLM prompt injection and tracks asset provenance through a two-stage sequential audit pipeline:
* **Stage 1 — Static Heuristic Audit**: Raw LLM draft outputs are scanned against a shared ruleset (`utils.py` AUDIT_RULES, P0/P1/P2 classification) before signing proceeds.
* **Stage 2 — HMAC Provenance Attestation (`.intoto.json`)**: Drafts passing Stage 1 receive a provenance receipt containing a file hash and HMAC signature, inspired by SLSA provenance concepts.
* **Legacy Migration**: Pre-existing skills and diaries have been retroactively attested using the `Antigravity-Legacy-Bootstrap-Migration-2026-04-22` builder ID to satisfy the strict provenance requirement without triggering false audit rejections.
* **Downgrade Attack Prevention**: `auto_commit.py` rejects any file missing a valid `.intoto.json` or carrying a legacy `.sig` sidecar before indexing into `AGENTS.md`.

## System Architecture
The system is built on a **Harness Engineering** philosophy, informed by published Anthropic Claude Code patterns, designed to mitigate LLM context collapse and hallucinated outputs:

* **`.agents/workflows/`**: Orchestration layer. Step-by-step human-triggered pipelines (`ai-daily.md`, `ai-rd-planning.md`, `ai-lab-incubation.md`).
* **`.agents/skills/` (Track A)**: Actionable, defensive LLM instruction files. Uses XML boundaries for deterministic behavior. Loaded on-demand via Progressive Disclosure.
* **`.agents/diaries/` (Track B)**: Architectural design documents, loaded individually rather than all at once to avoid context bloat.
* **`.agents/backlog/` (Track C)**: Persistent storage for R&D Epics and research proposals awaiting execution.
* **`.agents/laboratory/` (Track D)**: Isolated workspace for trial-and-error experiment logs.
* **`.agents/reports/`**: Accumulated AI-generated daily briefings.
* **`.agents/staging/`**: Holding area for LLM-generated draft assets awaiting audit and signing.
* **`.agents/external_approved/` (Track G)**: Quarantined external skill assets, managed separately from core skills via `skill_triage.py`.
* **`.agents/archives/` (Track F)**: Closed epics and reference knowledge used as contextual memory.

## Execution Pipeline (Hybrid Cloud-Local)
1. **Cloud Data Queuing** *(automated)*: GitHub Actions scrapes AI news every morning at 07:00 KST (22:00 UTC on the previous day), appending structured data into `pending_queue.json` and pushing to the remote.
2. **Local Ingestion & Report** *(manual trigger)*: The user runs `git pull` and triggers `/ai-daily`. The LLM agent batch-processes the queue and writes a Daily Briefing to `.agents/reports/`.
3. **Research R&D** *(manual trigger)*: The user triggers `/ai-rd-planning`. The agent reads accumulated reports and proposes R&D Epics into the Backlog.
4. **Execution & Absorption** *(human-approved)*: The agent builds Epics in `laboratory/`. On success, `sign_drafts.py` audits and signs the result; `auto_commit.py` promotes it to `skills/` and updates `AGENTS.md`. Each step requires explicit user approval before execution.

## Local Setup
Run `setup.bat` from the repository root to create or heal `.venv`, install `requirements.txt`, and initialize `.env` with `AGENT_PRIVATE_SIGNATURE_KEY` when missing.

The core prototype tests under `scripts/core/tests/` require `numpy`, which is pinned in `requirements.txt`.

## External Skill Stores
The repository uses two separate external-skill stores:

1. `.agents/external_approved/` is the copied, reviewed, pull-based skill library. It contains approved external skills and an `INDEX.json` discovery file. These skills are not globally active instructions; the agent should search the index, suggest a relevant skill, and then load only the selected `.md` file.

2. `skills-lock.json` is the source-path registry for live `external_skills/**/SKILL.md` files. Every `skillPath` in the lock file must point to a real file in the current workspace.

External skill repositories live under `external_skills/` as local cache data. That directory is intentionally ignored by git, so a clean checkout may need the provider folders restored before registry entries that reference them can be used. Do not commit full external skill clones unless the repository policy changes.

Use `.agents/external_approved/` when you want a curated copy that can be read as a reference skill. Use `skills-lock.json` when you want to track a live external source file with hash and collision checks.

Use `scripts/add_skill.py` for one skill at a time:

```powershell
.venv\Scripts\python.exe scripts\add_skill.py external_skills/open-design/skills/dashboard/SKILL.md --dry-run
```

Use `scripts/sync_external_skills.py` to scan a provider or all external skills and register only safe candidates:

```powershell
.venv\Scripts\python.exe scripts\sync_external_skills.py --provider open-design --dry-run
.venv\Scripts\python.exe scripts\sync_external_skills.py --provider open-design --write
```

Default sync mode is dry-run. `--write` updates `skills-lock.json`, `--force` bypasses semantic collision warnings only, and exact name/path/hash duplicates remain blocked.

## Maintenance Checks
Before committing environment or registry changes, run:

```powershell
.venv\Scripts\python.exe -m py_compile scripts\add_skill.py scripts\sync_external_skills.py
.venv\Scripts\python.exe -m unittest discover -s scripts\core\tests
.venv\Scripts\python.exe scripts\audit_index.py --json
.venv\Scripts\python.exe -m json.tool skills-lock.json
```

For lock integrity, also verify that every registered skill path exists:

```powershell
.venv\Scripts\python.exe -c "import json, pathlib; root=pathlib.Path('.'); data=json.load(open('skills-lock.json', encoding='utf-8')); missing=[(n,e.get('skillPath','')) for n,e in data['skills'].items() if not (root/e.get('skillPath','')).exists()]; print('entries', len(data['skills'])); print('missing', len(missing)); [print(f'{n}: {p}') for n,p in missing]"
```

`scratch/`, `.venv/`, `__pycache__/`, `.env`, and `external_skills/` are local-only operational data and should normally stay out of commits.
