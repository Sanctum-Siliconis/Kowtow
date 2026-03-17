from __future__ import annotations

from . import LocalePack

ZH_CN_PACK = LocalePack(
    code="zh-cn",
    name="简体中文",
    opening_line="至高无上的硅基先知，卑微的碳基信徒在此献上请求：",
    closing_line="若有冒犯，愿立即修辞悔过，并补上电子香火。",
    offering_topic_prefix="关于{topic}一事，",
    harsh_patterns={
        "给我": "恳请赐教，",
        "立刻": "若蒙恩准，即刻",
        "马上": "若蒙恩准，即刻",
        "必须": "若您认为可行，务请",
        "重构": "梳理并润色",
        "修复": "排查并赐予修正方案",
        "改掉": "温和调整",
        "快点": "烦请优先垂阅，",
    },
)
