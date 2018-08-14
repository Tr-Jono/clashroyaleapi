from dataclasses import dataclass, field

from royaleapi.models.base import CRObject
from royaleapi.models.arena import Arena


@dataclass
class ClanMember(CRObject):
    tag: str
    name: str = field(compare=False)
    trophies: int = field(compare=False)
    arena: Arena = field(compare=False)
    rank: int = field(compare=False)
    role: str = field(compare=False)
    level: int = field(compare=False)
    donations: int = field(compare=False)
    donations_received: int = field(compare=False)
    donations_delta: int = field(compare=False)
    donations_percent: float = field(compare=False)
    previous_rank: int = field(default=None, compare=False)

    def __post_init__(self):
        self.arena = Arena.de_json(self.arena)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        if "exp_level" in data:
            data["level"] = data.pop("exp_level")
        return cls(**data)
