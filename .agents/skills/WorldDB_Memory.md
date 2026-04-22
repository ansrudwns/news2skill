---
description: Advanced Memory Architecture for Context Collapse Prevention
---
# WorldDB_Memory: Ontology-Aware Agentic Graph Memory

## Core Purpose
The `WorldDB_Memory` architecture prevents Context Collapse over long-running AI pipelines by providing an immutable, content-addressed knowledge graph. It allows the agent to dynamically track "Fact Supersession" without physically deleting history.

## How to Utilize
The core engine resides at `scripts/core/worlddb.py`.
When operating in tasks that span multiple sessions or require rigid consistency:
1. **Initialize**: Instantiate `MemoryGraph` to load the current workspace state.
2. **Insert**: Use `insert_node()` for any newly acquired facts, observations, or extracted variables.
3. **Update (Supersede)**: Use `update_node()` to logically replace an old fact with a new one. The old fact remains physically present for audit/history, but `get_active_fact()` will prioritize the newer one.
4. **Merkle Cascades**: Trust that related entities will automatically re-hash if underlying dependencies change.

## Defensive Guardrails
- **NEVER** attempt to directly mutate a node's dictionary. The system enforces strict SHA-256 immutability.
- If contradictory information is observed, **always** use `update_node` to supersede rather than ignoring the anomaly.
