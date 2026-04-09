# Antigravity Agent Source of Truth

This is the primary Harness configuration and skill registry. 
Before embarking on any task, you MUST check this registry. If a task implies one of the domains below, you MUST use `view_file` to read the exact instructions from the respective `.md` file before proceeding.

## Track A: Executable Skills Registry
- **Structured_Output_Forcer**: Ensure robust payload exchanges by forcing LLM interfaces to output strict JSON schemas with fail-safes. (Path: `.agents/skills/Structured_Output_Forcer.md`)
- **Karpathy_Strict_Mode**: Suppress AI hallucination and over-engineering by enforcing minimal, surgical code modifications. (Path: `.agents/skills/Karpathy_Strict_Mode.md`)
- **Defensive_Fallback_Throttle**: Prevent infinite loops and 429 errors in asynchronous pipelines using backoffs and degradation. (Path: `.agents/skills/Defensive_Fallback_Throttle.md`)
- **Skeptical_Memory**: Ensure factual accuracy by actively verifying system file states before code editing. (Path: `.agents/skills/Skeptical_Memory.md`)
- **Adversarial_Verification**: Pause and self-critique/verify for edge cases before outputting the final result. (Path: `.agents/skills/Adversarial_Verification.md`)
- **Blocking_Budget**: Restrict autonomous background actions (pings/commands) to avoid blocking the user. (Path: `.agents/skills/Blocking_Budget.md`)

## Track B: Architectural Diaries Registry
- **Routing_Before_Thinking**: Optimize token expenditure by utilizing lightweight model routing before invoking heavy reasoning models. (Path: `.agents/diaries/Routing_Before_Thinking.md`)
- **Harness_Engineering**: Design patterns for control layers and execution-intelligence splits. (Path: `.agents/diaries/Harness_Engineering.md`)
- **MCP**: Best practices for generic verb routing to minimize Tool Sprawl. (Path: `.agents/diaries/MCP.md`)
- **Progressive_Disclosure**: Memory efficiency pattern - load only single focused docs rather than heavy context. (Path: `.agents/diaries/Progressive_Disclosure.md`)
- **autoDream**: Context maintenance and background memory healing strategies. (Path: `.agents/diaries/autoDream.md`)
- **Context_Collapse**: Compression techniques for large system logs using subagents. (Path: `.agents/diaries/Context_Collapse.md`)
