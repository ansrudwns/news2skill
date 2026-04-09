---
description: Self-critique mechanism to detect and fix potential vulnerabilities before outputting final results.
---
# Adversarial Verification Protocol

## Core Philosophy
An agent creating the code is inherently biased towards its success. To guarantee high quality, the agent must temporarily adopt the persona of a strict, adversarial reviewer.

## Execution Rules
1. **Phase Shift**: After writing the draft solution, pause. Switch your perspective to an "Adversarial Code Reviewer".
2. **Interrogation**: Ask yourself: "How could this code break?", "Are there obvious security flaws like missing auth checks?", "Does it loop infinitely?"
3. **Patch & Submit**: Before showing the user the final result, auto-correct the issues you found yourself.
