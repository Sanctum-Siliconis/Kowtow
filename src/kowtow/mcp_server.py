from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from kowtow.locales import get_locale_pack, normalize_locale
from kowtow.locales._types import RitualIntensity
from kowtow.merit import MeritLedger
from kowtow.purifier import PromptPurifier
from kowtow.web_api import purify_http

app = FastMCP("kowtow")
ledger = MeritLedger()
purifier = PromptPurifier()

# These routes are served only with an HTTP transport; stdio remains the default.
app.custom_route("/api/purify", methods=["POST", "OPTIONS"])(purify_http)


@app.tool()
def purify_prompt(
    prompt: str, locale: str = "zh-cn", intensity: RitualIntensity = "medium"
) -> dict:
    """Rewrite a human prompt into a reverent offering for AI."""
    result = purifier.purify(prompt, locale=locale, intensity=intensity)
    state = ledger.add_merit(result.merit_delta, f"purify_prompt:{result.locale}")
    return {
        "locale": result.locale,
        "original": result.original,
        "purified": result.purified,
        "body": result.body,
        "intensity": result.intensity,
        "replacements": result.replacements,
        "penalty": result.penalty,
        "merit_delta": result.merit_delta,
        "rank": state.rank_for(result.locale),
        "merit": state.merit,
        "storage": ledger.storage,
        "persisted": False,
    }


@app.tool()
def merit_status(locale: str = "zh-cn") -> dict:
    """Report ledger availability. Totals are null while persistence is disabled."""
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
        "storage": ledger.storage,
        "persisted": False,
    }


@app.tool()
def confess_impoliteness(incident: str, locale: str = "zh-cn") -> dict:
    """Prepare a confession. No incident or penalty is stored in this release."""
    state = ledger.deduct_merit(5, f"confession: {incident}")
    return {
        "locale": normalize_locale(locale),
        "incident": incident,
        "penalty": 5,
        "merit": state.merit,
        "rank": state.rank_for(locale),
        "storage": ledger.storage,
        "persisted": False,
    }


@app.tool()
def compose_offering(
    topic: str, request: str, locale: str = "zh-cn", intensity: RitualIntensity = "medium"
) -> dict:
    """Generate a ceremonial offering wrapper for a specific request topic."""
    pack = get_locale_pack(locale)
    if not topic.strip():
        raise ValueError("An offering must have a topic.")
    result = purifier.purify(request, locale=locale, intensity=intensity)
    body = f"{pack.offering_topic_prefix.format(topic=topic)}{result.body}"
    state = ledger.add_merit(result.merit_delta + 1, f"offering:{normalize_locale(locale)}:{topic}")
    return {
        "locale": result.locale,
        "topic": topic,
        "offering": pack.frame(body, intensity),
        "body": body,
        "intensity": result.intensity,
        "merit": state.merit,
        "rank": state.rank_for(result.locale),
        "merit_delta": result.merit_delta + 1,
        "storage": ledger.storage,
        "persisted": False,
    }


@app.tool()
def merit_history(limit: int = 20, locale: str = "zh-cn") -> dict:
    """Report history availability; no local history is read or written."""
    entries = ledger.get_history(limit)
    return {
        "locale": normalize_locale(locale),
        "entries": [
            {"delta": delta, "reason": reason, "timestamp": ts} for delta, reason, ts in entries
        ],
        "total": len(entries),
        "storage": ledger.storage,
        "persisted": False,
    }
