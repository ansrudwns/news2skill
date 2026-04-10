import random

def dummy_slm_generate_candidate():
    """Simulates an SLM hallucinating math equations. 10% chance to be perfectly correct."""
    is_correct = random.random() < 0.10
    if is_correct:
        return {"reasoning_path": "Let's think step by step...", "answer": 42, "is_valid": True}
    return {"reasoning_path": "I think the answer is...", "answer": random.randint(1, 100), "is_valid": False}

def external_verifier_tool(candidate):
    """Simulates the Formal Verifier Tool (Rule-based)."""
    # In reality, this would run Python code or a math solver.
    return candidate["is_valid"]

def test_time_compute_scaling(compute_budget_N):
    print(f"\n[Test-Time Compute N={compute_budget_N}] Starting generation...")
    candidates = []
    
    # Phase 1: Generation (Scaling compute)
    for i in range(compute_budget_N):
        candidates.append(dummy_slm_generate_candidate())
        
    # Phase 2: Tool-Integrated Verification
    for idx, c in enumerate(candidates):
        if external_verifier_tool(c):
            print(f" -> Candidate {idx+1}/{compute_budget_N} Verified SUCCESS! Returning Answer: {c['answer']}")
            return True
            
    print(f" -> ALL {compute_budget_N} Candidates FAILED.")
    return False

if __name__ == "__main__":
    print("=== T1: Scaling Test-Time Compute in SLMs (Toy Simulation) ===")
    random.seed(2026)
    
    budgets = [1, 5, 10, 50]
    results = {}
    
    for N in budgets:
        success = test_time_compute_scaling(N)
        results[N] = success
        
    print("\n=== Empirical Results ===")
    for N, success in results.items():
        print(f"Compute Budget N={N:2d} -> Accuracy: {'100%' if success else '0%'}")
