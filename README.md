# Antigravity Zero-Click Pipeline

An autonomous, self-evolving Agentic Harness that aggregates global artificial intelligence trends and distills them into rigorously defined executable **Skills** and architectural **Diaries**.

## Project Overview
This repository serves as an Automated AI R&D Knowledge Pipeline. Instead of relying on manual ingestion of technological developments, the system employs hybrid Python crawlers and autonomous LLM agents (Antigravity). It fetches the latest AI engineering breakthroughs, processes them through an Adversarial Verification phase, and permanently deploys them as localized context assets for immediate integration.

The framework operates fully autonomously every day via GitHub Actions.

## System Architecture
The system is constructed upon a strict "Harness Engineering" philosophy designed to mitigate LLM context collapse and hallucinated outputs.

* **`workflows/`**: The orchestration layer. Contains execution pipelines such as `ai-daily.md` which run the 6-step zero-click deployment from data aggregation to index registration.
* **`skills/` (Track A)**: Actionable, highly defensive system instructions.
  * Examples: *Karpathy_Strict_Mode*, *Structured_Output_Forcer*, *Defensive_Fallback_Throttle*.
* **`diaries/` (Track B)**: Conceptual architecture repositories utilized by the LLM when planning extensive system designs.
  * Examples: *Progressive_Disclosure*, *Context_Collapse*, *Routing_Before_Thinking*.
* **`backlog/` (Track C)**: A persistent storage layer for theoretical AI implementations that lack immediate execution paths.

## Execution Pipeline
1. **Hybrid Data Extraction**: A dedicated execution script (`scripts/fetch_ai_trends.py`) scrapes bleeding-edge engineering trends from Hacker News, Reddit (LocalLLaMA, MachineLearning), Hugging Face, and Google DeepMind.
2. **Adversarial Verification**: The LLM objectively analyzes the ingested ideas. Concepts lacking concrete code implementations are relegated to the `backlog/`. Any unverified or hallucinated proposals are purged.
3. **Zero-Click Auto-Commit**: A deployment script (`scripts/auto_commit.py`) securely commits validated insights into the `skills/` or `diaries/` directories and automatically synchronizes the root `AGENTS.md` index file.

## Operation & Usage
No manual intervention is required. 
The GitHub Action `.github/workflows/ai-daily-pipeline.yml` fires autonomously at 22:00 UTC (07:00 KST) daily. It executes the entire pipeline, generates localized assets, and automatically commits directly into this main repository branch.

**Integration Note**: To utilize this dynamically updating context in your local development environment, establish a symbolic link (`mklink`) from the `.agents` directory to your active workspace environments. This ensures local IDEs or Agent systems always utilize the latest verification rules.
