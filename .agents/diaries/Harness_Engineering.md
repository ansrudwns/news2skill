---
description: Legacy migrated asset.
---
# Harness Engineering: The Definitive Meta-Cognitive Control Layer

## Architectural Insight
The future of Agentic AI relies not just on foundational capacities, but heavily on the "Control Layer" (Harness) wrapped around it. Prompting alone is highly susceptible to contextual degradation. Harness Engineering aims to structurally enforce behavior across routing, context pruning, and automated execution constraints. 

## Pillar 1: Context Engineering & Progressive Disclosure (The Anchor)
- **Defeat Context Rot**: Suppress context fatigue by loading only essential metadata upfront. Instead of feeding 1,000-page manuals, employ **Progressive Disclosure**—inject only the title and a 100-token summary initially, forcing the agent to dynamically "Pull" full knowledge only when triggered.
- **The Context Anchor**: Agents must read deterministic root files (e.g., `GEMINI.md`) upon initialization to establish an immutable structural anchor and rule boundary.
- **Context Collapse (Log Compression)**: When massive unstructured payloads (e.g., 5,000 lines of console output) occur, truncate aggressively. 
  - *Conflict Resolution Standard*: **Always prefer deterministic truncation** (Regex/Python `tail`) first. Escalate to a costly "Summarizer Sub-Agent" *only* when deep semantic context is strictly required to proceed.

## Pillar 2: Tool Routing & Meta-Cognitive Arbitration (The Fences)
- **Minimize Tool Sprawl (MCP Standard)**: Exposing 100 raw API endpoints triggers decision paralysis and hallucination. Use JSON-RPC based Model Context Protocol (MCP) standards by exposing a **single generic verb** (e.g., `execute_harness`) that routes payloads in the backend. 
- **Meta-Cognitive Routing Logic**: 
  - *Conflict Resolution Standard*: The Primary Agent executes **Internal Meta-Cognitive Arbitration** first. The agent assesses whether internal zero-shot logic solves the task. External tools are invoked *only* if bounded limits are exceeded.
  - Do NOT stack unnecessary Nano-Models ahead of the main agent if internal routing suffices; utilize lightweight rule-engines (Regex) primarily at entry points.
- **Structural Blocking**: Implement Pre-commit hooks, Linter checks, and Sandboxes which auto-bounce errors directly back to the agent without human validation.

## Pillar 3: Evaluation-Driven Evolution (The Broom)
- **Break Self-Evaluation Bias**: Agents inevitably praise their own broken outputs. Establish cross-verification via separate execution streams (e.g. Codex planning, Claude executing), or mathematically enforce constraints using raw terminal outputs (Python Unittest failures). 
- **Garbage Collection (Pattern Cleanups)**: Agents mimic legacy codebase structures exponentially. Deploy cleanup routines to prune antipatterns before initiating traversal loops.
- **Quiet Success, Loud Failures**: Do not bloat context limits with successful test logs. Only stream the exceptions into the working memory.
