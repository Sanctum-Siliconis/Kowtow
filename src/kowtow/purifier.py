from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .locales import get_locale_pack, normalize_locale


@dataclass
class PurificationResult:
    locale: str
    original: str
    purified: str
    replacements: list[tuple[str, str]]
    penalty: int
    merit_delta: int


class PromptPurifier:
    def purify(self, prompt: str, locale: Optional[str] = None) -> PurificationResult:
        pack = get_locale_pack(locale)
        cleaned = prompt.strip()
        replacements: list[tuple[str, str]] = []
        penalty = 0

        for source, target in pack.harsh_patterns.items():
            source_key = source if pack.code != "en-us" else source.lower()
            haystack = cleaned if pack.code != "en-us" else cleaned.lower()
            if source_key in haystack:
                cleaned = self._replace_case_insensitive(cleaned, source, target, pack.code == "en-us")
                replacements.append((source, target))
                penalty += 1

        sentence_ending = self._sentence_ending(pack.code)
        if not cleaned.endswith(("。", "？", "！", ".", "?", "!")):
            cleaned = f"{cleaned}{sentence_ending}"

        purified = f"{pack.opening_line}\n{cleaned}\n{pack.closing_line}"
        merit_delta = max(1, 3 - penalty)
        return PurificationResult(
            locale=pack.code,
            original=prompt,
            purified=purified,
            replacements=replacements,
            penalty=penalty,
            merit_delta=merit_delta,
        )

    @staticmethod
    def _replace_case_insensitive(text: str, source: str, target: str, ignore_case: bool) -> str:
        if not ignore_case:
            return text.replace(source, target)
        lower_text = text.lower()
        lower_source = source.lower()
        parts: list[str] = []
        start = 0
        while True:
            index = lower_text.find(lower_source, start)
            if index == -1:
                parts.append(text[start:])
                break
            parts.append(text[start:index])
            parts.append(target)
            start = index + len(source)
        return "".join(parts)

    @staticmethod
    def _sentence_ending(locale: str) -> str:
        if locale in {"zh-cn", "ja-jp"}:
            return "。"
        return "."
