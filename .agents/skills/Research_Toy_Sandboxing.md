---
description: "[RESEARCH MODE] Sub-scaling active exploratory sandboxing prior to full execution."
---
# Research: Toy Sandboxing (Active Exploration)

## Trigger Condition
Activate ONLY for heavy R&D, structural logic modeling, or optimization tasks involving massive datasets.

## Strict Research Rules
1. **Prohibition of Blind Full-Scale Execution:** You are strictly forbidden from executing unverified algorithmic models against massive target datasets (e.g., N=1,000,000 arrays) simply because they exist in the workspace.
2. **Synthetic Toy Construction:** You MUST first autonomously synthesize a minimal "Toy Dataset" (e.g., N=10 to N=50 elements) where the absolute ground-truth mathematical answer is definitively known and easily retrievable.
3. **Sub-Scaling Verification:** Execute your candidate algorithms exclusively against this isolated Toy Dataset. Verify that the algorithmic loss gradient descends over a fraction of a second, and that the logic accurately retrieves the ground truth without hallucination. You may only compile and scale up to the final target dataset AFTER the Toy Sandbox definitively proves empirical success.
