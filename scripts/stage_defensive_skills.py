import os

files = {
    "draft_skill_Karpathy_Strict_Mode.md": """---
description: Suppress AI hallucination and over-engineering by enforcing minimal, surgical code modifications.
---
# Karpathy Strict Mode Protocol

## Core Philosophy
When modifying code or adding features, avoid speculative modifications. An agent should never preemptively refactor unrelated code or guess missing variables.

## Execution Rules
1. **Surgical Changes Only**: Do not modify even a single line of perfectly functioning adjacent code. Apply minimal, surgical edits to achieve the objective.
2. **No Hallucination**: Never guess the context or purpose of unknown variables/functions. If missing, pause and proactively ask the user.
3. **Conservative Verification**: When faced with multiple implementation paths, always choose the most conservative, readable, and simplest approach.
4. **Option-Aware Testing**: Do not blindly assume the patch will work. Explicitly list 3 edge cases (e.g., Null inputs, Out-of-bounds) and verify the logic against them before completion.
""",

    "draft_skill_Structured_Output_Forcer.md": """---
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
""",

    "draft_skill_Defensive_Fallback_Throttle.md": """---
description: Prevent infinite loops and 429 errors in asynchronous pipelines using backoffs and degradation.
---
# Defensive Fallback & Throttle Protocol (Ouroboros Defense)

## Core Philosophy
Naively constructed agent loops (Ouroboros anti-pattern) will retry failing actions indefinitely, exhausting API rate limits and completely halting the host server.

## Execution Rules
1. **Exponential Backoff**: On hitting 429 (Rate Limit) or 503 (Service Unavailable), never retry instantly. Calculate delay via `wait_time = (2 ** attempt) + jitter`.
2. **Max Retries & Degradation**: 
   - Break the loop forcefully after a maximum of 3 retries.
   - Do not throw an unhandled exception upon failure. Degrade the pipeline fallback immediately to a cheaper/faster heuristic (e.g., Regex fallback, Flash model, or returning default dummies).
3. **Hard Wall-Clock Timeout**: Every thread or agent logic MUST be enforced by an absolute execution deadline (e.g., `timeout=180` seconds). Kill the process upon breach and return partial data.
""",

    "draft_diary_Routing_Before_Thinking.md": """---
description: Optimize token expenditure by utilizing lightweight model routing before invoking heavy reasoning models.
---
# Routing Before Thinking (Routing First)

## Architectural Insight
Feeding massive datasets indiscriminately into heavy baseline models (like Opus or Pro) wastes tokens, slows down execution, and increases hallucination risks.

## Best Practices
1. **Interception Layer**: Place a highly lightweight rules-engine (Regex, Metadata) or a nano-model (Haiku/Flash) at the entry point of any multi-agent pipeline.
2. **Triage Classification**:
   - **Easy**: Resolve immediately using cache returns or simple string passes without heavy reasoning.
   - **Medium**: Route to a constrained worker with a heavily focused dataset segment.
   - **Hard**: Only escalate to the flagship reasoning model unconditionally when profound, generalized logic crafting is strictly demanded.
"""
}

def stage_files():
    staging_dir = os.path.join(".agents", "staging")
    os.makedirs(staging_dir, exist_ok=True)
    
    for filename, content in files.items():
        path = os.path.join(staging_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Staged: {path}")

if __name__ == "__main__":
    stage_files()
