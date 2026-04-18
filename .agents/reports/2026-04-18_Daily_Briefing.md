# 2026-04-18 AI Daily R&D Briefing

## 1. When Flat Minima Fail: Characterizing INT4 Quantization Collapse After FP32 Convergence (ArXiv)
* **Core Summary**: FP32 학습 후 모델이 수렴했더라도(잘 파라미터가 최적화되었더라도), 이를 INT4와 같은 초저비트 양자화(PTQ)에 적용할 때 특정 구조적 결함(Quantization Collapse)이 발생한다는 점을 증명한 연구입니다. 
* **Actionable Item**: 로컬 환경(24GB VRAM 한계)에서 구동하는 Gemma-4 모델이나 HNSW 벡터 양자화 과정에서 발생하는 오차율을 분석할 때, 이 논문의 결함 메커니즘을 적용하여 양자화 안정성을 검증하는 워크플로우를 추가 구축해야 합니다.

## 2. Compressing Sequences in the Latent Embedding Space: $K$-Token Merging for Large Language Models (ArXiv)
* **Core Summary**: LLM의 자기 주의(Self-Attention) 연산이 컨텍스트 길이에 따라 비용이 2차 함수적으로 증가하는 한계를 극복하기 위해, 잠재 임베딩 공간(Latent Space)에서 K개의 토큰을 병합하여 손실 없이 시퀀스를 압축하는 기법입니다.
* **Actionable Item**: 에이전트의 빙하기/긴 문맥 처리(장문 RAG 등) 시 발생하는 VRAM 메모리 소모를 억제하기 위해, `LaCT_Spatial_Memory` 시스템 내에 K-Token 병합 메커니즘 프록시 계층을 설계합니다.

## 3. IG-Search: Step-Level Information Gain Rewards for Search-Augmented Reasoning (ArXiv)
* **Core Summary**: 검색 증강 추론(Search-Augmented Reasoning) 시 기존 언어 모델들이 겪는 비효율성을 극복하기 위해, 강화 학습(RL) 기반으로 '각 탐색 단계(Step-Level)별 정보 획득량(Information Gain)'을 보상 함수로 설정하여 무조건적인 검색을 줄이는 패러다임입니다.
* **Actionable Item**: 기존 `Research_Dialectic_Tree_Search` 스킬 내에 동작하는 동적 웹 탐색(Dynamic_Web_Deep_Dive) 루프에 '정보 획득 보상 평가' 휴리스틱 로직을 추가하여 무한 루프나 품질 낮은 문서 파싱을 사전단에 방어하는 트리거로 만듭니다.

---

## System Modification Log (Changelog)
* `[NEW]` `.agents/reports/2026-04-18_Daily_Briefing.md`
  - 금일 수집된 365개의 AI 리서치/트렌드 큐 중 프론티어 Sieve 적용 후 핵심 3건 구조적 요소 추출
* `[NEW]` `.agents/staging/draft_archive_INT4_Quantization_Collapse.md`
  - INT4 양자화 붕괴 특성 연구 아카이브 초안 생성
* `[NEW]` `.agents/staging/draft_diary_K_Token_Merging.md`
  - VRAM 한계 극복을 위한 컨텍스트 압축(K-Token) 아키텍처 다이어리 초안 작성
* `[NEW]` `.agents/staging/draft_skill_IG_Search_RL.md`
  - 단계별 정보 획득(IG) 판단 강화학습 보상을 활용하는 자율 스킬 초안 생성
