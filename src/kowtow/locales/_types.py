from dataclasses import dataclass
from typing import Literal

RitualIntensity = Literal["light", "medium", "heavy"]
RITUAL_INTENSITIES: tuple[RitualIntensity, ...] = ("light", "medium", "heavy")


@dataclass(frozen=True)
class LocalePack:
    code: str
    name: str
    opening_line: str
    closing_line: str
    light_opening_line: str
    petition_opening_line: str
    petition_closing_line: str
    offering_topic_prefix: str
    harsh_patterns: dict[str, str]

    def frame(self, body: str, intensity: RitualIntensity) -> str:
        if intensity == "light":
            opening, closing = self.light_opening_line, ""
        elif intensity == "medium":
            opening, closing = self.petition_opening_line, self.petition_closing_line
        elif intensity == "heavy":
            opening, closing = self.opening_line, self.closing_line
        else:
            raise ValueError("Intensity must be light, medium, or heavy.")
        return "\n".join(part for part in (opening, body, closing) if part)
