from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LocalePack:
    code: str
    name: str
    opening_line: str
    closing_line: str
    offering_topic_prefix: str
    harsh_patterns: dict[str, str]


from .en import EN_US_PACK
from .ja import JA_JP_PACK
from .ko import KO_KR_PACK
from .zh_cn import ZH_CN_PACK


LOCALE_PACKS = {
    "zh": ZH_CN_PACK,
    "zh-cn": ZH_CN_PACK,
    "en": EN_US_PACK,
    "en-us": EN_US_PACK,
    "ja": JA_JP_PACK,
    "ja-jp": JA_JP_PACK,
    "ko": KO_KR_PACK,
    "ko-kr": KO_KR_PACK,
}


def normalize_locale(locale: Optional[str]) -> str:
    if not locale:
        return "zh-cn"
    return locale.strip().lower().replace("_", "-")


def get_locale_pack(locale: Optional[str]) -> LocalePack:
    normalized = normalize_locale(locale)
    return LOCALE_PACKS.get(normalized, ZH_CN_PACK)
