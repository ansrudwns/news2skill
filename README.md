# Antigravity Zero-Click Pipeline (Agentic Ouroboros)

An autonomous, self-evolving Agentic Harness that aggregates global artificial intelligence trends and distills them into rigorously defined executable **Skills** and architectural **Diaries**. 

## Project Overview
This repository serves as an Automated AI R&D Knowledge Pipeline designed around the concept of an **Agentic Ouroboros** (Self-improving AI). Instead of relying on manual ingestion of technological developments, the system employs hybrid Python crawlers and autonomous LLM agents (Antigravity). It fetches the latest AI breakthroughs, processes them in an isolated Laboratory, verifies them against global supply chain security standards (SLSA), and permanently deploys them as localized context assets.

The framework operates fully autonomously every day via GitHub Actions and local LLM agents.

## 🔒 Security & Provenance (Agentic SLSA)
The system tackles LLM Prompt Injection and Supply Chain attacks natively without human intervention:
* **Dual-Agent Auditor Node**: Raw LLM outputs are physically isolated and validated using strict heuristic rules.
* **Cryptographic Attestation (`.intoto.json`)**: If an AI's output is safe, the Auditor node generates its own SLSA-compliant JSON provenance receipt embedded with an HMAC signature.
* **Downgrade Attack Prevention**: `auto_commit.py` inspects every file before indexing. Files passing the `intoto` checks are absorbed into the system brain (`AGENTS.md`), while tampered or legacy files are strictly rejected.

## System Architecture
The system is constructed upon a strict **Harness Engineering** philosophy (heavily integrating leaked *Anthropic Claude Code* architectures) designed to mitigate LLM context collapse and hallucinated outputs:

* **`.agents/workflows/`**: The orchestration layer. Contains execution pipelines such as `ai-daily.md` (Daily ingestion).
* **`.agents/skills/` (Track A)**: Actionable, highly defensive system instructions. Uses XML boundaries (`<thinking>`, `<system>`) for deterministic behavior.
* **`.agents/diaries/` (Track B)**: Conceptual architecture repositories utilized via **Progressive Disclosure** (loading only single focused docs rather than heavy context).
* **`.agents/backlog/` (Track C)**: A persistent storage layer for theoretical AI implementations (Epics) and archived quests.
* **`.agents/laboratory/` (Track D)**: An isolated workspace preserving the trial-and-error logs of novel research projects.
* **`.agents/reports/`**: Aggregated collection of AI-generated summaries and daily briefings.
* **`.agents/staging/`**: A secure holding area for cryptographic signatures and verified skills prior to permanent integration.
* **`.agents/archives/` (Track F)**: Past reference solutions, methodologies, and closed epics used strictly as contextual memory.

## Execution Pipeline (Hybrid Cloud-Local)
1. **Cloud Data Queuing**: GitHub Actions autonomously scrapes AI news every morning at 07:00 KST, appending the raw data into `pending_queue.json`.
2. **Local Ingestion & Report**: The user downloads the queue via `git pull` and triggers `/ai-daily`. The LLM Agent summarizes the queue into a Daily Briefing.
3. **Research R&D (Ideation)**: Periodically, the user triggers `/ai-rd-planning`. The Agent reads all past reports to formulate actionable R&D Epics in the Backlog.
4. **Execution & SLSA Absorption**: The Agent builds the Epic inside the `laboratory/`. If successful, the Dual-Agent framework signs the result, and `auto_commit.py` upgrades the code natively into a `skill/` for next-generation intelligence.
