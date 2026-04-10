import numpy as np

def simulate_quantization():
    np.random.seed(42)
    # Generate random FP16 weights representing a layer
    weights = np.random.normal(0, 0.1, size=(1000, 1000))
    
    # Inject 1% extreme outliers (High Magnitude features crucial for reasoning)
    outlier_indices = np.random.choice(1000*1000, size=10000, replace=False)
    weights.flat[outlier_indices] = np.random.choice([-5.0, 5.0], size=10000)
    
    print("=== Baseline Matrix (1M weights) ===")
    print(f"Max Val: {np.max(weights):.2f}, Min Val: {np.min(weights):.2f}")
    
    # 1. Flat Quantization (INT4 Approximation -> Divide and Round)
    # This ruins outliers because the scale factor gets blown up
    scale_flat = np.max(np.abs(weights)) / 7.0 
    quant_flat = np.round(weights / scale_flat) * scale_flat
    mse_flat = np.mean((weights - quant_flat)**2)
    
    # 2. Scale-Dependent Optimization (Not All Bits Are Equal)
    # Preserve top 1% exactly (FP16), Quantize the remaining 99% tightly
    threshold = np.percentile(np.abs(weights), 99)
    mask_outlier = np.abs(weights) > threshold
    mask_normal = ~mask_outlier
    
    # Quantize only the regular weights using a much tighter scale
    scale_tight = np.max(np.abs(weights[mask_normal])) / 7.0
    quant_smart = np.copy(weights)
    quant_smart[mask_normal] = np.round(weights[mask_normal] / scale_tight) * scale_tight
    # Outliers remain untouched!
    
    mse_smart = np.mean((weights - quant_smart)**2)
    
    print(f"\n=== Empirical Results ===")
    print(f"1. Flat Quantization MSE  : {mse_flat:.4f} (High Error due to Outliers)")
    print(f"2. Smart Quantization MSE : {mse_smart:.4f} (Massive Improvement)")
    print(f"-> Conclusion: Saving VRAM by quantizing non-outliers is highly effective.")

if __name__ == "__main__":
    simulate_quantization()
