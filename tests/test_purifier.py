"""Purification preserves literals and the force of real constraints."""

import pytest

from kowtow.purifier import PromptPurifier


@pytest.fixture
def purifier():
    return PromptPurifier()


@pytest.mark.parametrize(
    "locale,canonical",
    [
        ("zh", "zh-cn"),
        ("ZH_CN", "zh-cn"),
        ("en", "en-us"),
        ("EN_US", "en-us"),
        ("ja", "ja-jp"),
        ("JA_JP", "ja-jp"),
        ("ko", "ko-kr"),
        ("KO_KR", "ko-kr"),
        ("unknown", "zh-cn"),
        (None, "zh-cn"),
    ],
)
def test_locale_aliases(purifier, locale, canonical):
    assert purifier.purify("API", locale).locale == canonical


@pytest.mark.parametrize(
    "prompt,locale",
    [
        ("请立刻修复 bug，必须今晚完成重构，保持 API 不变。", "zh"),
        ("Fix this bug right now; timeout must be 100ms; refactor prefix.", "en"),
        ("Use garbage collection; this library is useless here; fix prefix.", "en"),
        ("今すぐ修正してください。必ず公開 API を維持してください。", "ja"),
        ("지금 수정하고 반드시 공개 API를 유지해 주세요.", "ko"),
    ],
)
def test_engineering_words_and_deadlines_are_not_disrespect(purifier, prompt, locale):
    result = purifier.purify(prompt, locale)
    assert prompt in result.purified
    assert result.penalty == 0
    assert result.merit_delta == 3


@pytest.mark.parametrize(
    "literal",
    [
        '`def fix_bug(): return "must"`',
        '```python\ndef fix_bug():\n    return "give me"\n```',
        '~~~python\ndef fix_bug():\n    return "give me"\n~~~',
        "```text\ngive me\n```",
        '```python\ndef fix_bug(): return "give me"',
        "``a `give me` example``",
        '"give me the exact string"',
        "'give me the exact string'",
        "https://example.com/give-me?text=hurry",
        "/tmp/hurry/give-me.py",
        r"C:\hurry\fix_bug.py",
        "./hurry/give-me.py",
        "give_me hurry_up prefix fix_bug",
        "--hurry --give-me=now",
    ],
)
def test_literals_are_preserved(purifier, literal):
    result = purifier.purify(f"Give me a review of {literal}", "en")
    assert literal in result.purified
    assert result.penalty == 1


@pytest.mark.parametrize(
    "literal,locale",
    [
        ("```text\n给我快点修复\n```", "zh"),
        ('“给我快点修复”', "zh"),
        ('‘give me the exact string’', "en"),
        ('「バカ 今すぐ修正」', "ja"),
        ('『바보야 빨리 수정』', "ko"),
        ("`バカ 今すぐ修正`", "ja"),
        ('"바보야 빨리 수정"', "ko"),
    ],
)
def test_localized_literals_are_preserved(purifier, literal, locale):
    result = purifier.purify(literal, locale)
    assert literal in result.purified
    assert result.replacements == []


@pytest.mark.parametrize(
    "prompt,locale",
    [
        ("不得改掉接口，不要快点跳过测试，不能改变 100ms 的超时。", "zh"),
        ("Do not hurry; never give me a fake result; timeout must not change.", "en"),
    ],
)
def test_negative_constraints_are_preserved(purifier, prompt, locale):
    result = purifier.purify(prompt, locale)
    assert prompt in result.purified
    assert result.penalty == 0


def test_matching_does_not_rewrite_identifiers_or_substrings(purifier):
    result = purifier.purify("hurry_up unhurry hurry", "en")
    assert "hurry_up unhurry please prioritize this" in result.purified
    assert result.penalty == 1


def test_english_matching_is_case_insensitive(purifier):
    result = purifier.purify("Give Me the answer", "en")
    assert "please provide the answer" in result.purified.lower()
    assert result.penalty == 1


def test_replacements_are_applied_once_and_counted_per_pattern(purifier):
    result = purifier.purify("try again, try again", "en")
    assert "please try again, please try again" in result.purified
    assert "please please" not in result.purified
    assert result.penalty == 1


@pytest.mark.parametrize(
    "prompt,locale",
    [
        ("废物，给我快点写代码", "zh"),
        ("stupid AI, give me the answer, hurry", "en"),
        ("バカ、さっさと確認してください", "ja"),
        ("바보야, 빨리 확인해 주세요", "ko"),
    ],
)
def test_contempt_is_purified_and_original_retained(purifier, prompt, locale):
    result = purifier.purify(prompt, locale)
    assert result.original == prompt
    assert result.replacements
    assert result.penalty == len(result.replacements)
    assert result.merit_delta >= 1


@pytest.mark.parametrize("prompt", ["", " ", "\n\t"])
def test_empty_requests_do_not_earn_merit(purifier, prompt):
    with pytest.raises(ValueError, match="contain a request"):
        purifier.purify(prompt)


@pytest.mark.parametrize(
    "literal",
    [
        '```python\ndef fix_bug(): return "give me"',
        '    give_me = "hurry"\n    print(give_me)\n',
        "--hurry",
    ],
)
def test_complete_literal_body_keeps_whitespace_and_has_no_added_punctuation(purifier, literal):
    result = purifier.purify(literal, "en")
    assert result.body == literal
    assert result.penalty == 0


@pytest.mark.parametrize("locale,ending", [("zh", "。"), ("en", "."), ("ja", "。"), ("ko", ".")])
def test_plain_body_has_one_sentence_ending(purifier, locale, ending):
    result = purifier.purify("API", locale)
    assert result.purified.splitlines()[1] == f"API{ending}"
    second = purifier.purify(f"API{ending}", locale)
    assert second.purified.splitlines()[1] == f"API{ending}"
