from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING

from royaleapi.models.arena import Arena
from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient
    from royaleapi.models.player import Player


@dataclass
class ClanMember(CRObject):
    tag: str
    name: str = field(compare=False)
    trophies: int = field(compare=False)
    level: int = field(compare=False)
    arena: Arena = field(compare=False)
    role: str = field(compare=False)
    donations: int = field(compare=False)
    donations_received: int = field(compare=False)
    donations_delta: int = field(compare=False)
    donations_percent: float = field(compare=False)
    rank: int = field(compare=False)
    previous_rank: int = field(default=None, compare=False)

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.arena = Arena.de_json(self.arena, self.client)

    def get_player(self, use_cache: bool = True) -> "Player":
        return self.client.get_player(self.tag, use_cache=use_cache)

    @classmethod
    def de_json(cls, data: Dict, client: "RoyaleAPIClient") -> Optional["ClanMember"]:
        if not data:
            return None
        data = super().de_json(data, client)
        if "exp_level" in data:
            data["level"] = data.pop("exp_level")
        return cls(client=client, **data)
