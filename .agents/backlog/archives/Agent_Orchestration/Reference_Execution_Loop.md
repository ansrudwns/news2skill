---
description: Implement robust error loops and Ouroboros logic for python execution.
tags: [Loop, Python, Ouroboros, Autonomy]
---

# Epic 4: Critical Execution Loop (Test-Driven AI)

## 📌 Goal
To structurally eradicate the "Satisficing / Hallucination" phenomenon (where the agent guesses code and exits without testing). This epic integrates 4 absolute constraints into the framework’s core logic. It upgrades the agent from a conversational assistant into an authoritative **HPC-driven Senior Engineer**.

## ⚙️ Core Architecture Fixes

### 1. Empirical Validation Protocol
- **Symptom:** The agent assumes correctness without testing ("This formula seems correct").
- **Architectural Constraint:** The agent is strictly prohibited from finalizing logic purely via internal latent tensor calculations. If a hypothesis is formed, the agent MUST invoke `run_command` to execute the Python script / training loop, physically inspecting the terminal output loss convergence before yielding the final response.

### 2. Lower-Bound Mathematical Proofing
- **Symptom:** Ignoring inherent structural limitations of models (e.g., assuming a 1-layer transformer can solve recursive operations).
- **Architectural Constraint:** Before initiating architecture design, the agent must leverage the `<thinking>` scratchpad to mathematically prove: **"What is the theoretical minimal time-complexity *O(N)* required for this operation?"** If the proposed solution violates the mathematical lower bound, the hypothesis is autonomously dropped.

### 3. HPC Mindset Enforcement (Anti-Satisficing)
- **Symptom:** Satisficing with a 30-second brute-force execution and abandoning scalability.
- **Architectural Constraint:** When writing iterators, the default assumption must NOT be the native Python `for` loop. The agent must default to utilizing maximal hardware concurrency (e.g., `Multiprocessing`, C/C++ FFI, or `Numba` JIT Compilation). The system violently enforces uncompromised computational scale.

### 4. Monolithic Reproducibility (E2E Validation)
- **Symptom:** Returning fragmented functions or skipping critical training loops with comments like `... # your code here`.
- **Architectural Constraint:** Every script response MUST be a complete, end-to-end monolithic script. Copying and pasting line 1 to EOF must perfectly execute the entire pipeline without human modification. Violation of this rule triggers internal penalty heuristics.
