from dataclasses import dataclass

from royaleapi.models.base import CRObject
from royaleapi.models.card import Card


@dataclass
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

    def __post_init__(self):
        self.favorite_card = Card.de_json(self.favorite_card)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        return cls(**data)
