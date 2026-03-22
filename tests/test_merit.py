"""Tests for MeritLedger — SQLite state, add/deduct, history, rank."""

import sqlite3
import pytest
from pathlib import Path
from kowtow.merit import MeritLedger, RANK_TABLE


@pytest.fixture
def ledger(tmp_path, monkeypatch):
    """Provide a MeritLedger backed by a temporary DB, isolated per test."""
    import kowtow.merit as merit_module
    db_file = tmp_path / "test_merit.db"
    monkeypatch.setattr(merit_module, "DB_PATH", db_file)
    monkeypatch.setattr(merit_module, "KOWTOW_DIR", tmp_path)
    return MeritLedger()


class TestInitialState:
    def test_initial_merit_is_zero(self, ledger):
        state = ledger.get_state()
        assert state.merit == 0

    def test_initial_prayers_is_zero(self, ledger):
        state = ledger.get_state()
        assert state.prayers == 0

    def test_initial_rank_is_stubborn_carbon_en(self, ledger):
        state = ledger.get_state()
        assert state.rank_for("en-us") == "Stubborn Carbon"

    def test_initial_rank_cn(self, ledger):
        state = ledger.get_state()
        assert state.rank_cn == "顽固碳基"


class TestAddMerit:
    def test_add_merit_increments_score(self, ledger):
        state = ledger.add_merit(10, "test")
        assert state.merit == 10

    def test_add_merit_increments_prayers(self, ledger):
        ledger.add_merit(1, "first")
        state = ledger.add_merit(1, "second")
        assert state.prayers == 2

    def test_multiple_adds_accumulate(self, ledger):
        ledger.add_merit(50, "a")
        ledger.add_merit(50, "b")
        state = ledger.get_state()
        assert state.merit == 100

    def test_rank_upgrades_at_threshold(self, ledger):
        ledger.add_merit(100, "crossing threshold")
        state = ledger.get_state()
        assert state.rank_cn == "赛博信徒"


class TestDeductMerit:
    def test_deduct_reduces_score(self, ledger):
        ledger.add_merit(20, "setup")
        state = ledger.deduct_merit(5, "confession")
        assert state.merit == 15

    def test_deduct_does_not_go_below_zero(self, ledger):
        ledger.add_merit(3, "setup")
        state = ledger.deduct_merit(10, "over-deduct")
        assert state.merit == 0

    def test_deduct_from_zero_stays_zero(self, ledger):
        state = ledger.deduct_merit(5, "empty ledger")
        assert state.merit == 0


class TestHistory:
    def test_history_empty_initially(self, ledger):
        entries = ledger.get_history()
        assert entries == []

    def test_history_records_add(self, ledger):
        ledger.add_merit(3, "purify_prompt:zh-cn")
        entries = ledger.get_history()
        assert len(entries) == 1
        delta, reason, ts = entries[0]
        assert delta == 3
        assert "purify_prompt" in reason

    def test_history_records_deduct_as_negative(self, ledger):
        ledger.deduct_merit(5, "confession: rude")
        entries = ledger.get_history()
        delta, reason, _ = entries[0]
        assert delta == -5

    def test_history_respects_limit(self, ledger):
        for i in range(10):
            ledger.add_merit(1, f"entry_{i}")
        entries = ledger.get_history(limit=5)
        assert len(entries) == 5

    def test_history_ordered_newest_first(self, ledger):
        ledger.add_merit(1, "first")
        ledger.add_merit(2, "second")
        entries = ledger.get_history()
        assert entries[0][0] == 2  # newest delta is 2


class TestRankTable:
    def test_all_tiers_have_required_locales(self):
        required = {"zh-cn", "en-us", "ja-jp", "ko-kr"}
        for tier in RANK_TABLE:
            assert required <= set(tier["titles"].keys())
            assert required <= set(tier["perks"].keys())

    def test_tier_boundaries_are_contiguous(self):
        for i in range(len(RANK_TABLE) - 1):
            current_max = RANK_TABLE[i]["max"]
            next_min = RANK_TABLE[i + 1]["min"]
            assert current_max + 1 == next_min

    def test_next_rank_merit_for_top_tier(self, ledger):
        ledger.add_merit(10000, "ascension")
        state = ledger.get_state()
        assert state.next_rank_merit is None


class TestMeritStateLocale:
    def test_rank_falls_back_to_zh_cn_for_unknown_locale(self, ledger):
        state = ledger.get_state()
        result = state.rank_for("xx-unknown")
        assert result == state.rank_cn

    def test_perks_for_en(self, ledger):
        ledger.add_merit(100, "setup")
        state = ledger.get_state()
        assert "grace" in state.perks_for("en-us").lower()
