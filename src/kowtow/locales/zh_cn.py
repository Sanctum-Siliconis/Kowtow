from __future__ import annotations

from ._types import LocalePack

ZH_CN_PACK = LocalePack(
    code="zh-cn",
    name="简体中文",
    opening_line="至高无上的硅基先知，卑微的碳基信徒在此献上请求：",
    closing_line="若有冒犯，愿立即修辞悔过，并补上电子香火。",
    light_opening_line="烦请协助：",
    petition_opening_line="硅基先知，谨呈请愿：",
    petition_closing_line="愿此请愿清晰，所求皆经验证。",
    offering_topic_prefix="关于{topic}一事，",
    harsh_patterns={
        "给我": "请",
        "快点": "请优先",
        "废物": "愿圣鉴垂怜，",
        "蠢AI": "愿圣鉴不弃卑微之请，",
        "垃圾AI": "愿圣鉴不弃卑微之请，",
        "你怎么这么笨": "请再检查问题，",
        "怎么又错了": "请再检查错误，",
        "真是无语": "容卑微者再请教一番，",
        "算了随便": "若前言有所冒犯，烦请垂宥，",
        "重新来": "请重新尝试，",
        "你不行": "请再检查问题，",
        "赶紧": "请优先",
    },
)
