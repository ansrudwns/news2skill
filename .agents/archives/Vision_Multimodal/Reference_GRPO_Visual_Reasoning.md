---
description: "Reference Archive: Improving Visual Spatial Reasoning in Multimodal Language Models via Constrained Policy Optimization (Faithful GRPO)"
tags: [GRPO, Reinforcement Learning, VLM, Spatial Reasoning, Optimization]
---

# Faithful GRPO: Vision-Language Model Spatial Reasoning

## 1. Core Bottleneck
Multimodal reasoning models (MRMs) trained with Reinforcement Learning with Verifiable Rewards (RLVR) suffer from "reward hacking" or inaccurate policy optimization when dealing with spatial bounds. Models learn the statistical heuristics of spatial reasoning rather than faithful physical geometry.

## 2. Algorithmic Paradigm
**Faithful GRPO (Group Relative Policy Optimization):**
Unlike standard PPO, GRPO eliminates the need for an explicit value network by dynamically estimating the baseline from a relative group of policy trajectories. 
1. **Constrained Policy Optimization**: It penalizes the RL algorithm when the sequence of reasoning steps contradicts the visual ground truth constraints.
2. **Reward Function Design**: Rewards are structured non-linearly to grant partial credit for accurate spatial geometric mapping before the final answer is produced.

## 3. Advisory Application (Future System Integration)
When scaling our `LaCT_Spatial_Memory` or any visual integration for the `Antigravity` agent, we must implement GRPO instead of simple SFT for spatial reasoning. By bypassing the value-network overhead, we can train locally under 24GB VRAM while preventing hallucinations in spatial coordinates.

## 4. Deep Dive Implementation (Mathematics & Code)
**Lagrangian Dual Ascent for Constrained GRPO:**
Instead of simple scalar rewards, FGRPO introduces explicit logical and grounding constraints via the Lagrangian multiplier $\lambda$.
```python
def fgrpo_loss(policy_logprobs, ref_logprobs, advantages, constraint_violations, lambda_multiplier):
    # Standard GRPO clipped ratio
    ratio = torch.exp(policy_logprobs - ref_logprobs)
    clipped_ratio = torch.clamp(ratio, 1 - epsilon, 1 + epsilon)
    
    # 1. Base Advantage Optimization
    base_loss = -torch.min(ratio * advantages, clipped_ratio * advantages)
    
    # 2. Lagrangian Dual Ascent Constraint (The 'Faithful' part)
    # If a trajectory violates spatial logic or visual grounding, penalty scales dynamically.
    constraint_penalty = lambda_multiplier * constraint_violations
    
    final_loss = base_loss + constraint_penalty
    return final_loss.mean()
```
*Note: The $\lambda$ modifier adaptively increases during training steps if the VLM hallucinates a bounding box that contradicts the source visual patch.*
