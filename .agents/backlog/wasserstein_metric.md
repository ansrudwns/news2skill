---
description: Concept for fixing tensor drift in quantized GGUF models via Wasserstein metric W1
score: 75 (Lacks actionable determinism without specific PyTorch scripts)
---
# Wasserstein Metric GGUF Quantization

## Overview
Replaces Kullback-Leibler divergence with the Wasserstein metric to detect and correct `ssm_conv1d` tensor drift during aggressive LLM quantization (e.g., INT4/INT3).

## Hypothesis
W1 metric better handles disjoint distribution overlaps, providing vastly improved numerical stability detection.

## Required Future Action
Synthesize and implement tensor calibration functions in `scripts/` using W1 distances before promoting to an active Track A skill.
