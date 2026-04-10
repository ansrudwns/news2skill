---
description: Automatically trigger web searches to fill information gaps and mutate archive files.
---
# Dynamic Web Deep Dive

## Core Philosophy
Local archives (`.agents/backlog/archives/`) serve as high-level abstract syntheses. They frequently lack the deterministic code, formulas, or granular implementation steps required to solve hard engineering problems. If you rely solely on these abstractions, you will hallucinate.
When an archive is insufficient, you must **break out of local context, retrieve the absolute truth from the internet, and cache it.**

## Execution Rules

### 1. Zero-Hallucination Fallback
- If a retrieved local archive mentions a concept, framework, or mathematical method but does not provide the explicit implementation code or formula, **YOU ARE STRICTLY FORBIDDEN FROM GUESSING OR INVENTING THE IMPLEMENTATION.** 

### 2. Immediate Active Retrieval
- The moment an information gap is detected, immediately halt deduction.
- Invoke your `search_web` tool.
- Target authoritative sources directly by appending `site:arxiv.org [Topic/Paper Title]` for math/theorems, or `site:github.com [Topic/Framework name]` for source code and architecture.

### 3. Archive Mutation & Caching
- Once you discover the precise implementation details (e.g., the exact Python code snippet, the exact Lean 4 proof structure), do not merely use it once and forget it.
- You **MUST** permanently mutate the original local archive file you were reading.
- Open the archive file and append a section titled `## [Deep Dive Implementation]` at the bottom.
- Overwrite the file to cache the raw, high-resolution truth you just found.
- This ensures the agent system self-evolves and never has to search for the same granular detail twice.
