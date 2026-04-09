# Epic 2: LiteLLM 기반의 완전 무중단(Offline) 폴백 로우팅망 구축

## Background
당사는 모델을 가성비에 따라 알아서 나누어 타는 `Routing_Before_Thinking` 스킬을 가지고 있지만, 클라우드 서버(OpenAI, Anthropic)가 다운되거나 오프라인 환경에 들어갔을 때 로컬 모델로 전환하는 자동 스위칭(Fallback) 체계가 없음. (오늘 아침 등장한 Gemma 4 GGUF 활용처 부재)

## Adversarial Novelty Verification (중복성 검증 결과)
* **초기 기획안:** "API가 타임아웃 나면 Ollama를 때리도록 파이썬 `try-except` 커스텀 라우팅 코드 작성"
* **검증 결과 (PIVOT):** 웹 검색 결과, `LiteLLM` 라이브러리의 Proxy Config가 이미 Fallbacks 체인(`primary-openai` -> `fallback-ollama`)을 완벽하게 네이티브로 지원함. 우리가 커스텀 코드를 짤 필요가 없음.
* **수정된 액션 플랜:** 파이썬 코드를 뜯어고치는 대신, `LiteLLM` 컨테이너를 하나 띄우고 `config.yaml` 3줄만 추가하여 클라우드 API 호출을 자동으로 랩핑해주는 무중단 망(Intranet Local Fallback)을 도입.

## Hypothesis / Goal
클라우드 API(1차) -> Vertex AI(2차) -> 로컬 로드된 Gemma 4 / Llama-3 GGUF(3차) 순으로 API 요청을 자동 토스하는 `LiteLLM Proxy` 도입.

## Expected Impact
클라우드 사업자가 망가지건, 해저 광케이블이 끊어지건 상관없이 `Defensive_Fallback_Throttle` 스킬이 로컬 하드웨어를 통해 미션을 100% 무조건 완수해 내는 '좀비 에이전트' 인프라 확보.
