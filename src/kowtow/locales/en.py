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
    },
)
