---
description: "Reference Archive: Structured Distillation of Web Agent Capabilities Enables Generalization (Agent-as-Annotators)"
tags: [Web Agents, Distillation, Agent-as-Annotator, Synthetics, Autonomous Navigation]
---

# Structured Distillation of Web Agent Capabilities

## 1. Core Bottleneck
Frontier LLMs can navigate complex websites, but their API cost, latency, and token consumption make highly parallelized local deployment impossible. Small local models fail at web orchestration due to structural planning deficits.

## 2. Algorithmic Paradigm
**Agent-as-Annotators (Synthetic Structure Distillation):**
Instead of distilling pure input/output text mapping (which fails out-of-distribution), this framework distills the *structural reasoning topology*.
1. **Teacher Agent Trajectory Mapping**: A frontier agent navigates the web and records an explicit DAG (Directed Acyclic Graph) of its thought process, including failed DOM queries and fallback strategies.
2. **Structural Distillation**: The small local model is trained using sequence-to-sequence learning over these graph structures, internalizing the abstract states of web elements rather than specific HTML tags.

## 3. Advisory Application (Future System Integration)
For `Antigravity` agent evolution, we should stop relying purely on API calls for heavy web parsing. By employing an `Agent-as-Annotator` logic in our `.agents/laboratory/`, we can generate synthetic DOM failure trees constraint-optimized for 24GB VRAM models, transitioning web-tasks locally.

## 4. Deep Dive Implementation (Mathematics & Code)
**Synthetic DOM Tree Sequence Generation:**
The Teacher Agent explores a website and outputs a Directed Acyclic Graph (DAG) instead of a linear chat log. This DAG is serialized for Distillation.
```python
# Teacher Agent Annotated Output Format (Distilled to Local VLM)
distillation_dataset = [
    {
        "state_observation": "<html><button id='checkout'>...</html>",
        "action_tree": [
            {"action": "click(checkout)", "expected_state": "payment_screen"},
            {"fallback_action": "scroll(down)", "reason": "checkout_button_is_unclickable"}
        ],
        "reward_label": 1.0 # Successful endpoint
    }
]

def distill_agent_trajectory(small_model, dataset):
    """
    Train local 8B model to predict the entire tree topology (Action -> Fallback -> Resolution)
    rather than next-token predicting a single step.
    """
    optimizer = AdamW(small_model.parameters(), lr=2e-5)
...
```
*Note: By forcing the local model to predict `fallback_action` alongside the primary action, it gains the "meta-cognitive" structural reasoning that larger models naturally possess.*
