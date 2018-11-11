from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from royaleapi.models.base import CRObject
from royaleapi.models.arena import Arena

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


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
    client: Optional["RoyaleAPIClient"] = field(default=None, compare=False)

    def __post_init__(self):
        self.arena = Arena.de_json(self.arena, self.client)

    def get_player(self, use_cache=True):
        return self.client.get_player(self.tag, use_cache=use_cache)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None
        data = super().de_json(data, client)
        if "exp_level" in data:
            data["level"] = data.pop("exp_level")
        return cls(client=client, **data)
