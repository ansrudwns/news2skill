---
description: "Recursive agent optimization workflow for spawning bounded sub-agents to improve prompts, tool use, or weak intermediate outputs."
---
# Skill: Recursive Agent Optimization

## Description
This skill dictates how an agent can recursively spawn sub-agents to optimize its own prompt, tool usage, or intermediate outputs. Based on "Recursive Agent Optimization" (arXiv:2605.06639).

## Trigger
Use this skill when the first-pass output of a complex task fails adversarial verification, or when empirical performance drops below threshold.

## Execution Flow
1. **Evaluate**: The parent agent scores the output.
2. **Spawn**: If score < threshold, spawn a child agent with the exact failure trace.
3. **Mutate**: The child agent mutates the original prompt or parameters.
4. **Test**: The child agent runs the new configuration in the `07_Sandbox`.
5. **Backpropagate**: If successful, the new configuration is returned to the parent.

## Guidelines
- **DO**: Ensure strict recursion depth limits (e.g., `MAX_RECURSION = 3`) to prevent infinite loops.
- **DON'T**: Do not use this skill for simple deterministic tasks.

## Failure Modes
- **Infinite Recursion**: Prevented by aggressive depth tracking.
- **Resource Exhaustion**: Handled by Defensive Execution Protocol and SnapState.
