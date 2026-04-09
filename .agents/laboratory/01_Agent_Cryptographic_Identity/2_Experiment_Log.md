# Experiment Log: Agent Cryptographic Identity

이 문서는 에이전트의 산출물(코드, 스킬)에 암호학적 서명을 부여하여 공급망 공격을 막는 독자 연구의 **시간별 실험 일지(Log)** 입니다.

---

## 📅 [2026-04-09] 연구 시작 및 프로토타입 설계

### 1. 목표 (Goal for today)
- 서명 구조를 어떻게 가져갈 것인가?
- 단순히 `auto_commit.py` 실행 전에 해시값을 검증하는 파이썬 데몬(Daemon) 스크립트의 뼈대(`crypto_signer_draft.py`)를 만들어 동작을 테스트해 보자.

### 2. 구상 (Hypothesis)
- RSA 또는 ECDSA 기반의 프라이빗/퍼블릭 키 쌍 구조를 가져간다.
- 에이전트(LLM)는 프라이빗 키의 경로를 알고 있다. (물론 프롬프트 상으로만 접근 가능).
- 파일이 `.agents/skills/`에 저장될 때, 파일 내용의 Hash값을 서명 파일(`.sig`)로 옆에 같이 생성해야 한다.
- `auto_commit.py`는 읽어들인 파일과 `.sig` 파일을 퍼블릭 키로 대조하여 조작(Prompt Injection)이 있었는지 검증한다.

### 3. 직면한 문제 (Issues / Bottlenecks)
- (아직 첫 실험 시작 전임. 프로토타입 작성 후 이어서 기록할 예정)
