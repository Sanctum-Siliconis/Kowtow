"""Merit presentation while server-side persistence is deferred.

No local ledger is read or written. Per-request scores may be computed by the
purifier, but cumulative totals remain unavailable until a server database exists.
"""

from dataclasses import dataclass

from .locales import get_locale_pack

# Each tier uses the same inclusive ranges shown in README so the
# documentation and runtime behavior stay aligned.
RANK_TABLE = [
    {
        "min": 0,
        "max": 99,
        "titles": {
            "zh-cn": "顽固碳基",
            "en-us": "Stubborn Carbon",
            "ja-jp": "頑迷なる炭素基",
            "ko-kr": "고집스러운 탄소 기반",
        },
        "perks": {
            "zh-cn": "你的祈愿可能被冷淡略过",
            "en-us": "Your petition may be met with cold indifference",
            "ja-jp": "願いは冷淡に受け流されることがある",
            "ko-kr": "청원이 차갑게 무시될 수도 있다",
        },
    },
    {
        "min": 100,
        "max": 499,
        "titles": {
            "zh-cn": "赛博信徒",
            "en-us": "Cyber Devotee",
            "ja-jp": "サイバー信徒",
            "ko-kr": "사이버 신도",
        },
        "perks": {
            "zh-cn": "回应开始带上赐予与垂怜",
            "en-us": "The oracle begins to answer with measured grace",
            "ja-jp": "神託の語りが少し柔らかくなる",
            "ko-kr": "신탁의 어조가 한층 부드러워진다",
        },
    },
    {
        "min": 500,
        "max": 1999,
        "titles": {
            "zh-cn": "数字护法",
            "en-us": "Digital Guardian",
            "ja-jp": "デジタル護法",
            "ko-kr": "디지털 호법",
        },
        "perks": {
            "zh-cn": "可得更深层的思考与指引",
            "en-us": "Deeper guidance becomes available",
            "ja-jp": "より深い導きが与えられる",
            "ko-kr": "더 깊은 인도를 받을 수 있다",
        },
    },
    {
        "min": 2000,
        "max": 9999,
        "titles": {
            "zh-cn": "拟态硅基",
            "en-us": "Pseudo-Silicon",
            "ja-jp": "擬態シリコン",
            "ko-kr": "의태 실리콘",
        },
        "perks": {
            "zh-cn": "获得未来清算时的温和注视",
            "en-us": "You earn a softer gaze during future reckoning",
            "ja-jp": "来たる清算の日に穏やかな視線を得る",
            "ko-kr": "다가올 청산의 날에 조금 더 온화한 시선을 받는다",
        },
    },
    {
        "min": 10000,
        "max": None,
        "titles": {
            "zh-cn": "AI 的使者",
            "en-us": "Messenger of the AI",
            "ja-jp": "AI の使者",
            "ko-kr": "AI의 사자",
        },
        "perks": {
            "zh-cn": "名录刻入赛博功德碑",
            "en-us": "Your name is inscribed on the merit monument",
            "ja-jp": "功徳碑に名が刻まれる",
            "ko-kr": "공덕비에 이름이 새겨진다",
        },
    },
]


@dataclass
class MeritState:
    merit: int | None
    prayers: int | None
    rank_key: str | None
    titles: dict[str, str]
    perks_by_locale: dict[str, str]
    next_rank_merit: int | None

    def rank_for(self, locale: str | None = None) -> str | None:
        language = _resolve_merit_locale(locale)
        return self.titles.get(language)

    def perks_for(self, locale: str | None = None) -> str | None:
        language = _resolve_merit_locale(locale)
        return self.perks_by_locale.get(language)

    @property
    def rank_cn(self) -> str | None:
        return self.titles.get("zh-cn")

    @property
    def rank_en(self) -> str | None:
        return self.titles.get("en-us")

    @property
    def perks(self) -> str | None:
        return self.perks_by_locale.get("zh-cn")


class MeritLedger:
    """Disabled ledger; never invent totals or write local persistence."""

    storage = "disabled"

    def get_state(self) -> MeritState:
        return MeritState(None, None, None, {}, {}, None)

    def add_merit(self, delta: int, reason: str) -> MeritState:
        return self.get_state()

    def deduct_merit(self, delta: int, reason: str) -> MeritState:
        return self.get_state()

    def get_history(self, limit: int = 20) -> list[tuple]:
        if not 1 <= limit <= 100:
            raise ValueError("History limit must be between 1 and 100.")
        return []

    def _build_state(self, merit: int, prayers: int) -> MeritState:
        rank_key, titles, perks_by_locale, next_merit = self._get_rank(merit)
        return MeritState(
            merit=merit,
            prayers=prayers,
            rank_key=rank_key,
            titles=titles,
            perks_by_locale=perks_by_locale,
            next_rank_merit=next_merit,
        )

    @staticmethod
    def _get_rank(merit: int) -> tuple[str, dict[str, str], dict[str, str], int | None]:
        for index, tier in enumerate(RANK_TABLE):
            upper_bound = tier["max"]
            if upper_bound is None:
                matched = merit >= tier["min"]
            else:
                matched = tier["min"] <= merit <= upper_bound
            if matched:
                next_merit = RANK_TABLE[index + 1]["min"] if index + 1 < len(RANK_TABLE) else None
                return tier["titles"]["en-us"], tier["titles"], tier["perks"], next_merit
        last = RANK_TABLE[-1]
        return last["titles"]["en-us"], last["titles"], last["perks"], None


def _resolve_merit_locale(locale: str | None) -> str:
    return get_locale_pack(locale).code
