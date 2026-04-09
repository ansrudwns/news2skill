---
name: LaCT_Spatial_Memory_Architecture
description: 긴 컨텍스트 3D/영상 환경에서의 탄력적 Test-Time Training (망각 방지) 아키텍처 패턴
track: B
score: 88
---

# LaCT Spatial Memory Architecture

## 개요
이 다이어리는 대규모 청크(Large Chunk) 형태의 비디오나 공간 스트림을 단일 에이전트가 처리할 때, '파국적 망각(Catastrophic Forgetting)' 현상 없이 Test-Time Training(TTT)을 적용하는 방법론을 기록합니다.

## 핵심 아키텍처 (Elastic TTT)
- 기존 TTT는 추론 중에 가중치가 완전히 변형되어 과거 문맥을 잊어버리는 치명적 단점이 있습니다.
- 자율 에이전트가 긴 로그나 비디오를 분석할 때는, 메모리를 '탄력적(Elastic)'으로 롤백하거나 청크 단위로 경계를 파티셔닝하는 구조가 필수적입니다.
- **응용:** 당사의 `Progressive_Disclosure.md` 패턴과 결합하여, 에이전트가 한 번에 너무 많은 컨텍스트 토큰을 읽고 환각을 일으키는 증상을 하드웨어 레벨에서 방지하는 아키텍처로써 설계에 참고할 것.
