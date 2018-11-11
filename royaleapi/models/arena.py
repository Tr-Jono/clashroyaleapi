from dataclasses import dataclass, field

from royaleapi.models.base import CRObject


@dataclass
class Arena(CRObject):
    name: str
    arena: str = field(default=None, compare=False)
    arena_id: str = field(default=None, compare=False)
    trophy_limit: int = field(default=None, compare=False)

    @classmethod
    def de_json(cls, data, client):
        if not data or data["name"] == "unknown":
            return None
        data = super(Arena, cls).de_json(data, client)
        return cls(**data)
