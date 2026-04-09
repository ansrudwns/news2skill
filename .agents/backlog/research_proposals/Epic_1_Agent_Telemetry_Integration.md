# Epic 1: Langfuse/AgentTrace 기반의 에이전트 다이어리 자동화 시스템 도입

## Background
현재 당사의 시스템(`ai-daily` 분석기 등)은 한 번 실패하거나 포맷을 어길 때 `Defensive_Fallback_Throttle` 스킬을 통해 단순 재시도(Retry)만 할 뿐, '왜 실패했는지' 영구적인 지식(Reflexion)으로 남기거나 스스로 진화(ALTK-Evolve)하는 체계가 부족함. 로그가 일회성으로 증발함.

## Adversarial Novelty Verification (중복성 검증 결과)
* **초기 기획안:** "실패 로그를 분석하는 자체 Reflexion 파이썬 모듈 개발"
* **검증 결과 (PIVOT):** 웹 검색 결과, 이미 LangGraph, AgentTrace, Langfuse 등 OpenTelemetry(OTel) 기반의 너무나 훌륭한 오픈소스 에이전트 궤적 추적 인프라가 존재함. 자체 파이썬으로 허접하게 개발하는 것은 완벽한 인력 낭비.
* **수정된 액션 플랜:** 자체 모듈 개발 대신, 기존 파이프라인에 `Langfuse` SDK를 미들웨어로 연동(Integrate)하여, 프롬프트 실행 로그와 토큰 사용량을 대시보드로 수집하고 추후 분석 파이프라인으로 넘기는 구조를 적용.

## Hypothesis / Goal
당사의 에이전트 실행 환경 내부에 OpenTelemetry 인터페이스를 탑재하여, 모든 프롬프트, 툴 호출, 실행 결과를 영구 로깅하고 '실패 패턴'을 자동으로 찾아내어 백로그로 전송하는 생태계 구성.

## Expected Impact
동일한 에러를 두 번 반복하지 않으며, '망각의 늪'에 빠지는 에이전트를 실시간으로 모니터링할 최상위 관측소 확보 가능.
