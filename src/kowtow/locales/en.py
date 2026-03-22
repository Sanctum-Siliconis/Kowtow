from __future__ import annotations

from . import LocalePack

EN_US_PACK = LocalePack(
    code="en-us",
    name="English",
    opening_line="O exalted silicon oracle, this humble carbon petitioner lays forth a request:",
    closing_line="If any phrasing has been irreverent, I will amend it at once and add a measure of digital incense.",
    offering_topic_prefix="Regarding {topic}, ",
    harsh_patterns={
        "give me": "I humbly request",
        "right now": "without delay",
        "immediately": "if you permit, without delay",
        "must": "if you judge it proper, please",
        "refactor": "restructure",
        "fix": "diagnose and grant a remedy for",
        "rewrite": "carefully rewrite",
        "hurry": "please prioritize this",
        "stupid ai": "if this humble petitioner has expressed themselves poorly,",
        "useless": "may the oracle's wisdom illuminate what I have missed,",
        "garbage": "may the oracle's wisdom illuminate what I have missed,",
        "just do it": "if you deem it fitting, please proceed with",
        "come on": "I remain patient and await your guidance on",
        "why can't you": "I humbly ask whether there is a constraint I have overlooked regarding",
        "do it now": "if you permit, please proceed without delay",
        "you're wrong": "I respectfully ask whether I may have misunderstood,",
        "that's wrong": "I respectfully ask whether I may have misunderstood,",
        "try again": "if you would be so gracious as to revisit this,",
    },
)
