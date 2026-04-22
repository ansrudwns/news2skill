---
description: Legacy migrated asset.
---
# Archive: INT4 Quantization Collapse Mechanisms
> Evaluator Score: 85/100 (Passed)

## Concept Overview
Recent evaluations into Post-Training Quantization (PTQ) methodologies reveal that assuming a well-converged FP32 continuous minimum is inherently stable under discrete INT4 space projections is mathematically flawed. Flat minima often suffer from quantization collapse, leading to rapid degradation of layer-wise outputs and compounding degradation in transformer residual streams.

## Mathematical Implication
If continuous parameters $w^*$ exist within a highly coupled subset of eigenvectors on the Hessian $H$, INT4 projection breaks the alignment of variance, causing irreversible distribution bias.

## Local Environment Application
For 24GB hardware constraints (`Hardware_Profile.md`), when deploying LLMs (e.g., Gemma 4 variants):
1. Avoid naive scaling factors. Apply orthogonal clipping before quantization.
2. Ensure low-rank adapter (LoRA) compensators dynamically re-scale outlier weights.
3. Keep embeddings and normalization layers in FP16/BF16, solely quantizing projection dense layers.
