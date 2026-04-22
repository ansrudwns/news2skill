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
