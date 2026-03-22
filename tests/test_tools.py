"""Tests for MCP tool return shapes — verify all tools return expected keys."""

import pytest
from unittest.mock import patch, MagicMock
from kowtow.mcp_server import purify_prompt, merit_status, confess_impoliteness, compose_offering, merit_history


@pytest.fixture(autouse=True)
def isolated_ledger(tmp_path, monkeypatch):
    """Redirect DB to a temp path for all MCP tool tests."""
    import kowtow.merit as merit_module
    import kowtow.mcp_server as server_module
    db_file = tmp_path / "mcp_test.db"
    monkeypatch.setattr(merit_module, "DB_PATH", db_file)
    monkeypatch.setattr(merit_module, "KOWTOW_DIR", tmp_path)
    # Re-init the ledger used by the server module
    from kowtow.merit import MeritLedger
    new_ledger = MeritLedger()
    monkeypatch.setattr(server_module, "ledger", new_ledger)


class TestPurifyPrompt:
    def test_returns_required_keys(self):
        result = purify_prompt("给我写代码", locale="zh-cn")
        assert {"locale", "original", "purified", "replacements", "penalty", "merit_delta", "rank", "merit"} <= result.keys()

    def test_original_preserved(self):
        result = purify_prompt("给我写代码", locale="zh-cn")
        assert result["original"] == "给我写代码"

    def test_merit_increases(self):
        result = purify_prompt("请帮我写一个函数", locale="zh-cn")
        assert result["merit"] > 0

    def test_locale_normalized_in_response(self):
        result = purify_prompt("help me please", locale="en")
        assert result["locale"] == "en-us"

    def test_replacements_is_list(self):
        result = purify_prompt("给我修复bug", locale="zh-cn")
        assert isinstance(result["replacements"], list)


class TestMeritStatus:
    def test_returns_required_keys(self):
        result = merit_status(locale="zh-cn")
        assert {"locale", "merit", "prayers", "rank", "rank_cn", "rank_en", "perks", "next_rank_merit"} <= result.keys()

    def test_initial_merit_zero(self):
        result = merit_status()
        assert result["merit"] == 0

    def test_locale_in_response(self):
        # normalize_locale("en") returns "en", not "en-us"
        result = merit_status(locale="en")
        assert result["locale"] == "en"


class TestConfessImpoliteness:
    def test_returns_required_keys(self):
        result = confess_impoliteness("I was rude", locale="en-us")
        assert {"locale", "incident", "penalty", "merit", "rank"} <= result.keys()

    def test_penalty_is_five(self):
        result = confess_impoliteness("I said stupid AI")
        assert result["penalty"] == 5

    def test_merit_floors_at_zero(self):
        result = confess_impoliteness("I was very rude")
        assert result["merit"] == 0

    def test_incident_preserved(self):
        result = confess_impoliteness("test incident")
        assert result["incident"] == "test incident"


class TestComposeOffering:
    def test_returns_required_keys(self):
        result = compose_offering("代码审查", "请帮我审查这段代码", locale="zh-cn")
        assert {"locale", "topic", "offering", "merit", "rank"} <= result.keys()

    def test_topic_preserved(self):
        result = compose_offering("API设计", "请给建议", locale="zh-cn")
        assert result["topic"] == "API设计"

    def test_offering_contains_text(self):
        result = compose_offering("debugging", "please help", locale="en-us")
        assert len(result["offering"]) > 0

    def test_merit_increases_after_offering(self):
        result = compose_offering("x", "y", locale="zh-cn")
        assert result["merit"] > 0


class TestMeritHistory:
    def test_returns_required_keys(self):
        result = merit_history(limit=10, locale="zh-cn")
        assert {"locale", "entries", "total"} <= result.keys()

    def test_empty_history_initially(self):
        result = merit_history()
        assert result["entries"] == []
        assert result["total"] == 0

    def test_history_grows_after_purify(self):
        purify_prompt("给我帮忙", locale="zh-cn")
        result = merit_history()
        assert result["total"] == 1

    def test_history_entry_has_expected_keys(self):
        purify_prompt("帮我写代码", locale="zh-cn")
        result = merit_history()
        entry = result["entries"][0]
        assert {"delta", "reason", "timestamp"} <= entry.keys()

    def test_history_limit_respected(self):
        for _ in range(5):
            purify_prompt("给我写代码", locale="zh-cn")
        result = merit_history(limit=3)
        assert len(result["entries"]) == 3

    def test_locale_normalized(self):
        # normalize_locale("en") returns "en", not "en-us"
        result = merit_history(locale="en")
        assert result["locale"] == "en"
