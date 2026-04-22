---
description: Legacy migrated asset.
---
# Claude Advisor Tool API Architecture Reference

## Overview
Anthropic's `Advisor Tool` (Beta: `advisor-tool-2026-03-01`) is a hybrid execution paradigm for the `/v1/messages` API. It enables a lightweight "Executor" model (e.g., Claude 3.7 Sonnet) to handle routine tasks and automatically trigger a high-intelligence "Advisor" model (e.g., Claude 3.7 Opus) ONLY when it encounters complex bottlenecks or structural deadlocks.

## Strategic Relevance
This methodology solves the cost-intelligence trade-off in autonomous agentic loops.
While the Antigravity local agent cannot switch its own kernel model recursively, this reference is archived for **future Python-based API orchestration tools** (e.g., `llm_auditor.py` or SLSA reviewers) that may be developed within this repository to reduce API token costs by 90% while maintaining Opus-level oversight.

## Implementation Mechanics (API Reference)
1. **Single Request Orchestration**: The handoff occurs within a single API call. No custom looping logic is required by the developer.
2. **Parameters**:
   - `anthropic-beta`: `advisor-tool-2026-03-01`
   - `max_uses`: Limits the total number of times the Executor can consult the Advisor (prevents infinite cost drain).
3. **Behavior**: The Advisor model generates a 400-700 token strategic guideline and hands the execution context back to the Executor without returning final output directly to the end-user.

## Antigravity Adaptation Concept (Meta-Cognitive Handoff)
For the local Antigravity Agent, this concept translates to the **"Hold & Escalate Protocol"**:
- If the Agent faces >3 iteration failures (e.g., syntax loops, missing tool capabilities).
- The Agent must mimic the "Advisor Handoff" by suspending execution and explicitly requesting the Human Operator (or a higher-tier agent) for strategic clarification, rather than burning context limits.
