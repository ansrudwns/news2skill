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

## 2. Integrated Data Analysis (Batch Processing & The Frontier Sieve)
If `pending_queue.json` contains a massive number of entries, do NOT attempt to summarize them all at once. Process the JSON array in batches (e.g., 15 items per batch).
For every item, apply **The Frontier Sieve**:
1. Discard generic PR news, shallow blogs, or minor version updates.
2. ONLY extract deep architectural methodologies, novel mathematical breakthroughs, or code-implementable paradigms.
There is **NO LIMIT** on the number of topics you can extract. If 30 topics pass the sieve, extract all 30. Append findings from each batch sequentially.

## 3. Report Generation (Daily Archiving)
Write a permanent markdown file using the `write_to_file` tool to save the daily summary. 
The file MUST be saved in `.agents/reports/` using the current date formatting: `.agents/reports/YYYY-MM-DD_Daily_Briefing.md`.
The report should be written in **Korean**. Format each item with the Title, Source Link, Core Summary, and an Actionable Item detailing how our team can integrate the technology.

**CRITICAL REPORT RULE (System Modification Log):**
At the very bottom of the report, you MUST include a `## System Modification Log (Changelog)` section. Detail all files you created, edited, or deleted in the workspace during this daily session. Use labels `[NEW]`, `[MODIFIED]`, and `[DELETED]` along with a brief rationale for the architectural change. This ensures the user has a black-box trace of all your file-system modifications.

## 4. Autonomous Draft & Staging
Based on the generated report, autonomously perform the following:
- Classify the technology into **Executable Skill (Track A)**, **Architectural Diary (Track B)**, or **Reference Archive (Track F)**.
- **Deep Research**: If the original article lacks implementation code, you MUST actively use your `search_web` tool to search GitHub, StackOverflow, or official docs to find the missing instructions.
- Create draft files in `.agents/staging/` (name them `draft_skill_[name].md`, `draft_diary_[name].md`, or `draft_archive_[name].md`). All draft contents MUST be written in **highly professional English** to optimize LLM token usage.

## 5. Adversarial Verification
Act as a "Strict System Architect" to evaluate the drafts you just created. Score them out of 100. A draft must score >= 80 to pass.
1. **Redundancy & Conflict Avoidance**: Does it conflict with existing rules in `.agents/skills/`?
2. **Actionable Determinism**: Does it contain clear scripts or definitive command routines rather than vague instructions?
3. **Token Efficiency**: Is it concise?
4. **Safety**: Is it structurally sound and free from infinite loops?

**CRITICAL BACKLOG RULE:** If a draft idea is exceptionally brilliant but scores low *only* on "Actionable Determinism" (because you couldn't find the exact implementation code during your deep research), DO NOT DELETE IT. Instead, rename the file to `draft_backlog_[name].md`. If the idea is low quality, delete it outright.

## 6. Auto-Commit & Index Registration (Zero-Click Deployment)
// turbo-all
```bash
python scripts/sign_drafts.py
python scripts/auto_commit.py
```
- The `auto_commit.py` script will automatically handle Collision Protection, create the `backlog/` folder if needed, and update `AGENTS.md` natively.
- After all deployment is complete, **MUST EMPTY THE QUEUE** by modifying `pending_queue.json` to just `{"data": []}` using the `write_to_file` tool so we don't process them again next time.
- **CRITICAL SYNC:** The user manual promises automated backups. You MUST run a terminal command `git add .agents/ pending_queue.json seen_urls.txt ; git commit -m "🤖 [auto] Daily R&D Sync and Index Update" ; git push` to sync the changes back to the remote repository.
- Once the pipeline is complete, briefly summarize the results to the user in **Korean** (mentioning what trends were found, what drafts were passed, and what was stashed in the backlog).
