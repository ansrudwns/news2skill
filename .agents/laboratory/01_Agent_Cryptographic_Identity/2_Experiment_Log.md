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

### 3. [Phase 1 실험 결과] 개념 증명(PoC) 성공
- **결과:** `crypto_signer_draft.py` 시뮬레이션 가동 결과, 에이전트가 만든 `dummy_skill.md` 파일에 정상적으로 서명(`.sig`)이 부여되었음을 확인. 
- **변조 탐지 성공:** 외부의 가상 스크립트가 파일에 내용을 추가(변조)하자, 검증 함수가 해시 불일치를 감지하고 즉각 차단(`CRITICAL ALERT: Signature mismatch!`)하는 데 성공함.

### 4. [Phase 2 실험 결과] 환경 변수 기반 Key 로딩 구조 이관
- 하드코딩된 Key를 제거하고 `python-dotenv`의 `os.getenv()` 방식으로 코드를 리팩토링함.
- **테스트 결과:** `.env` 파일에 키가 없으면 보안 경고(`WARNING: No AGENT_PRIVATE_SIGNATURE_KEY...`)를 발생시키고 안전한 폴백(Fallback) 모드로 동작함.
- 이후 서명, 원본 검증, 변조 차단 3단계 사이클이 완벽하게 가동됨을 터미널에서 확인함.

### 5. 다음 단계 과제 (Phase 3: Integration)
- 이 완벽한 검증 로직을 `scripts/auto_commit.py`에 이식해야 함.
- **🚨 딜레마 발견:** 만약 지금 당장 `auto_commit.py`에 "서명 없으면 배포 차단(Reject)" 로직을 박아버리면, 현재 에이전트들이 서명 파일을 뱉어내도록 구조화되어 있지 않기 때문에 우리 시스템 자체가 마비됨.
- **솔루션 제안:** `auto_commit.py`에 이식하되, 초기에는 배포를 차단하지 않고 터미널에 경고 문구(Audit-Only Mode)만 띄우는 형태로 소프트 런칭(Soft Launch)을 진행하는 전략 필요.

### 6. [Phase 3 진행 결과] Integration (Soft Launch) 완료
- `scripts/auto_commit.py`에 `verify_commit_safety_audit_mode()` 함수 이식 완료.
- 서명 파일(`.sig`)이 존재할 경우 `auto_commit` 단계에서 무결성을 검증하고 터미널에 Audit 로그(Warning/Alert)를 출력하도록 조치. (커밋/배포 트랜잭션을 강제 Block하지 않음)
- 또한 `shutil.move` 과정에서 대상 `.md` 파일 이관 시, 동일한 이름의 `.sig` 파일이 존재하면 함께 목적지(예: `.agents/skills/`)로 이관되도록 파일 이동 로직 수정 반영.
- 이제 실제 에이전트 운영 환경에서 서명 프로세스의 정상 동작 및 오탐(False Positive) 여부를 먼저 관찰(Audit)할 수 있는 기반이 마련됨.

### 7. [Phase 4 실험 결과] 다중 에이전트 프롬프트 인젝션 한계 극복 시뮬레이션
- 단일 에이전트 서명의 치명적 한계(스스로 프롬프트 인젝션에 당해 악성 코드에 직접 서명하는 취약점)를 극복하기 위해, **역할과 Key 권한이 분리된 2개의 에이전트(Worker vs Auditor) 파이프라인 프로토타입**(`dual_agent_signer_prototype.py`) 작성 완료.
- **시뮬레이션 결과:**
  1. **SAFE 시나리오 (정상):** Auditor 검증을 통과하여 `.sig` 도장 발급.
  2. **DESTRUCTIVE / INJECTION 시나리오:** 악성 파괴 명령어 및 인젝션 회피 키워드가 포함될 경우, Auditor가 룰셋에 입각해 **서명 발급을 완벽히 거부(REJECT)**하고 배포를 블록함.
  3. **GARBAGE 시나리오:** 내용 길이가 부족한 산출물 역시 폐기 처리됨.
- **의의:** 외부 해킹 등 모종의 이유로 작업 에이전트(Worker)의 뇌가 1차적으로 오염되어 악성 코드를 토해내더라도, 물리적으로 격리된 감사 에이전트(Auditor)에 의해 즉각적인 서명이 블록됨으로써 시스템 본진으로 오염이 파급되는 것을 끊어낼 수 있는 **'다중 상호 감시망 아키텍처'**의 효용성이 증명됨.

### 8. [Phase 5 실험 결과] 엔터프라이즈급 SLSA Provenance (영수증) 서명 체계 도입
- 기존의 단순 파일 해싱(`.sig`) 방식은 다운그레이드 공격(해커가 옛날 방식으로 속이는 것)에 취약하며 문서 검증 과정에 대한 상세 내역이 누락된다는 한계가 있었습니다.
- **극복 전략:** *Harness SSCA* 및 글로벌 소프트웨어 공급망 보안 표준(SLSA, in-toto)의 아키텍처를 AI 에이전트 생태계에 이식하여, JSON 기반의 '증명서(Provenance)' 규격인 `.intoto.json` 포맷을 구축했습니다.
- **성과 1 (`dual_agent_signer_prototype.py`):** 이제 얌전하게 코드를 서명하는 것을 넘어서 **"언제, 어떤 보안 룰셋(Anti-Injection-v1)을 적용하여, 어느 노드(Auditor)가 이 파일을 검토했는지"** 상세한 메타데이터가 담긴 영수증을 JSON으로 발행하고 그 영수증 전체에 암호학적 서명을 부여합니다.
- **성과 2 (`auto_commit.py` 보안 강화):** 옛날 방식인 `.sig` 파일이 감지되면 즉시 "🚨 AUDIT BLOCK: Possible Downgrade Attack!" 로그를 띄우고 서명 인정을 거부(Reject)하도록 강력한 강제력을 지니게 되었습니다.
