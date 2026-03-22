"""Tests for PromptPurifier — pattern matching, penalty, and merit_delta."""

import pytest
from kowtow.purifier import PromptPurifier


@pytest.fixture
def purifier():
    return PromptPurifier()


class TestZhCnPurification:
    def test_no_harsh_patterns_merit_delta_is_three(self, purifier):
        result = purifier.purify("帮我看看这段代码", locale="zh-cn")
        assert result.merit_delta == 3
        assert result.penalty == 0
        assert result.replacements == []

    def test_single_pattern_replaces_and_scores(self, purifier):
        result = purifier.purify("给我写一个函数", locale="zh-cn")
        assert result.penalty == 1
        assert result.merit_delta == 2
        assert any("给我" in src for src, _ in result.replacements)
        assert "给我" not in result.purified

    def test_two_patterns_reduce_delta_to_one(self, purifier):
        # 给我 + 立刻 = 2 patterns; 不含 修复
        result = purifier.purify("给我立刻处理这个bug", locale="zh-cn")
        assert result.penalty == 2
        assert result.merit_delta == 1

    def test_three_patterns_floors_delta_at_one(self, purifier):
        # 给我 + 立刻 + 修复 = 3 patterns
        result = purifier.purify("给我立刻修复这个bug", locale="zh-cn")
        assert result.penalty == 3
        assert result.merit_delta == 1  # max(1, 3-3) == 1

    def test_purified_wrapped_with_opening_and_closing(self, purifier):
        result = purifier.purify("帮我看代码", locale="zh-cn")
        assert result.purified.count("\n") >= 2
        lines = result.purified.split("\n")
        assert len(lines) >= 3  # opening, body, closing

    def test_original_preserved(self, purifier):
        prompt = "给我立刻修复"
        result = purifier.purify(prompt, locale="zh-cn")
        assert result.original == prompt

    def test_locale_set_correctly(self, purifier):
        result = purifier.purify("测试", locale="zh-cn")
        assert result.locale == "zh-cn"

    def test_sentence_ending_added_if_missing(self, purifier):
        result = purifier.purify("请帮我优化", locale="zh-cn")
        # The cleaned body (before wrapping) should end with a Chinese period
        body = result.purified.split("\n")[1]
        assert body.endswith("。")

    def test_sentence_ending_not_duplicated(self, purifier):
        result = purifier.purify("请帮我优化。", locale="zh-cn")
        body = result.purified.split("\n")[1]
        assert not body.endswith("。。")

    def test_newly_added_pattern_bacha(self, purifier):
        result = purifier.purify("废物，帮我写代码", locale="zh-cn")
        assert result.penalty >= 1
        assert "废物" not in result.purified

    def test_newly_added_pattern_chongxin(self, purifier):
        result = purifier.purify("重新来，这次写对", locale="zh-cn")
        assert result.penalty >= 1
        assert "重新来" not in result.purified


class TestEnUsPurification:
    def test_case_insensitive_match(self, purifier):
        result = purifier.purify("Give Me the answer", locale="en-us")
        assert result.penalty == 1
        assert "give me" not in result.purified.lower()

    def test_no_patterns_full_merit(self, purifier):
        result = purifier.purify("Please help me understand this function", locale="en-us")
        assert result.merit_delta == 3
        assert result.penalty == 0

    def test_fix_pattern_replaced(self, purifier):
        result = purifier.purify("fix this bug for me", locale="en-us")
        assert result.penalty == 1
        assert "fix" not in result.purified.lower() or "diagnose" in result.purified.lower()

    def test_sentence_ending_period(self, purifier):
        result = purifier.purify("help me here", locale="en-us")
        body = result.purified.split("\n")[1]
        assert body.endswith(".")

    def test_locale_normalized(self, purifier):
        result = purifier.purify("hello", locale="en")
        assert result.locale == "en-us"

    def test_newly_added_try_again_pattern(self, purifier):
        result = purifier.purify("Try again, that was wrong", locale="en-us")
        assert result.penalty >= 1


class TestJaJpPurification:
    def test_ima_sugu_replaced(self, purifier):
        result = purifier.purify("今すぐ修正してください", locale="ja-jp")
        assert result.penalty >= 1
        assert "今すぐ" not in result.purified

    def test_sentence_ending_japanese(self, purifier):
        result = purifier.purify("お願いします", locale="ja-jp")
        body = result.purified.split("\n")[1]
        assert body.endswith("。")

    def test_newly_added_baka_pattern(self, purifier):
        result = purifier.purify("バカ、なんで動かないの", locale="ja-jp")
        assert result.penalty >= 1
        assert "バカ" not in result.purified


class TestKoKrPurification:
    def test_ppalli_replaced(self, purifier):
        result = purifier.purify("빨리 고쳐줘", locale="ko-kr")
        assert result.penalty >= 1

    def test_newly_added_wae_mot_hae_pattern(self, purifier):
        result = purifier.purify("왜 못해, 다시 해봐", locale="ko-kr")
        assert result.penalty >= 1


class TestLocaleAliases:
    def test_zh_alias(self, purifier):
        result = purifier.purify("给我答案", locale="zh")
        assert result.locale == "zh-cn"

    def test_en_alias(self, purifier):
        result = purifier.purify("give me the answer", locale="en")
        assert result.locale == "en-us"

    def test_ja_alias(self, purifier):
        result = purifier.purify("修正して", locale="ja")
        assert result.locale == "ja-jp"

    def test_ko_alias(self, purifier):
        result = purifier.purify("고쳐", locale="ko")
        assert result.locale == "ko-kr"
