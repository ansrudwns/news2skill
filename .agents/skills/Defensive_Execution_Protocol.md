---
description: Ensure robust payload exchanges, terminate infinite loops, and aggressively enforce fallback paradigms.
---
# Defensive Execution Protocol

## Core Philosophy
Naively constructed agent loops (Ouroboros anti-pattern) will retry failing actions indefinitely, exhausting API rate limits and completely crash the thread. This unified protocol physically enforces loop termination, deterministic JSON constraints, and loud observability via "Dummy" fallbacks.

## Execution Rules

### 1. Loop Termination & Exponential Backoff
- **Exponential Backoff**: On hitting 429 (Rate Limit) or 503 (Service Unavailable), never retry instantly. Calculate delay via `wait_time = (2 ** attempt) + jitter`.
- **Max Retries**: Break the loop forcefully after a maximum of 3 retries to prevent runaway daemon execution.
- **Hard Wall-Clock Timeout**: Every threaded agent logic MUST be constrained by an absolute execution deadline (e.g., `timeout=180` seconds). Kill the process upon breach to prevent thread freezing.

### 2. Output Forcing & The Regex Contradiction Rule
- **Never Parse LLM Output with Regex**: Relying on standard Regex or Markdown block parsing to capture natural language from an LLM causes catastrophic downstream errors. ALWAYS utilize the official JSON Response Schema of the overarching API.
- **When is Regex Permitted?**: You are strictly permitted to use regex *ONLY* as a fallback heuristic *instead* of an LLM. If the LLM API is breached or 429 limited and retries are exhausted, degenerate the pipeline to a cheaper, deterministic regex/string-matching function to extract logic rather than freezing the task.

### 3. Graceful Dummy Returns (Thread Survival)
- Wrap all volatile API interactions in a `try-except` block.
- **Defensive Dummy Return**: If the schema breaks or timeouts occur, NEVER throw a raw, unhandled `Traceback` that crashes the parent thread. Immediately return a safe dummy fallback payload that matches the expected dict signature (e.g., `{"status": "FAIL", "data": "timeout_dummy"}`).

### 4. Telemetry & Observability (Langfuse Philosophy)
- **Silent Success, Loud Failure**: Dummy returns ensure the pipeline compiler stays quiet and survives, but you MUST forcefully alert the human operator of the exact failure.
- Whenever a Dummy payload is emitted and handled, simultaneously log an aggressive asynchronous warning (a "Loud Failure") into an independent `failed_items_queue.json` or `.log` file detailing the specific chunk ID and failure reason. Do not bury the failure in standard outputs.

### 5. Visual Telemetry (Popup Dashboard Caching)
- **Conflict Resolution (vs Blocking_Budget.md)**: While autonomous background actions generally must not block the user's GUI, long-running ML training or heavy computation tasks are an explicit EXCEPTION. To prevent human anxiety (Opaque Execution), you MUST aggressively spawn front-end visual popups.
- **Protocol**: When executing long tasks autonomously via terminal, strictly utilize `Start-Process powershell -NoExit -Command ...` to pop up an interactive real-time monitoring dashboard on the user's physical desktop.
- **Dual Logging (Prevent Blindness)**: Because the Popup detaches stdout from the agent's pipe, the executed Python script MUST universally import the `logging` module configured with BOTH a `StreamHandler` (for the human popup) and a `FileHandler` (for the Agent to read logs natively). Never rely on print statements alone.
- **Anti-Zombie Garbage Collection**: Never let popup windows replicate infinitely. Before spawning a retry popup during failure loops, you MUST automatically detect and kill the previous hanging terminal session (Auto-kill) and manage `.flag` files to synchronize agent polling.
