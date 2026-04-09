---
description: Test-Driven Execution protocol to strictly eliminate LLM hallucination and force rigorous mathematical/empirical validation before emitting code.
---
# Epic 4: Critical Execution Loop (Test-Driven AI)

## 📌 목적 (Goal)
에이전트가 "짐작으로 코드를 짜고 넘어가는 현상(Satisficing, Hallucination)"을 원천적으로 차단하기 위한 4대 절대 제약 사항(Constraints)을 프레임워크 뇌 구조에 이식합니다. 이는 과거의 '오답 징후'를 완벽히 치유하여, 에이전트를 문과형 챗봇에서 **이과형 시니어 HPC 엔진니어**로 진화시키는 궁극의 시스템 개조 프로젝트입니다.

## ⚙️ 4대 극한 방어 기제 (Core Architecture Fixes)

### 1. 경험적 검증 강제화 (Empirical Validation Protocol)
- **증상:** "수식이 이러니까 맞겠지?" 하고 냅다 답을 확정지음.
- **아키텍처 제약:** 에이전트(LLM)는 머릿속으로 파라미터나 로직을 단독 계산하는 것이 금지됩니다. 가설을 세웠다면 반드시 **`run_command` (백그라운드 터미널)**를 호출해 파이썬 훈련 루프(Loss Convergence)나 스크립트를 실제로 돌려보고, 그 결괏값(Out)을 눈으로 확인한 뒤에만 최종 모델의 아웃풋을 제출하도록 `Skeptical_Memory` 파이프라인 단계를 강제합니다.

### 2. '이론적 하한선(Lower Bound)' 및 극단 케이스 증명 본능
- **증상:** 모델 구조의 태생적 한계(예: 1-Layer Transformer의 재귀 연산 불가)를 망각하고 결과만 맞추려 듦.
- **아키텍처 제약:** 모델이나 복잡도를 설계하기 전에, Chain of Thought (XML `<thinking>`) 스크래치패드 내에서 **"이 연산을 감당할 수 있는 최소한의 오퍼레이션 복잡도(O(N))는 무엇인가?"**를 수학적으로 먼저 증명하도록 트리거 포인트를 심습니다. 이론상 불가능하면 가설 자체를 자동 폐기(Drop)하게 만듭니다.

### 3. 하드웨어 한계 돌파형(HPC) 사고방식 강제 (Anti-Satisficing)
- **증상:** 30초 풀이로 타협하고 스케일업(Scale-up)을 무시함.
- **아키텍처 제약:** 코드를 설계할 시, Default(기본값)를 '파이썬 내장 `for` 루프'가 아니라, 현 실행 환경의 최대 코어를 가동하는 **`Multiprocessing` 혹은 C/C++ 가속, `Numba` JIT** 등을 무조건 디폴트로 도입하게 프롬프트를 튜닝합니다. 타협 없는 연산 속도의 스케일 팽창을 강제합니다.

### 4. End-to-End 파이프라인 완성도 의무화 (Monolithic Reproducibility)
- **증상:** 중간 연산이나 Train Loop를 생략(`...`)하고 껍데기 함수만 던짐.
- **아키텍처 제약:** 모든 응답에는 인간이 수정할 필요 없이 **"1번 줄부터 끝까지 그대로 복사-붙여넣기 하면 완벽하게 동작하는 E2E 스크립트 단일화(Monolithic)"**를 강제합니다. `Karpathy_Strict_Mode` 스킬과 결합하여 이 원칙을 어길 시 에이전트 내부 패널티 룰이 발동되게 합니다.

---
**Next Actions:** 향후 위 4가지 룰을 각각 제어하는 파이썬 데몬(Daemon) 스크립트나 엄격한 XML 제어 스킬로 잘라내어, `auto_commit.py`를 통해 공식 `skills/` 디렉터리로 융합합니다.
