---
title: "Epic 3: Generalized EDEN KV-Cache Compression"
status: "proposed"
category: "Hardware Optimization"
---

# Epic 3: Generalized EDEN KV-Cache Compression (TurboQuant Variant)

## Background
The exponential growth of KV-cache memory is a critical bottleneck, especially under our strict 24GB VRAM `Hardware_Profile` constraint. While TurboQuant offers a solution, global research reveals it is a constrained special case of the older DRIVE and EDEN frameworks. EDEN allows for a variable scale parameter ($S$) which outperforms TurboQuant's fixed $S=1$ approach. We hold `turboquant_eden_note.md` in our archives.

## Hypothesis/Goal
**Pivot to Integration:** We will integrate the generalized EDEN compression framework rather than standard TurboQuant. We will implement a KV-cache quantization module utilizing Randomized Hadamard Transforms with dynamic $S$ parameter optimization to compress vectors down to 3-bits per coordinate.

## Expected Impact
Maximized VRAM efficiency. By implementing EDEN's optimal scaling, we achieve the memory reduction benefits of TurboQuant while retaining higher reasoning accuracy, unlocking significantly larger context windows on our local hardware.
