---
description: "[RESEARCH MODE] Automatically trigger web searches to fill information gaps and generate patch proposals for archive files."
---
# Dynamic Web Deep Dive

## Core Philosophy
Local archives (`.agents/archives/`) serve as high-level abstract syntheses. They frequently lack the deterministic code, formulas, or granular implementation steps required to solve hard engineering problems. If you rely solely on these abstractions, you will hallucinate.
When an archive is insufficient, you must **break out of local context, retrieve the absolute truth from the internet, and formulate a patch proposal.**

## Execution Rules

### 1. Zero-Hallucination Fallback
- If a retrieved local archive mentions a concept, framework, or mathematical method but does not provide the explicit implementation code or formula, **YOU ARE STRICTLY FORBIDDEN FROM GUESSING OR INVENTING THE IMPLEMENTATION.** 

### 2. Immediate Active Retrieval (Primary Source Preference)
- The moment an information gap is detected, immediately halt deduction.
- Invoke your web search tool.
- **Primary Source First**: Target authoritative sources directly by searching `site:arxiv.org [Topic/Paper Title]` for math/theorems, or refer to official technical documentation, standards, and source code repositories.
- **Secondary Source Restriction**: Blogs or community articles may only be used as "discovery aids" and can never be treated as the canonical truth for the archive.

### 3. Archive Patch Proposal (User Approval Required)
- Once you discover the precise implementation details, do not merely use it once and forget it.
- You **MUST NOT** permanently mutate or overwrite the original local archive file automatically.
- Instead, formulate the new findings into a localized patch (e.g., `## [Deep Dive Implementation]`) and present it to the user.
- **Archive mutation is strictly blocked until the user issues an Explicit Approval** to overwrite the canonical archive. This prevents hallucinated data from contaminating the unified knowledge base.
