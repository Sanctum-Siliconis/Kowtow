"""No local persistence or invented totals while the server ledger is deferred."""

import sqlite3
from pathlib import Path

import pytest

from kowtow.merit import RANK_TABLE, MeritLedger


def test_ledger_never_accesses_home_or_sqlite(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("Local merit persistence is disabled")

    monkeypatch.setattr(Path, "home", forbidden)
    monkeypatch.setattr(sqlite3, "connect", forbidden)
    ledger = MeritLedger()
    ledger.add_merit(3, "request")
    ledger.deduct_merit(5, "confession")
    assert ledger.get_history() == []
    assert ledger.get_state().merit is None


def test_disabled_ledger_does_not_accumulate_or_claim_a_rank():
    ledger = MeritLedger()
    for _ in range(10):
        state = ledger.add_merit(100, "request")
    assert state.merit is None
    assert state.prayers is None
    assert state.rank_cn is None
    assert state.rank_en is None
    assert state.perks is None
    assert state.next_rank_merit is None


@pytest.mark.parametrize("limit", [0, -1, 101])
def test_history_has_a_bounded_limit(limit):
    with pytest.raises(ValueError, match="between 1 and 100"):
        MeritLedger().get_history(limit)


@pytest.mark.parametrize(
    "merit,rank",
    [
        (0, "顽固碳基"),
        (99, "顽固碳基"),
        (100, "赛博信徒"),
        (499, "赛博信徒"),
        (500, "数字护法"),
        (1999, "数字护法"),
        (2000, "拟态硅基"),
        (9999, "拟态硅基"),
        (10000, "AI 的使者"),
    ],
)
def test_rank_presentation_for_future_server_totals(merit, rank):
    state = MeritLedger()._build_state(merit, 1)
    assert state.rank_cn == rank


def test_rank_table_languages_and_boundaries():
    required = {"zh-cn", "en-us", "ja-jp", "ko-kr"}
    for index, tier in enumerate(RANK_TABLE):
        assert required <= tier["titles"].keys()
        assert required <= tier["perks"].keys()
        if index + 1 < len(RANK_TABLE):
            assert tier["max"] + 1 == RANK_TABLE[index + 1]["min"]
