# Not All Bits Are Equal: Scale-Dependent Quantization (Toy Sandbox)

## Hypothesis
In Large Language Models, outlier weights (high magnitude) drastically impact reasoning. Normal weights can be quantized to ultra-low precision (INT4 or INT2) to save VRAM, but outliers MUST be preserved at FP16. This provides a balance between 24GB local VRAM constraints and performance preservation.

## Local Implementation
This script uses Numpy to simulate compressing an FP16 weight matrix.
We identify top 1% outliers, keep them exact, and aggressively round the remaining 99%.

## Execution
Run `python experiment.py` to observe Mean Squared Error (MSE) compared to flat quantization.
