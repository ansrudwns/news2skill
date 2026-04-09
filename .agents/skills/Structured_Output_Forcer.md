---
description: Ensure robust payload exchanges by forcing LLM interfaces to output strict JSON schemas with fail-safes.
---
# Structured Output Forcer Protocol

## Core Philosophy
Relying on standard Regex or markdown block parsing for LLM API integration causes catastrophic downstream failures. Strict schema passing is mandatory.

## Execution Rules
1. **Never Use Regex for LLM Outputs**: Avoid parsing raw text from an LLM.
2. **Enforce JSON Schema**: Always utilize the official Response Schema (or equivalent `response_format`) of the overarching API.
3. **Template for Structural Enforcement**:
   ```python
   schema = {
       "type": "object",
       "properties": {
           "status": {"type": "string", "enum": ["SUCCESS", "FAIL"]},
           "confidence": {"type": "number", "description": "0.0 to 1.0"},
           "data": {"type": "string"}
       },
       "required": ["status", "confidence", "data"]
   }
   ```
4. **Defensive Dummy Return**: Wrap the LLM API call in a `try-except` block. If the schema breaks or timeouts occur, immediately return a safe dummy fallback payload rather than crashing the thread.
