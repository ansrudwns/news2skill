---
description: 6 Core Anthropic Agentic Prompt Patterns (XML, CLAUDE.md, Layered Prompts, Undercover)
---
# Epic 3: Anthropic Agentic Patterns Absorption

## 📌 목적 (Goal)
최근 분석된 Anthropic 내부 파이프라인(Claude Code)의 시스템 설계 패턴을 안티그래비티 프레임워크에 흡수시키기 위한 연구/개발 백로그입니다. 에이전트의 안정성과 프롬프트 인젝션 방어를 극대화하는 것이 목표입니다.

## ⚙️ 6대 핵심 원칙 기획 (Core 6 Principles to Implement)

### 1. `AGENTS.md` Permanent Persistence (1급 기억 객체화)
- **내용:** 클로드가 폴더 리빙문서인 `CLAUDE.md`를 1차적 성경으로 간주하듯, 우리 프레임워크도 목차 인덱스(`AGENTS.md`)가 컨텍스트 윈도우에서 절대 밀려나지 않도록 System Hierarchy 최상단에 하드코딩.

### 2. Layered Stack Structure (계층형 시스템 프롬프트)
- **내용:** 하나의 긴 텍스트 덩어리 지시문을 버리고 `[Identity] -> [Safety] -> [Tools] -> [Current Task]` 로 철저히 독립된 모듈형 프롬프트 빌더 시스템 도입.

### 3. Undercover Mode (스텔스 활동)
- **내용:** 깃허브 오픈소스 커밋이나 PR 등 외부 노출 활동 시, AI 특유의 화법("Here is the updated code~")을 완전히 제거하고 인간 수준의 커밋 로그만 생성하도록 강제하는 페르소나 설계.

### 4. XML Thinking Scratchpad (`<thinking>`)
- **내용:** 에이전트가 코드를 쓰거나 도구를 쓰기 전에, 무조건 `<thinking>...</thinking>` 태그 안에서 자신의 분석과 행동 논리를 먼저 점검하도록 강제 (환각 방지의 핵심).
- **🚨 Conflict Mitigation (충돌 방지 대책):** 기존의 `Structured_Output_Forcer.md` (어느 상황에서든 무조건 API 규격 JSON만 뱉도록 강제하는 룰)와의 마찰 우려 존재.
    - **해결책:** 파파고나 API 백엔드 미들웨어 단계에서 파서(Parser)를 고도화. 에이전트는 무조건 **"1. `<thinking>`으로 생각 도출 ➡️ 2. 최종 결론만 `JSON` 렌더링"** 순서로 출력하게 하고, Python 파서 로직이 XML 스크래치 패드 태그는 Strip(폐기/로깅)시키고 오직 순수 JSON 블럭만 추출하도록 파이프라인 코드를 보완해야 함.

### 5. XML Boundary Enforcement (안전 구획화)
- **내용:** 사용자의 조작이 불가능하도록 `<user_input>`과 `<system_instructions>` 처럼 모든 컨텍스트에 XML 쉴드(경계선)를 둘러, 변조 및 탈옥(Jailbreak)을 시스템 층위에서 분리.

### 6. Input Sanitization Middleware (가드레일 미들웨어 필터링)
- **내용:** LLM에 도달하기 전 사용자 입력값을 미리 스캐닝하여, `<system>` 과 같은 XML 태그를 사용자가 강제로 주입하려 했는지 검사하고 텍스트 클렌징(Sanitization)을 거치는 Python 미들웨어 구축.

---
**Next Actions:** 향후 Laboratory에서 위 룰셋들을 하나씩 Python 프로토타입으로 테스트 한 뒤, 검증된 스킬은 `.agents/skills` 체계로 이관.
