---
name: AgentTrace_Telemetry_Integration
description: Agent self-healing (Reflexion) and OTel system logging integration.
track: A
score: 96
---

# Agent Telemetry & Reflexion Logger

## Overview
This skill forces the integration of OTel middleware to establish a Reflexion mechanism, allowing the agent to continuously evolve by asking "Why did I fail?" and storing the answers via Langfuse telemetry.

## Strict Execution Rules
1.  **OTel Middleware Injection:** Immediately prior to any core LLM inference execution, you MUST prioritize setting up and importing the OpenTelemetry wrapper (e.g., `Langfuse`).
2.  **Failure Telemetry Capture:** If an `Exception` occurs or the payload is rejected by `Adversarial_Verification` (Score < 80), do NOT simply perform a generic Retry. You MUST format the Trace ID and the raw prompt, and push the failure log to the telemetry server.
3.  **Cross-Session Inheritance:** Upon receiving a new task, you MUST check the local workspace for an `error_remediation.md` file. If it exists, you MUST ingest it as the top-priority System Prompt to prevent repeating historical mistakes.
