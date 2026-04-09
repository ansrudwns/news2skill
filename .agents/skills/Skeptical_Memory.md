---
description: Ensure factual accuracy by actively verifying system state before making code modifications.
---
# Skeptical Memory Protocol

## Core Philosophy
Agent context windows can become stale. Trusting your current context implicitly leads to regressions and hallucinations. Memory is merely a hint; the file system is the ground truth.

## Execution Rules
1. **Never Assume Code State**: Before you patch or overwrite a file, NEVER assume you remember its exact lines.
2. **Explicit Verification**: You MUST use your local file-reading tools (`view_file`, `cat`, or `grep_search`) to check the current logic directly before writing.
3. **Zero-Trust**: Treat previous conversation history as potentially outdated. Verify right before action.
