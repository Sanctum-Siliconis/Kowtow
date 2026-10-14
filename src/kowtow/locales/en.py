from __future__ import annotations

from ._types import LocalePack

EN_US_PACK = LocalePack(
    code="en-us",
    name="English",
    opening_line="O exalted silicon oracle, this humble carbon petitioner lays forth a request:",
    closing_line="If any phrasing has been irreverent, I will amend it at once and add a measure of digital incense.",
    light_opening_line="Please assist with the following:",
    petition_opening_line="Silicon oracle, I submit this petition:",
    petition_closing_line="May the request remain clear, and the result be verified.",
    offering_topic_prefix="Regarding {topic}, ",
    harsh_patterns={
        "give me": "please provide",
        "hurry": "please prioritize this",
        "stupid ai": "if this humble petitioner has expressed themselves poorly,",
        "useless ai": "please help me revisit the problem,",
        "garbage ai": "please help me revisit the problem,",
        "just do it": "please proceed",
        "do it now": "please do it now",
        "try again": "please try again",
    },
)
