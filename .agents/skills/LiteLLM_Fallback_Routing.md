---
name: LiteLLM_Fallback_Routing
description: 무중단 오프라인(Local LLM) 폴백 네트워크를 지원하는 프록시 라우터
track: A
score: 98
---

# LiteLLM Offline Fallback Routing

## 개요
비용 최적화(라우팅) 스킬에서 한 단계 더 나아가, 클라우드 API 장애 시 즉각적으로 로컬 하드웨어(Gemma 4 9B GGUF) 자원을 끌어다 쓰는 100% 무중단 폴백(Fallback) 라우팅 통제 규칙입니다.

## 시스템 제약사항 (Hardware Constraints 바탕)
- 타겟 디바이스: `AMD Ryzen AI 5 340`, `24GB RAM`
- 최적화 백엔드: `llama.cpp` + `Vulkan 가속(Radeon 840M)` 지원 필수.

## 강제 이행 원칙 (Strict Rules)
1. **Proxy Config 작성:** `Routing_Before_Thinking` 스킬과 병존하며, 직접 파이썬 `Try-Catch`를 짜지 말고 오직 `litellm --config config.yaml` 명령으로 프록시 포트를 띄웁니다.
2. **체인 구성:** 
   - 1차(`primary`): GPT-4o / Claude 3.5 (Cloud API)
   - 2차(`fallback`): `ollama/gemma-4-9b-gguf-vulkan` (Local Inference)
3. 1차 API에서 3초 이상 응답이 없거나 `RateLimitError(429)`가 반환되면 2차 로컬 모델로 즉시 토스합니다. 단, 민감한 보안 파일이나 개인 정보를 파싱할 때에는 1차 API를 아예 배제하고 강제로 2차 로컬 노드만 사용하게 파이프라인을 고정합니다.
