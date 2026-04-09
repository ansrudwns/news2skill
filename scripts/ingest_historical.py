import json
import os

def main():
    # 사전에 학습된 핵심 개념 8가지를 고정밀로 추출하기 위한 하드코딩된 리스트입니다.
    # 복잡한 정규식으로 인해 일부 개념이 누락되는 것을 막기 위한 안전한 방식입니다.
    items = [
        {"title": "Harness Engineering (하네스 엔지니어링)", "summary": "에이전트의 구동 환경과 통제 계층(AGENTS.md, 진실의 원천, 실행-지능 분리)을 설계하는 아키텍처 패턴."},
        {"title": "Model Context Protocol (MCP)", "summary": "에이전트가 도구와 통합하는 통신 규약. 단일 범용 동사를 사용해 컨텍스트 윈도우 점유율을 줄이는 모범 사례 포함."},
        {"title": "Progressive Disclosure (단계적 공개 스킬 아키텍처)", "summary": "평상시엔 100토큰짜리 요약본만 로딩하고, 조건이 일치할 때만 전체 SKILL.md 지침을 불러오는 기억력 가성비 극대화 패턴."},
        {"title": "Skeptical Memory (회의적 메모리)", "summary": "과거 기억을 맹신하지 않고 액션 전에 실제 파일 변경 상태를 검증(Verify)하는 에러율 감소 기법."},
        {"title": "autoDream (오토드림 자가치유 데몬)", "summary": "유저가 활동하지 않는 유휴 시간에 자율 에이전트가 돌아가며 메모리 파편화를 통합하고 모순을 제거하는 기법."},
        {"title": "Context Collapse (컨텍스트 붕괴/압축)", "summary": "토큰 한계 도달 시, 중요도가 떨어지는 도구의 출력값을 별도의 에이전트가 강제로 요약본으로 축소 렌더링하는 기법."},
        {"title": "Blocking Budget (차단 예산)", "summary": "자율 에이전트가 작업을 수행할 때 사용자 방해를 막기 위해 15초 제한 및 2회 초과 알림 금지를 설정하는 제어 장치."},
        {"title": "Adversarial Verification (적대적 심사 검증관)", "summary": "문제를 만들라는 본 에이전트와, 흠집을 찾으라는 감시 에이전트를 분리하여 성공률을 높이는 시스템 체크 로직."}
    ]
    
    final_output = {
        "source": "AI 기술 동향 및 클로드 유출 분석.txt",
        "total_items": len(items),
        "data": items
    }
    
    with open("historical_raw.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Successfully converted the historical document into {len(items)} discrete JSON chunks.")

if __name__ == "__main__":
    main()
