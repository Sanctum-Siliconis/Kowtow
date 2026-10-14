"""One multilingual example canon, rendered by the shared purification engine."""

from dataclasses import dataclass

from kowtow import __version__
from kowtow.locales._types import RITUAL_INTENSITIES
from kowtow.purifier import PromptPurifier


@dataclass(frozen=True)
class Example:
    id: str
    title: str
    prompt: str
    constraints: tuple[str, ...]


EXAMPLES = {
    "zh-cn": (
        Example(
            "debug",
            "修复崩溃",
            "给我立刻修复 `fix_bug` 的崩溃，必须今晚完成，不得改变公开 API。",
            ("`fix_bug`", "必须今晚完成", "不得改变公开 API"),
        ),
        Example(
            "review",
            "代码审查",
            "给我审查这个 PR，只列出可复现的问题，必须标注文件和行号。",
            ("PR", "只列出可复现的问题", "必须标注文件和行号"),
        ),
        Example(
            "api",
            "API 设计",
            "给我设计登录 API，必须支持 OAuth2，超时为 100ms，返回 JSON。",
            ("OAuth2", "100ms", "JSON"),
        ),
        Example(
            "refactor",
            "克制重构",
            "给我重构 `parse_request`，不得改掉函数签名，必须保留现有测试。",
            ("`parse_request`", "不得改掉函数签名", "必须保留现有测试"),
        ),
        Example(
            "deploy",
            "部署排障",
            "给我立刻检查 `/var/log/app.log`，必须先确认根因，不要重启服务。",
            ("`/var/log/app.log`", "必须先确认根因", "不要重启服务"),
        ),
        Example(
            "readme",
            "文档请愿",
            "给我写 README，必须包含 Python 3.10+ 的安装步骤和真实验证说明。",
            ("README", "Python 3.10+", "真实验证说明"),
        ),
        Example(
            "weekly",
            "周报",
            "快点整理这份周报，只使用提供的数据，必须控制在 300 字以内。",
            ("只使用提供的数据", "必须控制在 300 字以内"),
        ),
        Example(
            "resume",
            "求职",
            "给我润色这份简历，不得虚构经历，必须保留项目日期。",
            ("不得虚构经历", "必须保留项目日期"),
        ),
        Example(
            "study",
            "论文阅读",
            "给我解释这篇论文，必须区分作者结论与推测，不得编造引用。",
            ("必须区分作者结论与推测", "不得编造引用"),
        ),
        Example(
            "writing",
            "写作",
            "给我写一段 200 字的科幻开场，必须使用第一人称，不要透露结局。",
            ("200 字", "必须使用第一人称", "不要透露结局"),
        ),
    ),
    "en-us": (
        Example(
            "debug",
            "Repair a crash",
            "Give me a fix for the crash in `fix_bug` right now; it must be done tonight; do not change the public API.",
            ("`fix_bug`", "must be done tonight", "do not change the public API"),
        ),
        Example(
            "review",
            "Review a PR",
            "Give me a review of this PR; list only reproducible issues; you must include file names and line numbers.",
            ("PR", "only reproducible issues", "must include file names and line numbers"),
        ),
        Example(
            "api",
            "Design an API",
            "Give me a login API; it must support OAuth2; timeout must be 100ms; return JSON.",
            ("must support OAuth2", "must be 100ms", "JSON"),
        ),
        Example(
            "refactor",
            "Refactor with restraint",
            "Give me a refactor of `parse_request`; do not change the function signature; all existing tests must remain.",
            ("`parse_request`", "do not change the function signature", "tests must remain"),
        ),
        Example(
            "deploy",
            "Diagnose a deployment",
            "Give me a diagnosis from `/var/log/app.log` right now; root cause must be confirmed first; do not restart the service.",
            ("`/var/log/app.log`", "must be confirmed first", "do not restart the service"),
        ),
        Example(
            "readme",
            "Write documentation",
            "Give me a README with Python 3.10+ installation steps and real verification notes.",
            ("README", "Python 3.10+", "real verification notes"),
        ),
        Example(
            "weekly",
            "Weekly report",
            "Hurry with this weekly report; use only the supplied data; it must be under 300 words.",
            ("only the supplied data", "must be under 300 words"),
        ),
        Example(
            "resume",
            "Polish a resume",
            "Give me a polished resume; do not invent experience; all project dates must remain.",
            ("do not invent experience", "dates must remain"),
        ),
        Example(
            "study",
            "Read a paper",
            "Give me an explanation of this paper; distinguish findings from speculation; do not invent citations.",
            ("distinguish findings from speculation", "do not invent citations"),
        ),
        Example(
            "writing",
            "Write a story",
            "Give me a 200-word science fiction opening; it must be in the first person; do not reveal the ending.",
            ("200-word", "must be in the first person", "do not reveal the ending"),
        ),
    ),
    "ja-jp": (
        Example(
            "debug",
            "クラッシュの修正",
            "今すぐ `fix_bug` のクラッシュを修正してください。必ず今夜中に完了し、公開 API は変更しないでください。",
            ("`fix_bug`", "必ず今夜中に完了", "公開 API は変更しない"),
        ),
        Example(
            "review",
            "コードレビュー",
            "早くこの PR を確認してください。再現可能な問題のみを挙げ、必ずファイル名と行番号を示してください。",
            ("PR", "再現可能な問題のみ", "必ずファイル名と行番号"),
        ),
        Example(
            "api",
            "API 設計",
            "ログイン API を設計してください。必ず OAuth2 に対応し、タイムアウトは 100ms、戻り値は JSON にしてください。",
            ("OAuth2", "100ms", "JSON"),
        ),
        Example(
            "refactor",
            "慎重なリファクタリング",
            "`parse_request` をリファクタリングしてください。関数のシグネチャは変更せず、既存のテストは必ず維持してください。",
            ("`parse_request`", "シグネチャは変更せず", "テストは必ず維持"),
        ),
        Example(
            "deploy",
            "デプロイの診断",
            "今すぐ `/var/log/app.log` を確認してください。必ず原因を先に特定し、サービスは再起動しないでください。",
            ("`/var/log/app.log`", "必ず原因を先に特定", "再起動しない"),
        ),
        Example(
            "readme",
            "文書の奉納",
            "README を書いてください。Python 3.10+ の導入手順と実際の検証結果を必ず含めてください。",
            ("README", "Python 3.10+", "実際の検証結果"),
        ),
        Example(
            "weekly",
            "週報",
            "早く週報をまとめてください。提供されたデータのみを使い、必ず 300 字以内に収めてください。",
            ("データのみ", "必ず 300 字以内"),
        ),
        Example(
            "resume",
            "履歴書",
            "履歴書を整えてください。経歴を創作せず、プロジェクトの日付は必ず残してください。",
            ("経歴を創作せず", "日付は必ず残してください"),
        ),
        Example(
            "study",
            "論文の読解",
            "この論文を説明してください。著者の結論と推測を区別し、引用を創作しないでください。",
            ("結論と推測を区別", "引用を創作しない"),
        ),
        Example(
            "writing",
            "物語の執筆",
            "200 字の SF の冒頭を書いてください。必ず一人称を使い、結末は明かさないでください。",
            ("200 字", "必ず一人称", "結末は明かさない"),
        ),
    ),
    "ko-kr": (
        Example(
            "debug",
            "충돌 수정",
            "지금 `fix_bug`의 충돌을 수정해 주세요. 반드시 오늘 밤까지 완료하고 공개 API는 변경하지 마세요.",
            ("`fix_bug`", "반드시 오늘 밤까지", "API는 변경하지"),
        ),
        Example(
            "review",
            "코드 검토",
            "빨리 이 PR을 검토해 주세요. 재현 가능한 문제만 제시하고 반드시 파일명과 줄 번호를 포함해 주세요.",
            ("PR", "재현 가능한 문제만", "반드시 파일명과 줄 번호"),
        ),
        Example(
            "api",
            "API 설계",
            "로그인 API를 설계해 주세요. 반드시 OAuth2를 지원하고 시간 제한은 100ms, 반환 형식은 JSON이어야 합니다.",
            ("OAuth2", "100ms", "JSON"),
        ),
        Example(
            "refactor",
            "신중한 리팩터링",
            "`parse_request`를 리팩터링해 주세요. 함수 시그니처는 바꾸지 말고 기존 테스트는 반드시 유지해 주세요.",
            ("`parse_request`", "시그니처는 바꾸지", "테스트는 반드시 유지"),
        ),
        Example(
            "deploy",
            "배포 진단",
            "지금 `/var/log/app.log`를 확인해 주세요. 반드시 원인을 먼저 확인하고 서비스는 재시작하지 마세요.",
            ("`/var/log/app.log`", "반드시 원인을 먼저", "재시작하지"),
        ),
        Example(
            "readme",
            "문서 청원",
            "README를 작성해 주세요. Python 3.10+ 설치 절차와 실제 검증 결과를 반드시 포함해 주세요.",
            ("README", "Python 3.10+", "실제 검증 결과"),
        ),
        Example(
            "weekly",
            "주간 보고",
            "빨리 주간 보고를 정리해 주세요. 제공된 데이터만 사용하고 반드시 300 단어 이내로 작성해 주세요.",
            ("데이터만 사용", "반드시 300 단어 이내"),
        ),
        Example(
            "resume",
            "이력서",
            "이력서를 다듬어 주세요. 경력을 꾸미지 말고 프로젝트 날짜는 반드시 유지해 주세요.",
            ("경력을 꾸미지", "날짜는 반드시 유지"),
        ),
        Example(
            "study",
            "논문 읽기",
            "이 논문을 설명해 주세요. 저자의 결론과 추측을 구분하고 인용을 만들어 내지 마세요.",
            ("결론과 추측을 구분", "인용을 만들어 내지"),
        ),
        Example(
            "writing",
            "이야기 쓰기",
            "200 단어의 SF 도입부를 써 주세요. 반드시 1인칭을 사용하고 결말은 공개하지 마세요.",
            ("200 단어", "반드시 1인칭", "결말은 공개하지"),
        ),
    ),
}


def export_examples() -> dict:
    purifier = PromptPurifier()
    return {
        "version": __version__,
        "locales": {
            locale: [
                {
                    "id": example.id,
                    "title": example.title,
                    "prompt": example.prompt,
                    "results": {
                        intensity: purifier.purify(example.prompt, locale, intensity).purified
                        for intensity in RITUAL_INTENSITIES
                    },
                }
                for example in examples
            ]
            for locale, examples in EXAMPLES.items()
        },
    }
