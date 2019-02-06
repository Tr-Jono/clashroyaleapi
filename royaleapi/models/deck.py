from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, TYPE_CHECKING

from royaleapi import utils
from royaleapi.models.base import CRObject
from royaleapi.models.card import Card

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass(eq=False)
class Deck(CRObject):
    # This object is specifically for the deck popularity endpoint
    cards: List[Card]
    deck_link: str
    popularity: int  # No idea why this is an integer instead of a Popularity object

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self.cards = Card.de_list(self.cards, self.client)

    def __eq__(self, other):
        # Order of cards does not matter
        if self.__class__ is other.__class__:
            return Counter([i.key for i in self.cards]) == Counter([i.key for i in other.cards])
        return NotImplemented

    def average_elixir(self) -> float:
        return utils.average_elixir(self.cards)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["Deck"]:
        if not data:
            return None
        if "decklink" in data:
            data["deck_link"] = data.pop("decklink")
        data = super().de_json(data, client)
        return cls(**data)
