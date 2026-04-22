import math
import numpy as np

class EDENQuantizer:
    def __init__(self, dim, num_bits=3):
        """
        Generalized EDEN KV-Cache Compression Prototype
        Utilizes Randomized Hadamard Transforms and dynamic Scale (S) optimization.
        """
        # Ensure dimension is a power of 2 for Fast Hadamard Transform
        assert (dim & (dim - 1) == 0) and dim > 0, "Dimension must be a power of 2"
        self.dim = dim
        self.num_bits = num_bits
        
        # 3-bit quantization means 8 levels.
        # We can use [-4, -3, -2, -1, 0, 1, 2, 3]
        self.q_min = -(2 ** (num_bits - 1))
        self.q_max = (2 ** (num_bits - 1)) - 1
        
        # Random sign vector for Randomized Hadamard Transform
        # Using a fixed seed for reproducibility in testing, or dynamic in production
        np.random.seed(42)
        self.random_signs = np.random.choice([-1, 1], size=dim)
        
        # Precompute Hadamard matrix for simplicity in prototype
        # In a highly optimized CUDA version, this would be a Fast Walsh-Hadamard Transform (FWHT)
        self.hadamard_matrix = self._generate_hadamard_matrix(dim)
        # Normalization factor for Hadamard transform to make it orthogonal
        self.normalization = 1.0 / math.sqrt(dim)

    def _generate_hadamard_matrix(self, n):
        """Generates a Walsh-Hadamard matrix of size n x n."""
        H = np.array([[1]])
        while H.shape[0] < n:
            H = np.block([[H, H], [H, -H]])
        return H

    def randomized_hadamard_transform(self, x):
        """Applies Randomized Hadamard Transform: H * D * x"""
        # Multiply by random signs (D * x)
        x_signed = x * self.random_signs
        # Apply Hadamard transform and normalize
        return self.normalization * np.dot(self.hadamard_matrix, x_signed)

    def inverse_randomized_hadamard_transform(self, y):
        """Applies Inverse Randomized Hadamard Transform: D * H^T * y"""
        # H is symmetric and H * H = I * dim. With normalization, H^T = H.
        x_signed = self.normalization * np.dot(self.hadamard_matrix, y)
        # Inverse of D is D itself since elements are +1/-1
        return x_signed * self.random_signs

    def quantize(self, y, S):
        """Quantizes the transformed vector y using scale S."""
        # y_q = clip(round(y / S), q_min, q_max)
        y_scaled = np.round(y / S)
        y_q_int = np.clip(y_scaled, self.q_min, self.q_max)
        return y_q_int

    def dequantize(self, y_q_int, S):
        """Dequantizes the integer vector back to float using scale S."""
        return y_q_int * S

    def optimize_scale(self, y, num_candidates=100):
        """
        Dynamically finds the optimal scale parameter S that minimizes MSE.
        For EDEN, S is optimized per vector (or per block).
        """
        # S candidate range: max absolute value / max quant level is a good starting point
        max_val = np.max(np.abs(y))
        if max_val == 0:
            return 1.0 # arbitrary non-zero scale if all zeros
            
        # Standard TurboQuant might use a fixed heuristic like max_val / q_max.
        # EDEN optimizes S.
        min_s = max_val / (self.q_max * 2.0)
        max_s = max_val / (self.q_max * 0.5)
        
        candidates = np.linspace(min_s, max_s, num_candidates)
        best_S = candidates[0]
        min_mse = float('inf')
        
        for S in candidates:
            y_q_int = self.quantize(y, S)
            y_dequant = self.dequantize(y_q_int, S)
            mse = np.mean((y - y_dequant) ** 2)
            if mse < min_mse:
                min_mse = mse
                best_S = S
                
        return best_S

    def compress(self, x):
        """
        Full compression pipeline: RHT -> Optimize S -> Quantize
        Returns the quantized integers and the chosen scale S.
        """
        # 1. RHT
        y = self.randomized_hadamard_transform(x)
        # 2. Optimize S
        S = self.optimize_scale(y)
        # 3. Quantize
        y_q_int = self.quantize(y, S)
        
        return y_q_int, S

    def decompress(self, y_q_int, S):
        """
        Full decompression pipeline: Dequantize -> Inverse RHT
        Returns the reconstructed vector x_hat.
        """
        # 1. Dequantize
        y_dequant = self.dequantize(y_q_int, S)
        # 2. Inverse RHT
        x_hat = self.inverse_randomized_hadamard_transform(y_dequant)
        return x_hat
