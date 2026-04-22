import unittest
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eden_quant import EDENQuantizer

class TestEDEN(unittest.TestCase):
    def test_hadamard_transform_reversibility(self):
        """Verify that RHT -> Inverse RHT perfectly reconstructs the input."""
        dim = 64
        quantizer = EDENQuantizer(dim=dim)
        
        x = np.random.randn(dim)
        y = quantizer.randomized_hadamard_transform(x)
        x_hat = quantizer.inverse_randomized_hadamard_transform(y)
        
        mse = np.mean((x - x_hat) ** 2)
        self.assertLess(mse, 1e-10, f"RHT is not reversible, MSE: {mse}")

    def test_eden_compression(self):
        """Verify that the full EDEN compression/decompression loop works and has acceptable MSE."""
        dim = 128
        quantizer = EDENQuantizer(dim=dim, num_bits=3)
        
        x = np.random.randn(dim)
        x[10] = 5.0
        x[42] = -6.0
        
        y_q_int, S = quantizer.compress(x)
        x_hat = quantizer.decompress(y_q_int, S)
        
        self.assertTrue(np.all(y_q_int >= quantizer.q_min), f"Quantized values below q_min: {np.min(y_q_int)}")
        self.assertTrue(np.all(y_q_int <= quantizer.q_max), f"Quantized values above q_max: {np.max(y_q_int)}")
        
        mse = np.mean((x - x_hat) ** 2)
        self.assertLess(mse, 0.5, f"MSE is too high: {mse}")

    def test_outlier_smearing(self):
        """Verify that RHT smears outliers effectively, which is the main point of EDEN/TurboQuant."""
        dim = 256
        quantizer = EDENQuantizer(dim=dim, num_bits=3)
        
        x = np.zeros(dim)
        x[0] = 100.0
        
        y = quantizer.randomized_hadamard_transform(x)
        max_y = np.max(np.abs(y))
        
        self.assertLess(max_y, 10.0, "Outlier was not properly smeared by RHT")

if __name__ == "__main__":
    unittest.main()
