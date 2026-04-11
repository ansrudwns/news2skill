---
description: "Optimization architecture implementing 3-bit Lloyd-Max scalar quantization for HNSW vector embeddings."
---

# 3-bit HNSW Vector Quantization (Lloyd-Max)

## Core Concept
In constrained Agentic scenarios, large-scale floating-point memories (float32 embeddings at dim=1024) occupy ~4,096 bytes per node, blowing up VRAM footprints for dense RAG lookups. 
Recent empirical findings demonstrate that storing 3-bit quantized embeddings directly within Hierarchical Navigable Small World (HNSW) nodes can compress the size down to ~388 bytes (~10x reduction) while preserving >95% topological recall.

## Architectural Guidelines
1. **Lloyd-Max Scalar Quantization**: Instead of straight uniform quantization, apply Lloyd-Max clustering across the local node geometries. This allocates more quantization bins to the densest regions of the embedding distribution.
2. **In-Node Compression**: Do not store the full vector off-disk. Embed the 3-bit codes directly in the graph edge attributes or adjacent index chunks so distance calculations happen strictly on L1/L2 caches.
3. **Asymmetric Distance Computation (ADC)**: During query time, keep the input query as float32. Compute the exact float-to-3bit quantized dot products. Do NOT decompress the 3-bit index back to float32.

## Implementation Standard
```python
import numpy as np

def lloyd_max_3bit_quantize(vectors, num_iterations=10):
    """
    Simulated 3-bit Lloyd Max Scalar Quantizer.
    Reduces float32 array to categorical bins 0-7.
    """
    # 3-bit allows 8 centroid bins
    num_bins = 8
    
    # Initialize centroids randomly from the data distribution
    min_val, max_val = np.min(vectors), np.max(vectors)
    centroids = np.linspace(min_val, max_val, num_bins)
    
    for _ in range(num_iterations):
        # 1. Assign items to nearest centroid
        distances = np.abs(vectors[..., np.newaxis] - centroids)
        assignments = np.argmin(distances, axis=-1)
        
        # 2. Update centroids to mean of assigned nodes
        for i in range(num_bins):
            mask = (assignments == i)
            if np.any(mask):
                centroids[i] = np.mean(vectors[mask])
                
    return assignments.astype(np.uint8), centroids
```

## Security & Reliability Note
- Since quantization compresses the vector space identically backward, accuracy drops steeply below 3 bits. 
- Ensure that the initial embedding space normalization properly spans `[-1, 1]` or standard normal space to optimize Lloyd-Max boundary captures.
