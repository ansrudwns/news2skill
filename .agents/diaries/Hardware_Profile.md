---
name: Hardware_Profile_Constraints
description: 사용자 로컬 환경 하드웨어 벤치마크 및 폴백(Fallback) 제약조건
track: B
score: 100
---

# Local Hardware Profile

이 다이어리는 로컬 LLM 폴백(Fallback) 또는 오프라인 무중단 에이전트를 가동할 때 기준이 되는 사용자 노트북의 하드웨어 스펙을 영구적으로 저장합니다. (2026-04-09 스캔)

## 📌 단말기 스펙 (Windows 11 Home)
- **CPU:** AMD Ryzen AI 5 340 (통합 NPU 대응 모델)
- **메모리 (RAM):** 24 GB
- **GPU:** AMD Radeon(TM) 840M Graphics

## 💡 에이전트 실행 권장 가이드라인
1. **메모리 여유분:** 24GB의 거대한 RAM 용량을 바탕으로, **Gemma 4 9B GGUF (Q4_K_M ~ Q6_K 양자화)** 모델을 램에 한 번에 올려도 약 6~8GB만 차지하므로 아주 쾌적한 오프라인 에이전틱 구동이 가능함.
2. **AMD 백엔드 활용:** 엔비디아(CUDA)가 아닌 AMD 그래픽 시스템이므로, 향후 로컬 LLM 구동 시 `llama.cpp`의 **Vulkan(벌칸)** 백엔드를 활성화하여 GPU 가속을 끌어내는 것이 핵심.
3. **병렬 처리 잠재력:** Ryzen AI 칩셋의 특성상 간단한 임베딩(Vector) 작업 등은 백그라운드 NPU로, 메인 에이전트 추론은 GPU로 분산시키는 오버클럭 세팅이 가능함.
