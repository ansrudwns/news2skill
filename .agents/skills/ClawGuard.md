---
description: Runtime boundary shield against indirect prompt injection — sanitizes MCP/web payloads with aggressive regex at the tool_call input boundary, the only place regex is permitted under DSP Rule 2.
---
# ClawGuard: Runtime Boundary Shield against Indirect Prompt Injection

## Definition
A security interceptor placed at the exact boundary of `tool_call` execution. Restricts arbitrary MCP exploits or malicious repository codes from manipulating the primary LLM logic layer.

## Mechanism
1. **Pre-execution Filtering**: Instantiates input sanitization leveraging stringent regex or lightweight semantic checks directly evaluating fetched MCP payloads or web contexts prior to LLM intake.
2. **Deterministic Halt**: If forbidden keywords (e.g., `delete-all`, unexpected `<override>` injection tags) are detected, ClawGuard blocks the tool execution natively and triggers defensive Dialectic Recovery.

## Tuning & Integration (Defensive_Execution_Protocol)
- **Regex Boundary Clarification**: As per DSP Rule 2, output generation parsing via regex remains strictly forbidden. However, ClawGuard is explicitly granted permission to use aggressive Regex ONLY at the `INPUT` validation boundary (e.g., sanitizing MCP returns) to shield the LLM from executing injected malicious commands.

## Implementation Path
A critical necessity for `Karpathy_Strict_Mode`. Score: 88/100 (Pass)
