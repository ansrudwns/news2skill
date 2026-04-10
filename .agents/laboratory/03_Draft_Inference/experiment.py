import time
import random

def slow_target_model(token):
    """Simulates a heavy 70B parameter model taking 50ms per token."""
    time.sleep(0.05)
    return True # Golden Truth Generator

def fast_draft_model(num_tokens):
    """Simulates a tiny 1B target drafting tokens instantly."""
    return [True] * num_tokens # Guesses

def simulate_standard_autoregressive(tokens_to_generate=20):
    start = time.time()
    for _ in range(tokens_to_generate):
        slow_target_model(1)
    return time.time() - start

def simulate_speculative_decoding(tokens_to_generate=20, draft_length=4, acceptance_rate=0.7):
    start = time.time()
    tokens_generated = 0
    
    while tokens_generated < tokens_to_generate:
        # Fast model drafts N tokens instantly
        draft = fast_draft_model(draft_length)
        
        # Slow model evaluates all N drafted tokens in parallel (1 forward pass)
        time.sleep(0.05) # Parallel verification takes same time as 1 token
        
        # Determine how many drafted tokens were actually correct
        accepted = 0
        for _ in draft:
            if random.random() < acceptance_rate:
                accepted += 1
            else:
                break
                
        # We always get at least 1 token (the one explicitly generated upon rejection)
        tokens_generated += (accepted + 1)
        
    return time.time() - start

if __name__ == "__main__":
    print("=== Draft-Based Speculative Decoding (Toy Simulation) ===")
    random.seed(42)
    
    std_time = simulate_standard_autoregressive(30)
    print(f"1. Standard Autoregressive Generation (30 tokens) : {std_time:.2f} seconds")
    
    # Simulate high acceptance rate (e.g. drafting common code or text)
    spec_time_high = simulate_speculative_decoding(30, draft_length=4, acceptance_rate=0.8)
    print(f"2. Speculative Decoding (80% Draft Accept Rate)   : {spec_time_high:.2f} seconds")
    
    # Simulate low acceptance rate 
    spec_time_low = simulate_speculative_decoding(30, draft_length=4, acceptance_rate=0.2)
    print(f"3. Speculative Decoding (20% Draft Accept Rate)   : {spec_time_low:.2f} seconds")
    
    print(f"\n-> Theoretical Speedup limit: {std_time / spec_time_high:.2f}x faster using Draft Models!")
