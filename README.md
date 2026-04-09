# Antigravity Zero-Click Pipeline

An autonomous, self-evolving Agentic Harness that aggregates global artificial intelligence trends and distills them into rigorously defined executable **Skills** and architectural **Diaries**.

## Project Overview
This repository serves as an Automated AI R&D Knowledge Pipeline. Instead of relying on manual ingestion of technological developments, the system employs hybrid Python crawlers and autonomous LLM agents (Antigravity). It fetches the latest AI engineering breakthroughs, processes them through an Adversarial Verification phase, and permanently deploys them as localized context assets for immediate integration.

The framework operates fully autonomously every day via GitHub Actions.

## System Architecture
The system is constructed upon a strict "Harness Engineering" philosophy designed to mitigate LLM context collapse and hallucinated outputs.

* **`workflows/`**: The orchestration layer. Contains execution pipelines such as `ai-daily.md` (Daily ingestion) and `ai-rd-planning.md` (Macro R&D Strategist).
* **`skills/` (Track A)**: Actionable, highly defensive system instructions.
* **`diaries/` (Track B)**: Conceptual architecture repositories utilized by the LLM when planning extensive system designs.
* **`backlog/` (Track C)**: A persistent storage layer for theoretical AI implementations (Epics) and archived quests.
* **`laboratory/` (Track D)**: An isolated workspace preserving the trial-and-error logs (`Experiment_Log.md`) of novel research projects.

## Execution Pipeline (Hybrid Cloud-Local)
1. **Cloud Data Queuing**: GitHub Actions autonomously scrapes AI news every morning at 07:00 KST, appending the raw data into `pending_queue.json`.
2. **Local Ingestion & Report**: The user downloads the queue via `git pull` and triggers `/ai-daily`. The LLM Agent summarizes the queue into a Daily Briefing and empties the queue.
3. **Meta-Research Ideation**: Periodically, the user triggers `/ai-rd-planning`. The Agent reads all past reports to formulate actionable R&D Epics in the Backlog.
4. **Execution & Mastery**: The User approves an Epic. The LLM Agent builds it inside the `laboratory/` (if novel) or directly auto-commits it as a `skill/` (if integration).

## Operation & Usage
This framework operates in a **Hybrid Cloud-Local Mode** to minimize API costs.
1. Cloud runs 24/7 autonomously collecting data to the Queue.
2. Open terminal and run `git pull` to fetch the accumulated queue to your laptop.
3. Chat with the Agent: **"Run the `/ai-daily` workflow"** to process the news into intelligence.
4. (Optional) Chat: **"Run the `/ai-rd-planning` workflow"** to generate new architectural Epics.
