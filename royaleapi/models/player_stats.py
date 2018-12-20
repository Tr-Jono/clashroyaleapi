from dataclasses import dataclass, field
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject
from royaleapi.models.card import Card

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass(eq=False)
class PlayerStats(CRObject):
    clan_cards_collected: int
    tournament_cards_won: int
    max_trophies: int
    three_crown_wins: int
    cards_found: int
    favorite_card: Card
    total_donations: int
    challenge_max_wins: int
    challenge_cards_won: int
    level: int
    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False, compare=False)

    def __post_init__(self):
        self.favorite_card = Card.de_json(self.favorite_card, self.client)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["PlayerStats"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(client=client, **data)
