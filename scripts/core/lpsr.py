import numpy as np
from typing import List, Tuple, Dict, Any

class LPSR_Detector:
    """
    Latent Phase-Shift Rollback (LPSR) Detector.
    Monitors residual stream vectors and token entropies to detect inference reasoning errors.
    """
    def __init__(self, cos_sim_threshold: float = 0.5, entropy_threshold: float = 2.0):
        self.cos_sim_threshold = cos_sim_threshold
        self.entropy_threshold = entropy_threshold
        
    def check_phase_shift(self, prev_residual: np.ndarray, curr_residual: np.ndarray, current_entropy: float) -> bool:
        """
        Dual-gate detection logic:
        A phase shift (reasoning error) is detected if:
        1. The direction of the residual vector changes sharply (Low Cosine Similarity).
        2. The model is highly uncertain about the token (High Entropy).
        """
        # Calculate cosine similarity
        norm_prev = np.linalg.norm(prev_residual)
        norm_curr = np.linalg.norm(curr_residual)
        
        if norm_prev == 0 or norm_curr == 0:
            cos_sim = 1.0 # Safe default
        else:
            cos_sim = np.dot(prev_residual, curr_residual) / (norm_prev * norm_curr)
            
        # Dual-gate check
        if cos_sim < self.cos_sim_threshold and current_entropy > self.entropy_threshold:
            return True
            
        return False

class MockAutoregressiveDecoder:
    """
    Simulates an LLM autoregressive generation loop with a KV Cache.
    """
    def __init__(self, detector: LPSR_Detector):
        self.detector = detector
        # Simulated KV Cache: just storing the generated "tokens" (strings for mock)
        self.kv_cache: List[str] = []
        
        # We store the residual vectors of the critical layer to compare step (t) with (t-1)
        self.residual_history: List[np.ndarray] = []
        
    def generate_step(self, token: str, residual_vector: np.ndarray, token_entropy: float) -> bool:
        """
        Processes one generation step. Returns True if a phase-shift was detected and a rollback occurred.
        """
        # Check for phase shift if we have history
        if len(self.residual_history) > 0:
            prev_residual = self.residual_history[-1]
            if self.detector.check_phase_shift(prev_residual, residual_vector, token_entropy):
                self._apply_rollback_and_steering()
                return True # Rollback triggered
                
        # Normal path: append to KV cache and history
        self.kv_cache.append(token)
        self.residual_history.append(residual_vector)
        return False
        
    def _apply_rollback_and_steering(self):
        """
        Simulates rolling back the KV cache to the state before the phase shift,
        and injecting a steering vector.
        """
        # Rollback: truncate the last step of history and cache (the step leading to the error)
        if len(self.kv_cache) > 0:
            self.kv_cache.pop() # Remove the previous token that led to this bad state
            self.residual_history.pop()
            
        # Simulated Steering: We append a special steering marker to the cache
        # In a real LLM, we would modify the actual KV tensors at a specific layer.
        self.kv_cache.append("<STEERING_CORRECTION>")
        
        # Append a mock corrected residual
        self.residual_history.append(np.ones(5))
