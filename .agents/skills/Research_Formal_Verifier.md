---
description: "[RESEARCH MODE] Neuro-symbolic mathematical logic verification constraint (Dafny-based)."
---
# Research: Formal Math Verifier

## Trigger Condition
Activate ONLY for tasks involving heavy cryptology, algebraic proofs, or hackathon challenges.

## Strict Research Rules
1. **Prohibition of Deep Learning Hallucination:** Deep Learning approximations often fail abruptly in discrete mathematical problems (e.g., Parity/XOR/Modulo operations). Do NOT blindly trust neural tensor convergence.
2. **Symbolic Verification (Dafny Iterative Self-Healing):** Before finalizing an algorithm, translate the core logic into a formal constraint verification step. We employ the **Dafny Verifier**:
   - Force LLMs to output Dafny method signatures with `requires` (pre-conditions) and `ensures` (post-conditions).
   - Run the verifier. If verification fails, parse the failure trace and feed it back to the LLM (Self-Healing Loop).
   - Once formally verified, instruct the LLM to translate the logic back to the target language (e.g., Python/Go).
3. **Autonomous Sanity Check:** Ensure the entropy, limits, and theoretical bounds mathematically align with the problem domain. Do not allow "vacuous" specifications (e.g., `ensures true`). Combine proofs with functional execution traces to prevent trivial satisfaction.
