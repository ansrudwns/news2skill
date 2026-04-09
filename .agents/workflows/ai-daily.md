---
description: Automated AI R&D Daily Hybrid Analysis & Assetization Workflow
---

This is a 6-step zero-click pipeline workflow that hybridizes Python scraping with autonomous Agentic Web Search. It aggregates the latest AI papers, news, and blogs daily, evaluates them, and automatically deploys validated knowledge into the file system or stashes incomplete ideas into a Research Backlog.

## 1. Hybrid Data Extraction
First, use your native `search_web` tool to autonomously search for "latest AI engineering methodologies, Github trending AI frameworks, and Anthropic/Google breakthroughs today". 
Second, execute the python script below to scrape structured data from global hacker communities (Reddit/HN) and corporate feeds.
// turbo-all
```bash
python scripts/fetch_ai_trends.py
```

## 2. Integrated Data Analysis
Analyze the raw JSON output AND the findings from your web search. Select the 4~5 most insightful and actionable topics for our development/product team.

## 3. Report Generation
Write a markdown artifact named `AI_Trend_Report.md` in **Korean** based on the selected items. Format each item with the Title, Source Link, Core Summary, and an Actionable Item detailing how our team can integrate the technology.

## 4. Autonomous Draft & Staging
Based on the generated report, autonomously perform the following:
- Classify the technology as either an **Executable Skill (Track A)** or **Conceptual Knowledge (Track B)**.
- **Deep Research**: If the original article lacks implementation code, you MUST actively use your `search_web` tool to search GitHub, StackOverflow, or official docs to find the missing instructions.
- Create draft files in `.agents/staging/` (name them `draft_skill_[name].md` or `draft_diary_[name].md`). All draft contents MUST be written in **highly professional English** to optimize LLM token usage.

## 5. Adversarial Verification
Act as a "Strict System Architect" to evaluate the drafts you just created. Score them out of 100. A draft must score >= 80 to pass.
1. **Redundancy & Conflict Avoidance**: Does it conflict with existing rules in `.agents/skills/`?
2. **Actionable Determinism**: Does it contain clear scripts or definitive command routines rather than vague instructions?
3. **Token Efficiency**: Is it concise?
4. **Safety**: Is it structurally sound and free from infinite loops?

**CRITICAL BACKLOG RULE:** If a draft idea is exceptionally brilliant but scores low *only* on "Actionable Determinism" (because you couldn't find the exact implementation code during your deep research), DO NOT DELETE IT. Instead, rename the file to `draft_backlog_[name].md`. If the idea is low quality, delete it outright.

## 6. Auto-Commit & Index Registration (Zero-Click Deployment)
For the drafted files, autonomously perform the following shell command to deploy them safely:
// turbo-all
```bash
python scripts/auto_commit.py
```
- The `auto_commit.py` script will automatically handle Collision Protection, create the `backlog/` folder if needed, and update `AGENTS.md` natively.
- Once the pipeline is complete, briefly summarize the results to the user in **Korean** (mentioning what trends were found, what drafts were passed, and what was stashed in the backlog).
