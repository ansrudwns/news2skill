---
name: Hardware_Profile_Constraints
description: Host hardware benchmarks and offline fallback constraints.
track: B
score: 100
---

# Local Hardware Profile (2026-04-09 Scan)

This diary persistently stores the hardware specifications of the host laptop. It serves as the absolute baseline for determining Local LLM fallback and offline continuous operations.

## 📌 Host Specifications (Windows 11 Home)
*   **CPU:** AMD Ryzen AI 5 340 (Integrated NPU Supported)
*   **Memory (RAM):** 24 GB
*   **GPU:** AMD Radeon(TM) 840M Graphics

## 💡 Agent Execution Guidelines
1.  **Memory Overhead:** Leveraging the massive 24GB RAM capacity, utilizing the **Gemma 4 9B GGUF (Q4_K_M to Q6_K quantization)** model requires only 6~8GB overhead, ensuring a highly responsive offline agentic environment.
2.  **AMD Backend Utilization:** Because the system leverages AMD graphics rather than NVIDIA (CUDA), executing local LLM inference requires activating the `llama.cpp` **Vulkan** backend to draw out hardware-accelerated GPU performance.
3.  **Parallel Processing Potential:** Given the characteristics of the Ryzen AI chipset, you can distribute lightweight embedding operations to the background NPU, while offloading the main agent inference to the GPU.
