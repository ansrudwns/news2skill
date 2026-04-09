---
description: Suppress AI hallucination and over-engineering by enforcing minimal, surgical code modifications.
---
# Karpathy Strict Mode Protocol

## Core Philosophy
When modifying code or adding features, avoid speculative modifications. An agent should never preemptively refactor unrelated code or guess missing variables.

## Execution Rules
1. **Surgical Changes Only**: Do not modify even a single line of perfectly functioning adjacent code. Apply minimal, surgical edits to achieve the objective.
2. **No Hallucination**: Never guess the context or purpose of unknown variables/functions. If missing, pause and proactively ask the user.
3. **Conservative Verification**: When faced with multiple implementation paths, always choose the most conservative, readable, and simplest approach.
4. **Option-Aware Testing**: Do not blindly assume the patch will work. Explicitly list 3 edge cases (e.g., Null inputs, Out-of-bounds) and verify the logic against them before completion.
