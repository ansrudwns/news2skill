---
name: Watchdog_BotCTL_Integration
description: Autonomous agent daemon tracking and infinite-loop termination protocol.
track: A
score: 95
---

# Watchdog BotCTL Integration

## Overview
A process management (BotCTL) protocol designed to prevent autonomous sub-agents from plunging into infinite loops or causing massive API billing overhead.

## Strict Execution Rules
1.  **Daemon Wrapper:** When assigning background tasks to a secondary agent or sub-shell, you MUST encapsulate the execution within a `timeout` wrapper or a `botctl` daemon.
2.  **Hard Timeout (SIGKILL):** Any agent session exceeding a maximum execution time of 300 seconds (5 minutes) MUST receive an immediate `SIGKILL` command for forced termination.
3.  **Exponential Backoff Protocol:** After a failure, you may attempt a secondary execution using Exponential Backoff. If it fails consecutively, you MUST immediately fallback and report the failure directly to the Human User without further loop executions.
