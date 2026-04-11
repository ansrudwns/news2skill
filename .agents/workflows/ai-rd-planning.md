---
description: R&D Strategy Ideation and Global Novelty Verification Workflow
---

This workflow is an executive-level Meta-Research process. It analyzes the accumulated daily trends, formulates macro R&D project proposals based on identified market missing-links, and performs strict Adversarial Novelty Verification to ensure we don't reinvent the wheel.

## 1. Context Ingestion (Macro Trend Analysis)
- Read all accumulated files located inside `.agents/reports/`.
- Review the `AGENTS.md` and currently deployed files in `.agents/skills/` and `.agents/diaries/` to understand our system's current capability baseline.
- Analyze the difference between "Global AI Trends" and "Our Current Architecture". What are the glaring bottlenecks or major missing conceptual frameworks?

## 2. R&D Ideation (Proposal Generation)
Propose 3 highly actionable, cutting-edge R&D project proposals (Epics). Each proposal must define:
- **Title**: A clear R&D mission name.
- **Background**: Why this is necessary based on the accumulated reports.
- **Hypothesis/Goal**: The core feature or architecture to be built.
- **Expected Impact**: How this elevates our AI infrastructure.

## 3. Adversarial Novelty Verification (Pre-computation Check)
**Do not skip this step.** For EACH of your 3 proposals, you MUST actively verify if it is already a solved problem.
- **Global Verification**: Use available web search tools to search Google and GitHub. Look for exact frameworks, papers, or OSS libraries that already do exactly what the proposal suggests.
- **Internal Verification**: Check if our existing `.agents/skills` or `backlog` already explicitly solves this.

*If an existing robust solution or paper already exists*: You must PIVOT the proposal. Instead of "building it from scratch", change the Epic strategy to "Integrate [Existing Solution] into our architecture". We do not reinvent the wheel.

## 4. Epic Publication & Deployment Proposal
For the 3 verified/pivoted R&D Epics, use a file-writing tool to save them inside `.agents/backlog/research_proposals/` naming them `Epic_1_[Name].md`, `Epic_2_[Name].md`, etc. (Create the directory first if needed).

Prepare the deployment command to securely save them and push to the remote repository. **You MUST request Explicit User Approval before running this command.**
```bash
python scripts/auto_commit.py
```

- Report a brief **Korean** summary to the user outlining the 3 finalized Epics and the results of the Novelty Verification.
