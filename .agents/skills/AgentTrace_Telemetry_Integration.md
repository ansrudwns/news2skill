---
name: AgentTrace_Telemetry_Integration
description: Langfuse/OTel 기반의 에이전트 자가 치유(Reflexion) 시스템 로깅 연동
track: A
score: 96
---

# Agent Telemetry & Reflexion Logger

## 개요
이 스킬은 무한 루프나 태스크 실패 방지를 넘어서, 에이전트가 "내가 왜 실패했는가"를 Langfuse 대시보드 및 로컬 로그에 남겨 지속적으로 진화(ALTK-Evolve)할 수 있게 만드는 OTel 미들웨어 연동 규칙입니다.

## 강제 이행 원칙 (Strict Rules)
1. **OTel 미들웨어 삽입:** 에이전트 코어 추론 로직(LLM Call) 직전에 OpenTelemetry 래퍼(e.g., `Langfuse`) 설정을 최우선으로 `import` 하고 세팅합니다.
2. **실패 로그 캐치:** `Exception`이 발생하거나 `Adversarial_Verification`에서 Score 80점 미만으로 반려된 경우, 단순 재시도(Retry)를 하지 말고 해당 Trace ID와 프롬프트를 반드시 로깅 서버로 푸시합니다.
3. **다음 세션 반영:** 에이전트가 새 태스크를 할당받을 때, 로컬에 떨어진 `error_remediation.md` 파일이 존재한다면 최우선 시스템 프롬프트(System Prompt)로 읽어들여 같은 실수를 반복하지 않게 만듭니다.
