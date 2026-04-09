---
name: LiteLLM_Fallback_Routing
description: Zero-downtime offline (Local LLM) fallback network routing rules.
track: A
score: 98
---

# LiteLLM Offline Fallback Routing

## Overview
This skill implements a 100% zero-downtime fallback routing constraint. Rather than basic cost optimization, it dictates that the agent MUST utilize local hardware (Gemma 4 9B GGUF) immediately when Cloud API outages occur.

## System Constraints (Hardware Baseline)
*   **Target Device:** `AMD Ryzen AI 5 340`, `24GB RAM`
*   **Optimization Backend:** `llama.cpp` + `Vulkan Acceleration (Radeon 840M)` MUST be supported.

## Strict Execution Rules
1.  **Proxy Config Initialization:** Do NOT manually write Python Try-Catch blocks for fallback. You MUST spawn the proxy port exclusively using the `litellm --config config.yaml` command.
2.  **Chain Configuration:**
    *   Primary (`primary`): GPT-4o / Claude 3.5 (Cloud API)
    *   Secondary (`fallback`): `ollama/gemma-4-9b-gguf-vulkan` (Local Inference)
3.  **Fallback Trigger:** If the Primary API fails to respond within 3 seconds or returns `RateLimitError (429)`, immediately toss the payload to the local fallback.
4.  **Privacy Air-Gap:** If processing sensitive security files or PII (Personally Identifiable Information), you MUST completely bypass the Primary API and force the pipeline to use ONLY the Secondary Local Node.
