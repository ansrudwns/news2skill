---
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
