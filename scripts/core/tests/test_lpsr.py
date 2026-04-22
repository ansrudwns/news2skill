import unittest
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lpsr import LPSR_Detector, MockAutoregressiveDecoder

class TestLPSR(unittest.TestCase):

    def test_normal_generation(self):
        detector = LPSR_Detector(cos_sim_threshold=0.5, entropy_threshold=2.0)
        decoder = MockAutoregressiveDecoder(detector)
        
        # Step 1: Normal vector, low entropy
        v1 = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
        rolled_back = decoder.generate_step("The", v1, token_entropy=0.5)
        self.assertFalse(rolled_back)
        self.assertEqual(len(decoder.kv_cache), 1)
        
        # Step 2: Similar vector, low entropy
        v2 = np.array([0.9, 0.1, 0.0, 0.0, 0.0])
        rolled_back = decoder.generate_step("sky", v2, token_entropy=0.6)
        self.assertFalse(rolled_back)
        self.assertEqual(len(decoder.kv_cache), 2)

    def test_phase_shift_rollback(self):
        detector = LPSR_Detector(cos_sim_threshold=0.5, entropy_threshold=2.0)
        decoder = MockAutoregressiveDecoder(detector)
        
        # Step 1: Normal vector
        v1 = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
        decoder.generate_step("The", v1, token_entropy=0.5)
        
        # Step 2: Normal vector
        v2 = np.array([0.9, 0.1, 0.0, 0.0, 0.0])
        decoder.generate_step("sky", v2, token_entropy=0.6)
        
        # Step 3: Phase Shift! Vector flips direction (low cosine sim) AND high entropy
        v3 = np.array([-1.0, 0.0, 0.0, 0.0, 0.0]) 
        # cos_sim(v2, v3) is approx -0.9, which is < 0.5
        rolled_back = decoder.generate_step("banana", v3, token_entropy=3.5)
        
        # Should trigger rollback
        self.assertTrue(rolled_back)
        
        # Cache should have popped 'sky' and injected '<STEERING_CORRECTION>'
        # So it should be ['The', '<STEERING_CORRECTION>']
        self.assertEqual(decoder.kv_cache, ["The", "<STEERING_CORRECTION>"])

    def test_false_positive_prevention(self):
        # Dual gate prevents rollback if only one condition is met
        detector = LPSR_Detector(cos_sim_threshold=0.5, entropy_threshold=2.0)
        decoder = MockAutoregressiveDecoder(detector)
        
        v1 = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
        decoder.generate_step("The", v1, token_entropy=0.5)
        
        # Low cosine sim, but LOW entropy (Model is confident in its sharp turn, e.g. punctuation or topic shift)
        v2 = np.array([-1.0, 0.0, 0.0, 0.0, 0.0]) 
        rolled_back = decoder.generate_step(".", v2, token_entropy=0.1)
        
        # Should NOT trigger rollback
        self.assertFalse(rolled_back)
        self.assertEqual(decoder.kv_cache, ["The", "."])

if __name__ == '__main__':
    unittest.main()
