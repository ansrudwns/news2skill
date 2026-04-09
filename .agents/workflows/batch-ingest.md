---
description: Automated Historical Knowledge Batch Ingestion Workflow
---

This is a one-time zero-click pipeline workflow that extracts historical insights from `AI 기술 동향 및 클로드 유출 분석.txt`, evaluates them autonomously, and deploys validated Knowledge Diaries or Skills into the system.

## 1. Historical Data Extraction
Execute the python script below to parse the historical document and save the structured insights into `historical_raw.json`.
// turbo-all
```bash
python scripts/ingest_historical.py
```

## 2. Data Analysis
Read `historical_raw.json` to analyze the extracted insights. All items here are highly valuable, so process all of them.

## 3. Autonomous Draft & Staging
For each insight from the JSON, autonomously perform the following:
- Classify the technology as either an **Executable Skill (Track A)** or **Conceptual Knowledge (Track B)**.
- Create draft files in `.agents/staging/` (name them `draft_skill_[name].md` or `draft_diary_[name].md`). Write the respective prompt instructions, Python scripts, or deep architectural analysis into these drafts. Ensure the drafts are written in **Korean** for maximum readability by the user.

## 4. Adversarial Verification
Act as a "Strict System Architect" to evaluate the drafts you just created. Score them out of 100 on the following 4 criteria. A draft must score >= 80 on ALL criteria to pass:
1. **Redundancy & Conflict Avoidance**: Does it conflict with existing rules?
2. **Actionable Determinism**: Does it contain clear scripts or definitive definitions?
3. **Token Efficiency (Cost vs Value)**: Is it concise enough that it won't cause prompt bloat?
4. **Safety (Sandbox Test)**: Is it structurally safe?

## 5. Auto-Commit & Index Registration (Zero-Click Deployment)
For the excellent draft files that passed Step 4, autonomously perform the following shell command to deploy them into the active ecosystem safely:
// turbo-all
```bash
python scripts/auto_commit.py
```
- Any files that failed the verification MUST be deleted from staging.
- The `auto_commit.py` script will automatically handle Collision Protection (preventing overwrites) and will independently update `AGENTS.md` for you.
- Once the entire pipeline is complete, briefly summarize the results to the user in **Korean**.

