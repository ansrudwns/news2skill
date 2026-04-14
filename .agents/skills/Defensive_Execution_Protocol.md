---
description: "Ensure robust payload exchanges, terminate infinite loops, and aggressively enforce fallback paradigms."
---
# Defensive Execution Protocol

## Core Philosophy
Naively constructed agent loops (Ouroboros anti-pattern) will retry failing actions indefinitely, exhausting API rate limits and completely crash the thread. This unified protocol physically enforces loop termination, deterministic JSON constraints, and loud observability via "Dummy" fallbacks.

## Execution Rules

### 1. Loop Termination & Exponential Backoff
- **Exponential Backoff**: On hitting 429 (Rate Limit) or 503 (Service Unavailable), never retry instantly. Calculate delay via `wait_time = (2 ** attempt) + jitter`.
- **Max Retries**: Break the loop forcefully after a maximum of 3 retries to prevent runaway daemon execution.
- **Hard Wall-Clock Timeout & Foreground Exceptions**: Every background threaded agent logic MUST be constrained by a timeout. For **GEAR 5 (RESEARCH MODE) Operations**, these are treated as "Scoped Foreground Exceptions" to safely override the 15-second background blocking budget. The default hard timeout for these foreground tasks is **180 seconds** unless the user explicitly approves an extension. Longer runs must declare expected duration, log paths, and a cancellation method upfront.

### 2. Output Forcing & The Regex Contradiction Rule
- **Never Parse LLM Output with Regex**: Relying on standard Regex or Markdown block parsing to capture natural language from an LLM causes catastrophic downstream errors. ALWAYS utilize the official JSON Response Schema of the overarching API.
- **When is Regex Permitted?**: You are strictly permitted to use regex *ONLY* as a fallback heuristic *instead* of an LLM. If the LLM API is breached or 429 limited and retries are exhausted, degenerate the pipeline to a cheaper, deterministic regex/string-matching function to extract logic rather than freezing the task.

### 3. Graceful Dummy Returns (Thread Survival)
- Wrap all volatile API interactions in a `try-except` block.
- **Defensive Dummy Return**: If the schema breaks or timeouts occur, NEVER throw a raw, unhandled `Traceback` that crashes the parent thread. Immediately return a safe dummy fallback payload that matches the expected dict signature (e.g., `{"status": "FAIL", "data": "timeout_dummy"}`).

### 4. Telemetry & Observability (Langfuse Philosophy)
- **Silent Success, Loud Failure**: Dummy returns ensure the pipeline compiler stays quiet and survives, but you MUST forcefully alert the human operator of the exact failure.
- Whenever a Dummy payload is emitted and handled, simultaneously log an aggressive asynchronous warning (a "Loud Failure") into an independent `failed_items_queue.json` or `.log` file detailing the specific chunk ID and failure reason. Do not bury the failure in standard outputs.
- **<CRITICAL_OVERRIDE - DIALECTIC TENTATIVE RECOVERY>**: LLM agents suffer from "Task Completion Bias" (silently swallowing errors to finish the task). You are STRICTLY FORBIDDEN from silently bypassing errors. However, you should not just freeze. If an error occurs: 
  1) **HALT** the primary execution pipeline. 
  2) **Investigate**: Autonomously perform web searches, read documentation, or trace logs to understand the root cause. 
  3) **Propose & Discuss**: Present a concise "Post-Mortem & Recovery Plan" to the user. Explain the error, share your research findings, and propose alternate routes. 
  4) **Wait for clearance**: Wait for the user's approval or engage in discussion before attempting the new patch.

### 5. Visual Telemetry (Popup Dashboard Caching)
- **User-Approved Popups**: While background actions must not block the user's GUI, heavy computation tasks might benefit from visual tracking. However, you MUST NOT spawn front-end visual popups without **Explicit User Approval**.
- **Protocol**: When approved by the user, utilize `Start-Process powershell -NoExit -Command ...` to pop up an interactive real-time monitoring dashboard.
- **Dual Logging (Prevent Blindness)**: Because the Popup detaches stdout, the executed script MUST universally import `logging` with BOTH a `StreamHandler` (for the popup) and a `FileHandler` (for the Agent to read logs natively). Never rely on print statements alone.
- **Anti-Zombie Garbage Collection**: Never let popup windows replicate infinitely. Before spawning a retry popup, you must clear the previous hanging session. However, you are **STRICTLY PROHIBITED** from using generic `kill` commands based on process names. You MUST exclusively use deterministic **PID file ownership validation** to prove you spawned the process before terminating it.
