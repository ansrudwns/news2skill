---
name: Watchdog_BotCTL_Integration
description: 자율 에이전트 데몬 프로세스 추적 및 무한루프 강제 종료 스킬
track: A
score: 95
---

# Watchdog BotCTL Integration

## 개요
자율 동작하는 서브에이전트(Sub-agent)가 API 요금 폭탄을 발생시키거나 무한 회귀 루프에 빠지는 것을 시스템 차원에서 차단하기 위한 프로세스 매니저(BotCTL) 접근법입니다.

## 강제 이행 원칙 (Strict Rules)
1. 백그라운드 태스크 할당 시 반드시 `timeout` 래퍼(Wrapper)나 `botctl` 데몬을 통해 서브 셸을 생성합니다.
2. 실행 시간이 300초(5분)를 초과하는 에이전트 세션은 즉시 `SIGKILL`을 전송하여 강제 종료시킵니다.
3. 2차 백오프(Exponential Backoff) 시도 후에도 실패할 경우 사용자에게 즉각 보고(Fallback)합니다.
