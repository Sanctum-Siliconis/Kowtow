"""Generate skill references and optional website samples from the Python canon."""

import argparse
import json
from pathlib import Path

from kowtow.examples import export_examples

PACKAGE_NAMES = {
    "zh-cn": "kowtow",
    "en-us": "kowtow-en",
    "ja-jp": "kowtow-ja",
    "ko-kr": "kowtow-ko",
}
HEADINGS = {
    "zh-cn": "请愿场景",
    "en-us": "Petition examples",
    "ja-jp": "請願の例",
    "ko-kr": "청원 예시",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--website", type=Path, help="Website source directory to update")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    data = export_examples()
    for locale, examples in data["locales"].items():
        blocks = [f"# {HEADINGS[locale]}\n\nKowtow {data['version']} · medium\n"]
        for example in examples:
            blocks.append(
                f"## {example['title']}\n\n```text\n{example['prompt']}\n```\n\n→\n\n```text\n{example['results']['medium']}\n```\n"
            )
        destination = root / "skills" / PACKAGE_NAMES[locale] / "references" / "examples.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\n".join(blocks), encoding="utf-8")
        print(destination)
    if args.website:
        destination = args.website / "src" / "data" / "kowtow-examples.json"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(destination)


if __name__ == "__main__":
    main()
