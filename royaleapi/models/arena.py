from dataclasses import dataclass, field

from royaleapi.models.base import CRObject


@dataclass
class Arena(CRObject):
    name: str = field(compare=False)
    arena: str = field(compare=False)
    arena_id: int
    trophy_limit: int = field(compare=False)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(Arena, cls).de_json(data)
        return cls(**data)
