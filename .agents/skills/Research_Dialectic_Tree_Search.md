---
description: "[RESEARCH MODE] Production-Ready v1 Guarded Research Orchestrator. Master entry point governing all benchmarking, dialectic synthesis, and formal verification when Gear 5 is activated."
---
# Research: Dialectic Tree Search Orchestrator

## Trigger Condition
**[GEAR 5 (RESEARCH MODE)] Only triggers during hackathons, algorithm design, or tasks demanding absolute logical proof. For deterministic automation, use Gear 1.**

## V1 Mandatory Sandbox Guardrails
The Orchestrator strictly enforces these 5 cardinal rules across all sub-modules:

1. **AST & Runtime Execution Vault**
   - **AST Allowlist**: `math, random, statistics, itertools, functools, collections, heapq, bisect, decimal, fractions`, plus bounded `numpy` (if installed).
   - **Hard Deny**: All other imports, filesystem I/O (`open/write/delete`), networks (`socket`, `requests`), shell execution (`subprocess`, `os.system`), dynamic evaluation (`eval`, `exec`, `compile`, `globals`).
   - **Runtime Enforcer**: Code must NEVER be executed directly via Python. You MUST execute candidate code via `.agents/laboratory/sandbox_runner.py <file>` to physically enforce AST blocking, hard timeouts (e.g., 10s-180s), and stdout truncation limits.
2. **Determinism in Randomness**
   - Benchmarks requiring randomness MUST declare and utilize a fixed deterministic seed for reproducible empirical comparisons.
3. **Numpy Operations Limit**
   - Numpy is restricted exclusively to in-memory numeric operations. Loading files (`np.load`, `np.save`), memmap, and unbounded multidimensional object allocation are strictly blocked.
4. **Knowledge Primary Source Hierarchy**
   - Blogs and SEO articles are strictly "discovery aids." 
   - Canonical truth used to patch local archives MUST be grounded in Primary Sources (Official docs, arXiv papers, verified source code).
5. **Score & Scopes Division**
   - **Sandbox Phase**: Code is restricted to the sandbox limits.
   - **Production Integration**: Winning code receives Workspace-Write privileges under non-destructive edits and `Karpathy_Strict_Mode`. Destructive operations still require Explicit User Approval.

---

## 5-Phase Dialectic Execution Flow

The Orchestrator orchestrates the following sequential sub-modules:

* **Phase 1: Candidate Generation (Multi-branch)**
  - Sub-module: `.agents/skills/Research_Progressive_Tree_Search.md`
  - Generates 3-5 distinct, conceptually varied theoretical implementations.
* **Phase 2: Toy Sandbox Benchmark (Physical Execution)**
  - Sub-module: `.agents/skills/Research_Toy_Sandboxing.md`
  - Subjects candidates to physical measurement using edge-case inputs via `sandbox_runner.py`.
* **Phase 3: Adversarial Critique (Weakness Analysis)**
  - Sub-module: `.agents/skills/Adversarial_Verification.md`
  - Analyzes the sandbox traceback metrics to ruthlessly expose time-complexity limits, structural flaws, or logical holes in each branch.
* **Phase 4: Synthesis (Dialectic Fusion)**
  - Sub-module: `.agents/skills/Iterative_Dialectic_RAG.md`
  - Fuses the strengths of the branches. Hard constraints: Max Retries (2), Max Pivots (2) before requesting Human Guidance.
* **Phase 5: Formal Verification (Production Readiness)**
  - Sub-module: `.agents/skills/Research_Formal_Verifier.md`
  - Final mathematical/structural confirmation prior to production integration.
