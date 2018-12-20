from dataclasses import dataclass, field
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject
from royaleapi.models.player import Player

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class ClanWarParticipant(CRObject):
    tag: str
    name: str = field(compare=False)
    cards_earned: int = field(compare=False)
    battles_played: int = field(compare=False)
    wins: int = field(compare=False)
    collection_day_battles_played: int = field(compare=False)

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False, compare=False)

    def get_player(self, use_cache: bool = True) -> Player:
        return self.client.get_player(self.tag, use_cache=use_cache)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["ClanWarParticipant"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(client=client, **data)
