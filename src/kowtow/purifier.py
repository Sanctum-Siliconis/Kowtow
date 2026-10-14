from __future__ import annotations

import re
from dataclasses import dataclass

from .locales import get_locale_pack
from .locales._types import RITUAL_INTENSITIES, RitualIntensity

# Rewrite only prose. Literal content, identifiers and negative constraints
# are deliberately conservative: preserving a request matters more than flair.
_PROTECTED = re.compile(
    r"(?P<fence>`{3,}|~{3,})[^\n]*\n.*?(?:(?P=fence)|\Z)"
    r"|(?P<ticks>`+).*?(?P=ticks)"
    r"|(?<!\w)\"(?:\\.|[^\"\\])*\""
    r"|(?<!\w)'(?:\\.|[^'\\])*'(?!\w)"
    r"|“[^”]*”|‘[^’]*’|「[^」]*」|『[^』]*』"
    r"|\b(?:https?|ftp)://[^\s<>]+"
    r"|(?<!\w)(?:[A-Za-z]:[\\/]|\.\.?/|~/|/)[^\s`\"'<>]+"
    r"|(?<!\w)--?[\w][\w-]*(?:=[^\s]+)?"
    r"|\b\w+(?:[_./:-]\w+)+\b"
    r"|\b(?:do not|don't|must not|never|without)\b[^.!?\n;]*"
    r"|(?:不得|不要|不能|不可|禁止|无需|不必)[^，。！？\n;；]*"
    r"|^(?: {4}|\t)[^\n]*(?:\n|\Z)",
    re.DOTALL | re.MULTILINE | re.IGNORECASE,
)


@dataclass
class PurificationResult:
    locale: str
    original: str
    purified: str
    replacements: list[tuple[str, str]]
    penalty: int
    merit_delta: int
    body: str
    intensity: RitualIntensity


class PromptPurifier:
    def purify(
        self, prompt: str, locale: str | None = None, intensity: RitualIntensity = "medium"
    ) -> PurificationResult:
        if not prompt.strip():
            raise ValueError("A petition must contain a request.")
        if intensity not in RITUAL_INTENSITIES:
            raise ValueError("Intensity must be light, medium, or heavy.")
        pack = get_locale_pack(locale)
        cleaned = prompt
        replacements: list[tuple[str, str]] = []
        sources = sorted(pack.harsh_patterns, key=len, reverse=True)
        alternatives = "|".join(re.escape(source) for source in sources)
        if pack.code == "en-us":
            alternatives = rf"(?<!\w)(?:{alternatives})(?!\w)"
        pattern = re.compile(alternatives, re.IGNORECASE if pack.code == "en-us" else 0)

        def replace(match: re.Match) -> str:
            source = match.group().lower() if pack.code == "en-us" else match.group()
            target = pack.harsh_patterns[source]
            replacement = (source, target)
            if replacement not in replacements:
                replacements.append(replacement)
            if pack.code == "en-us" and match.group()[0].isupper():
                target = target[0].upper() + target[1:]
            return target

        parts: list[str] = []
        start = 0
        for protected in _PROTECTED.finditer(cleaned):
            parts.append(pattern.sub(replace, cleaned[start : protected.start()]))
            parts.append(protected.group())
            start = protected.end()
        ends_with_literal = start == len(cleaned)
        parts.append(pattern.sub(replace, cleaned[start:]))
        cleaned = "".join(parts)
        penalty = len(replacements)

        sentence_ending = self._sentence_ending(pack.code)
        if not ends_with_literal and not cleaned.rstrip().endswith(
            ("。", "？", "！", ".", "?", "!", "`", "~")
        ):
            cleaned = f"{cleaned}{sentence_ending}"

        purified = pack.frame(cleaned, intensity)
        merit_delta = max(1, 3 - penalty)
        return PurificationResult(
            locale=pack.code,
            original=prompt,
            purified=purified,
            replacements=replacements,
            penalty=penalty,
            merit_delta=merit_delta,
            body=cleaned,
            intensity=intensity,
        )

    @staticmethod
    def _sentence_ending(locale: str) -> str:
        if locale in {"zh-cn", "ja-jp"}:
            return "。"
        return "."
