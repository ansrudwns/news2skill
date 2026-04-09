---
description: Optimize token expenditure by utilizing lightweight model routing before invoking heavy reasoning models.
---
# Routing Before Thinking (Routing First)

## Architectural Insight
Feeding massive datasets indiscriminately into heavy baseline models (like Opus or Pro) wastes tokens, slows down execution, and increases hallucination risks.

## Best Practices
1. **Interception Layer**: Place a highly lightweight rules-engine (Regex, Metadata) or a nano-model (Haiku/Flash) at the entry point of any multi-agent pipeline.
2. **Triage Classification**:
   - **Easy**: Resolve immediately using cache returns or simple string passes without heavy reasoning.
   - **Medium**: Route to a constrained worker with a heavily focused dataset segment.
   - **Hard**: Only escalate to the flagship reasoning model unconditionally when profound, generalized logic crafting is strictly demanded.
