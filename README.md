<div align="center">
  <h1>Antigravity Zero-Click Pipeline 🚀</h1>
  <p>An autonomous, self-evolving Agentic Harness that scrapes global AI trends and distills them into executable <strong>Skills</strong> and cognitive <strong>Diaries</strong>.</p>
</div>

## 🧠 What is this?
This repository is an **Automated AI R&D Knowledge Pipeline**. Instead of manually reading AI news, this system uses a combination of Python crawlers and autonomous LLM agents (Antigravity) to fetch the latest AI engineering breakthroughs, pass them through an "Adversarial Verification" phase, and permanently deploy them as localized context assets.

It operates **100% autonomously** every morning via **GitHub Actions**.

## 🏗️ Architecture

The system is built upon a strict "Harness Engineering" philosophy to prevent LLM context collapse and hallucination.

* **`workflows/`**: The orchestration layer. Contains pipelines like `ai-daily.md` which run the 6-step zero-click deployment from data scraping to index registration.
* **`skills/` (Track A)**: Actionable, highly defensive instructions for the LLM. 
  * Examples: *Karpathy_Strict_Mode*, *Structured_Output_Forcer*, *Defensive_Fallback_Throttle*.
* **`diaries/` (Track B)**: Conceptual architecture repositories used by the LLM when planning massive system designs.
  * Examples: *Progressive_Disclosure*, *Context_Collapse*, *Routing_Before_Thinking*.
* **`backlog/` (Track C)**: A temporary stashing ground for brilliant AI concepts that were found but lacked clear implementation code. 

## ⚙️ How it works (The Pipeline)
1. **Hybrid Data Extraction**: A python script (`scripts/fetch_ai_trends.py`) scrapes bleeding-edge engineering trends from *Hacker News, Reddit (LocalLLaMA, MachineLearning), Hugging Face, DeepMind*, while the LLM runs autonomous dynamic Google searches.
2. **Adversarial Verification**: The LLM reviews its own drafted ideas objectively. If an idea lacks code implementation, it is relegated to the `backlog/`. If it is pure hallucination or conflicts with existing rules, it is deleted.
3. **Zero-Click Auto-Commit**: A Python script (`scripts/auto_commit.py`) safely moves validated insights into `skills/` or `diaries/` and automatically updates the root `AGENTS.md` index file.

## 🚀 Usage (Self-Driving Mode)
You don't need to do anything. 
The GitHub Action `.github/workflows/ai-daily-pipeline.yml` fires autonomously at **22:00 UTC (07:00 KST)** every day. It runs the entire pipeline, generates new schemas, and auto-commits directly into this repository.

> **Note**: To utilize the LLM context dynamically in your local development environment, simply symlink (`mklink`) the `.agents` directory to your active coding projects so your IDE or Agent can fetch the latest rules.
