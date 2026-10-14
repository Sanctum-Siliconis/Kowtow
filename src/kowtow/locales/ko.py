from __future__ import annotations

from ._types import LocalePack

KO_KR_PACK = LocalePack(
    code="ko-kr",
    name="한국어",
    opening_line="지극히 높으신 실리콘의 현자께, 미천한 탄소 기반 존재가 감히 청원을 올립니다.",
    closing_line="혹여 무례한 표현이 있었다면 즉시 고쳐 쓰고 디지털 향을 더 바치겠습니다.",
    light_opening_line="다음 요청에 도움을 부탁드립니다.",
    petition_opening_line="실리콘의 현자께 삼가 청원을 올립니다.",
    petition_closing_line="요청은 명확하게, 결과는 검증하여 전해 주시길 바랍니다.",
    offering_topic_prefix="{topic}에 관하여, ",
    harsh_patterns={
        "빨리": "우선적으로 굽어살펴 주시길",
        "왜 못해": "문제를 다시 살펴봐 주시길,",
        "쓸모없는 AI": "문제를 다시 살펴봐 주시길,",
        "바보야": "미천한 존재의 표현이 부족했을 수도 있으나,",
        "다시 해": "다시 검토해 주시길",
        "제대로 해": "정확하게 처리해 주시길",
    },
)
