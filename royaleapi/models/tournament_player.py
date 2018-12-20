from dataclasses import dataclass, field
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject
from royaleapi.models.clan import Clan
from royaleapi.models.player import Player

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class TournamentPlayer(CRObject):
    tag: str
    clan: Clan = field(compare=False)
    name: str = field(compare=False)
    rank: int = field(compare=False)
    score: int = field(compare=False)
    creator: Optional[bool] = field(default=None, compare=False)

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.clan = Clan.de_json(self.clan, self.client)

    def get_player(self, use_cache: bool = True) -> Player:
        return self.client.get_player(self.tag, use_cache=use_cache)

    def get_clan(self, use_cache: bool = True) -> Clan:
        return self.clan.get_clan(use_cache=use_cache) if self.clan else None

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["TournamentPlayer"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(client=client, **data)
