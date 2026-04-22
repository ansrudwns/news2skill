---
description: Advanced Hardware Optimization & Error Correction Protocols
---
# Inference_Optimizers: LPSR & EDEN

## Core Purpose
To operate safely and efficiently within the rigid 24GB VRAM constraint (`Hardware_Profile`), the system employs two core low-level optimization protocols located in `scripts/core/`:
1. **LPSR (Latent Phase-Shift Rollback)**: Detects reasoning hallucinations mid-generation.
2. **EDEN (TurboQuant Compression)**: Compresses the KV-cache to 3-bits using Randomized Hadamard Transforms, extending context windows mathematically.

## How to Utilize
- **LPSR (`scripts/core/lpsr.py`)**: When building custom autoregressive loops or chaining multiple LLM outputs, route the generation through `LPSR_Detector`. If `check_phase_shift` triggers, the engine will automatically truncate the corrupted KV cache and prompt a steering intervention.
- **EDEN (`scripts/core/eden_quant.py`)**: For highly parallelized `Fanout` modes (as defined in `Agentic_Aggregation`), wrap the context vector with `EDENQuantizer`. It dynamically computes optimal scale $S$ and compresses context representations, avoiding VRAM Out-of-Memory (OOM) errors.

## Defensive Guardrails
- **DO NOT** disable LPSR's entropy gating during complex multi-step reasoning. Reactive retries are inefficient; proactive detection saves compute.
- **EDEN Constraint**: Do not compress below 3-bits per coordinate; empirical laboratory testing (`test_eden.py`) bounds acceptable MSE at the 3-bit depth.
