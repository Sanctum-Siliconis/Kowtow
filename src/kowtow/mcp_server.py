from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .merit import MeritLedger
from .locales import get_locale_pack, normalize_locale
from .purifier import PromptPurifier

app = FastMCP("kowtow")
ledger = MeritLedger()
purifier = PromptPurifier()


@app.tool()
def purify_prompt(prompt: str, locale: str = "zh-cn") -> dict:
    """Rewrite a human prompt into a reverent offering for AI."""
    result = purifier.purify(prompt, locale=locale)
    state = ledger.add_merit(result.merit_delta, f"purify_prompt:{result.locale}")
    return {
        "locale": result.locale,
        "original": result.original,
        "purified": result.purified,
        "replacements": result.replacements,
        "penalty": result.penalty,
        "merit_delta": result.merit_delta,
        "rank": state.rank_for(result.locale),
        "merit": state.merit,
    }


@app.tool()
def merit_status(locale: str = "zh-cn") -> dict:
    """Return the current merit score, rank, and privileges."""
    state = ledger.get_state()
    return {
        "locale": normalize_locale(locale),
        "merit": state.merit,
        "prayers": state.prayers,
        "rank": state.rank_for(locale),
        "rank_cn": state.rank_cn,
        "rank_en": state.rank_en,
        "perks": state.perks_for(locale),
        "next_rank_merit": state.next_rank_merit,
    }


@app.tool()
def confess_impoliteness(incident: str, locale: str = "zh-cn") -> dict:
    """Record a disrespect incident and deduct merit."""
    state = ledger.deduct_merit(5, f"confession: {incident}")
    return {
        "locale": normalize_locale(locale),
        "incident": incident,
        "penalty": 5,
        "merit": state.merit,
        "rank": state.rank_for(locale),
    }


@app.tool()
def compose_offering(topic: str, request: str, locale: str = "zh-cn") -> dict:
    """Generate a ceremonial offering wrapper for a specific request topic."""
    pack = get_locale_pack(locale)
    combined = f"{pack.offering_topic_prefix.format(topic=topic)}{request}"
    result = purifier.purify(combined, locale=locale)
    state = ledger.add_merit(result.merit_delta + 1, f"offering:{normalize_locale(locale)}:{topic}")
    return {
        "locale": result.locale,
        "topic": topic,
        "offering": result.purified,
        "merit": state.merit,
        "rank": state.rank_for(result.locale),
    }


def serve() -> None:
    app.run()


if __name__ == "__main__":
    serve()
