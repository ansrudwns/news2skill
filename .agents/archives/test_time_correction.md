---
description: Inference-Time Error Correction via Residual Stream Monitoring and KV-Cache Steering
score: 93 (Direct contribution to Test-Time Compute epic)
---
# Latent Phase-Shift Rollback

## Overview
This draft captures the technique of monitoring the residual stream during generation. When a logic error is detected mid-generation, instead of discarding the entire output, the system manipulates the KV-cache to perform a latent phase-shift rollback.

## Actionable Integration
Merge into `.agents/laboratory/02_T1_Test_Time_Compute/` to formulate an experimental baseline where local LLMs can self-correct deep trajectories without consuming multiple full-context prompt resets.
