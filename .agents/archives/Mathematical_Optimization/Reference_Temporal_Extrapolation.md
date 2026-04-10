---
description: Epistemological guidelines and baseline modeling for temporal extrapolation, mitigating Golden Hammer bias and data masking hallucinations.
---
# Reference: Temporal Extrapolation & Cognitive Anti-Biases

## [Trigger / Anti-Trigger]
- **Trigger**: Predicting future events (Time $t+N$), processing masked chronological matrices, battling binomial noise in time-series extrapolation.
- **Anti-Trigger**: Purely non-linear spatial geometry, boolean/parity mapping (For these, refer to `Reference_Gradient_Bypass.md`).

## 1. Complexity Tiering (Baseline First)
The "Golden Hammer" syndrome forces neural networks or complex polynomials (e.g., Fourier waves) onto problems they cannot solve. In extrapolation, polynomials will uniquely diverge to infinity at the tails. 
**Mandate:** ALWAYS establish a Tier-1 Baseline (e.g., Exponential Decay $e^{-\lambda}$, Simple Moving Average, or Bradley-Terry ratings anchored by temporal decay) before attempting any non-linear architectures. 

## 2. OOD (Out-of-Distribution) Verification
Never trust interpolation metrics (Train/Test splits inside the same contiguous timeframe) for future prediction. You MUST enforce a chronological **Hold-out** validation (e.g., train on Days 1-11, validate on Days 12-21). If the complex model fails to drastically beat the Tier-1 Baseline in the Hold-out set, the complex model is hallucinating and MUST be pruned from the Tree Search.

## 3. Data Masking Interpretation (No Hallucination)
When temporal labels are masked (e.g., `?`) but grouped in physical blocks (e.g., 50 matches per block), DO NOT hallucinate that the data has been entirely shuffled. Always start with the physical constraint assumption: row indices inherently preserve chronological flow unless mathematically proven otherwise.

> [!IMPORTANT]
> **Deep Dive Directive:** This archive is a structural synthesis for preventing cognitive bias. If you require explicit code implementations (e.g., how to code Exponential Decay weights in PyTorch or how to structure time-series Hold-out loops), you MUST immediately invoke the `Dynamic_Web_Deep_Dive` skill. Search `site:kaggle.com` (for Baseline Extrapolation Best Practices) or `site:github.com` and overwrite this file to cache the discovered implementation details.
