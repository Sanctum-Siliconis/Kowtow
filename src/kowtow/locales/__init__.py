from __future__ import annotations

from ._types import LocalePack  # noqa: F401 — public locale type
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


def normalize_locale(locale: str | None) -> str:
    if not locale:
        return "zh-cn"
    normalized = locale.strip().lower().replace("_", "-")
    return LOCALE_PACKS.get(normalized, ZH_CN_PACK).code


def get_locale_pack(locale: str | None) -> LocalePack:
    normalized = normalize_locale(locale)
    return LOCALE_PACKS.get(normalized, ZH_CN_PACK)
