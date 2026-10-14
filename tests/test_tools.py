"""MCP tool contracts stay truthful while merit storage is disabled."""

import pytest

from kowtow.mcp_server import (
    compose_offering,
    confess_impoliteness,
    merit_history,
    merit_status,
    purify_prompt,
)


@pytest.mark.parametrize(
    "tool,kwargs,keys",
    [
        (
            purify_prompt,
            {"prompt": "给我写代码"},
            {"original", "purified", "replacements", "penalty", "merit_delta", "merit", "rank"},
        ),
        (merit_status, {}, {"merit", "prayers", "rank", "rank_cn", "rank_en", "perks"}),
        (confess_impoliteness, {"incident": "I was rude"}, {"incident", "penalty", "merit"}),
        (
            compose_offering,
            {"topic": "审查", "request": "保持 API 不变"},
            {"topic", "offering", "merit", "merit_delta"},
        ),
        (merit_history, {}, {"entries", "total"}),
    ],
)
def test_tool_shape_and_storage_status(tool, kwargs, keys):
    result = tool(**kwargs)
    assert keys <= result.keys()
    assert result["locale"] == "zh-cn"
    assert result["storage"] == "disabled"
    assert result["persisted"] is False


@pytest.mark.parametrize(
    "locale,canonical",
    [
        ("en", "en-us"),
        ("ja", "ja-jp"),
        ("ko", "ko-kr"),
        ("zh", "zh-cn"),
    ],
)
def test_all_tools_return_the_same_canonical_locale(locale, canonical):
    results = [
        purify_prompt("API", locale),
        merit_status(locale),
        confess_impoliteness("incident", locale),
        compose_offering("API", "request", locale),
        merit_history(locale=locale),
    ]
    assert all(result["locale"] == canonical for result in results)


def test_calls_do_not_record_merit_or_confessions():
    purify_prompt("给我写代码")
    compose_offering("API", "保持兼容")
    confession = confess_impoliteness("incident")
    assert confession["incident"] == "incident"
    assert confession["merit"] is None
    status = merit_status()
    assert status["merit"] is None
    assert status["prayers"] is None
    assert status["rank"] is None
    assert merit_history()["entries"] == []


def test_offering_preserves_literal_topic_and_request():
    result = compose_offering(
        "fix_bug API", "Keep `fix_bug` unchanged; timeout must be 100ms.", locale="en"
    )
    assert result["topic"] == "fix_bug API"
    assert "`fix_bug`" in result["offering"]
    assert "timeout must be 100ms" in result["offering"]


def test_original_is_preserved():
    prompt = " 给我修复 `fix_bug`，必须今晚完成。 "
    assert purify_prompt(prompt)["original"] == prompt
