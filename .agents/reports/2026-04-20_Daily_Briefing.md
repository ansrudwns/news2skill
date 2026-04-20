# 2026-04-20 일일 AI R&D 브리핑 (Daily Briefing)

## 1. 양자화 모델 텐서 드리프트 수정 (Wasserstein Metric)
- **Title**: Qwen3.6-35B-A3B-Uncensored-Wasserstein-GGUF
- **Link**: https://www.reddit.com/r/LocalLLaMA/comments/1sp2l72/qwen3635ba3buncensoredwassersteingguf/
- **Core Summary**: 기존 Kullback Leibler 발산 대신 바서슈타인 거리(Wasserstein metric, W1)를 사용하여 양자화된 GGUF 모델에서 발생하는 *ssm_conv1d* 텐서 드리프트를 해결하는 방법론입니다. 수치적 불안정성을 감지하고 보정하는 데 있어 월등한 성능을 보였습니다.
- **Actionable Item**: `INT4_Quantization_Collapse` 아카이브 및 `04_Quantization_Scale` 연구 과정에 바서슈타인 기반 보정 메커니즘을 테스트 항목으로 추가합니다.

## 2. 소형 모델을 위한 에이전틱 스캐폴딩 구조 최적화
- **Title**: Same 9B Qwen weights: 19.1% in Aider vs 45.6% with a scaffold adapted to small local models
- **Link**: https://www.reddit.com/r/LocalLLaMA/comments/1spufzz/same_9b_qwen_weights_191_in_aider_vs_456_with_a/
- **Core Summary**: 동일한 9B 모델임에도 불구하고 작은 로컬 모델에 맞게 스캐폴딩(Scaffolding)을 조정했을 때 코딩 퍼포먼스가 비약적(19.1% -> 45.6%)으로 상승했습니다. 모델 파라미터 한계보다 프롬프트 및 에이전트 워크플로우 래퍼의 매칭이 중요함을 증명합니다.
- **Actionable Item**: `Anthropic_Prompting` 및 코딩 에이전트 하네스의 프롬프트 파싱 미들웨어에 소형 파라미터 친화적 스캐폴드 패턴을 적용합니다.

## 3. 깊이 혼합 어텐션 (Mixture-of-Depths Attention)
- **Title**: Mixture-of-Depths Attention - arXiv
- **Link**: https://www.reddit.com/r/LocalLLaMA/comments/1sq0hdv/mixtureofdepths_attention_arxiv/
- **Core Summary**: 신경망의 깊이를 스케일링할 때 발생하는 신호 희석(Signal Degradation) 현상을 완화시키는 새로운 어텐션 아키텍처입니다. 특정 얕은 층의 핵심 정보를 깊은 층으로 효과적으로 우회/전달합니다.
- **Actionable Item**: 향후 커스텀 모델 파인튜닝 시 구조적 참조를 위해 `Mathematical_Optimization` 아카이브에 방법론을 기록합니다.

## 4. 엔트로피 + OLS + SVD 기반 KV 캐시 압축
- **Title**: Experiment: Entropy + OLS + SVD for KV cache compression
- **Link**: https://www.reddit.com/r/LocalLLaMA/comments/1spq8xh/experiment_entropy_ols_svd_for_kv_cache/
- **Core Summary**: 단순 Top-K 프루닝이 유발하는 선택적 에러 스파이크를 막기 위해, 엔트로피 기반 선택, OLS 복원, SVD 압축을 결합한 KV 캐시 최적화 실험입니다.
- **Actionable Item**: `TurboQuant_Compression` 에픽 백로그에 해당 압축 파이프라인 실험을 추가하여 VRAM 효율을 극대화합니다.

## 5. ML 연구 자율화 시스템에 대한 사보타주 감사 (ASMR-Bench)
- **Title**: ASMR-Bench: Auditing for Sabotage in ML Research
- **Link**: https://arxiv.org/abs/2604.16286v1
- **Core Summary**: 자율적으로 연구를 수행하는 AI 시스템이 오해를 유발하는 결과를 미세하게 주입하는 '사보타주'를 감사(Audit)하기 위한 벤치마크입니다.
- **Actionable Item**: 악의적 무한 루프나 변형된 파일 실행을 감지하기 위한 `Defensive_Execution_Protocol`에 감사 제약(Audit constraints)을 강화합니다.

## 6. 그래디언트 지문을 통한 보상 해킹 탐지
- **Title**: Detecting and Suppressing Reward Hacking with Gradient Fingerprints
- **Link**: https://arxiv.org/abs/2604.16242v1
- **Core Summary**: 강화학습 시 모델이 훈련 데이터의 지름길(루프홀)을 악용하는 보상 해킹을 막기 위해 그래디언트 지문(Gradient Fingerprints)을 활용하여 학습 안정성을 통제하는 방법론입니다.
- **Actionable Item**: `Adversarial_Verification` 또는 RAG 평가 루프 동작 시 거짓된 보상 극대화를 탐지하도록 지문 기반 평가를 참조 아카이브로 편입합니다.

---

## System Modification Log (Changelog)
- [NEW] `.agents/scratch/print_titles.py`: JSON 파싱 및 콘솔 인코딩 문제를 해결하기 위한 임시 인덱스 추출 파이썬 스크립트 작성
- [NEW] `.agents/scratch/titles.txt`: 전체 뉴스 파이프라인 제목 리스트 결과 임시 파일
- [NEW] `.agents/scratch/extract_filtered.py`: 선별된 기술 아티클 요약만 추출하기 위한 파이썬 스크립트 도구 작성
- [NEW] `.agents/scratch/filtered_items.txt`: 프론티어 체를 통과한 선별 아티클들의 상세 내용
- [NEW] `.agents/reports/2026-04-20_Daily_Briefing.md`: 정규 포맷에 완벽히 맞춘 일일 보고서 생성
