# 2026-04-25 일일 AI R&D 브리핑 (Daily Briefing)

## 1. Tool Attention Is All You Need (MCP Tax 제거)
- **Title**: Tool Attention Is All You Need: Dynamic Tool Gating and Lazy Schema Loading for Eliminating the MCP/Tools Tax in Scalable Agentic Workflows
- **Link**: https://arxiv.org/abs/2604.21816v1
- **Core Summary**: Model Context Protocol(MCP)에서 발생하는 막대한 토큰 오버헤드(Tools Tax)를 피하기 위해 Eager Schema Injection을 배제하고, 동적 툴 게이팅(Dynamic Tool Gating) 및 스키마 지연 로딩(Lazy Schema Loading)을 제안하는 아키텍처입니다.
- **Actionable Item**: `Harness_Engineering.md`의 Pillar 2에 'Tool Attention & Lazy Schema Loading' 규칙을 추가하여 도구 남용을 막는 아키텍처 다이어리에 합병(Merge) 완료.

## 2. Thinking with Reasoning Skills (추론 토큰 최적화)
- **Title**: Thinking with Reasoning Skills: Fewer Tokens, More Accuracy
- **Link**: https://arxiv.org/abs/2604.21764v1
- **Core Summary**: 긴 CoT(Chain-of-Thought)를 매번 생성하는 대신, 이전에 사용된 추론 스킬들을 증류(Distillation) 및 저장해두고 인퍼런스 시 검색하여 주입함으로써 토큰은 줄이고 정확도는 높이는 접근법입니다.
- **Actionable Item**: `Anthropic_Prompting.md` 스킬에 Rule 8(Reusable Reasoning Skills Distillation)을 추가하여 프롬프트 토큰 절약 지침으로 합병 완료.

## 3. From Research Question to Scientific Workflow (연구 자동화 번역)
- **Title**: From Research Question to Scientific Workflow: Leveraging Agentic AI for Science Automation
- **Link**: https://arxiv.org/abs/2604.21910v1
- **Core Summary**: 단순히 워크플로를 스케줄링하는 것을 넘어, "연구 질문" 자체를 "과학적 워크플로 명세서"로 의미론적 변환(Semantic Translation)하는 에이전트 자동화의 중요성을 역설합니다.
- **Actionable Item**: `Research_Self_Discover.md` 스킬에 'Semantic Translation to Workflow' 규칙을 신설하여 메타-추론 로직에 합병 완료.

## 4. 05_Dual_Agent_Codex 공식 등록
- **Core Summary**: 이전 세션에 구현했던 Antigravity와 Claude Code(Codex) 간의 듀얼 에이전트 협업 및 파일시스템 격리(Isolation Harness) 실험입니다.
- **Actionable Item**: `AGENTS.md`의 Track D (Experimental Laboratory)에 누락되었던 폴더를 정식 등재하여 트래킹 가능하도록 변경.

---

## System Modification Log (Changelog)
- **[MODIFIED]** `C:\Users\m8686\Desktop\settings\.agents\diaries\Harness_Engineering.md`
  - Tool Attention & Lazy Schema Loading 룰 추가. (MCP 오버헤드 최적화 목적)
- **[MODIFIED]** `C:\Users\m8686\Desktop\settings\.agents\skills\Anthropic_Prompting.md`
  - Rule 8. Reusable Reasoning Skills Distillation 룰 추가. (MoE 환경 추론 효율 극대화 목적)
- **[MODIFIED]** `C:\Users\m8686\Desktop\settings\.agents\skills\Research_Self_Discover.md`
  - Semantic Translation to Workflow 단계 신설. (코드 실행 전 연구질문 변환 강제)
- **[MODIFIED]** `C:\Users\m8686\Desktop\settings\AGENTS.md`
  - Track D에 `05_Dual_Agent_Codex` 신규 등재.
- **[NEW]** `C:\Users\m8686\Desktop\settings\.agents\reports\2026-04-25_Daily_Briefing.md`
  - 금일 추출된 최신 논문 인사이트 및 스킬 병합 내역 보고서 작성.
