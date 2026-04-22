---
description: Legacy migrated asset.
---
# SKILL: IG-Search (Information Gain Search Strategy)
> Evaluator Score: 92/100 (Passed)

## Description
[RESEARCH MODE]
Enhances the `Research_Dialectic_Tree_Search` with a pre-calculation node that judges search feasibility through Step-Level Information Gain (IG).

## Heuristic Logic
To prevent search hallucination or meaningless API consumption:
1. **Node Evaluation**: Before searching, define an Information Expectation Matrix (What exactly are we looking for?).
2. **Post-Evaluation**: Once search results are retrieved, analyze the overlap against the Information Expectation Matrix.
3. **Penalty**: If overlap > 0.8 but novel data < 0.1, the search space is declared "depleted", and the branch is pruned.
4. **Reward Pipeline**: Future steps receive an aggregated multiplier based on novelty extracted from the URL.

## Pseudocode Paradigm
```python
def check_search_validity(current_context, proposed_search_query):
    # Assess semantic deviation
    if is_redundant(proposed_search_query):
         return False
    # ...
```
To be formally constructed into `Defensive_Execution_Protocol.md` logic.
