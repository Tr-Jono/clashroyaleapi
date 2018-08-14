from dataclasses import dataclass, field

from royaleapi.models.base import CRObject


@dataclass
class Achievement(CRObject):
    name: str
    stars: int = field(compare=False)
    value: int = field(compare=False)
    target: int = field(compare=False)
    info: str = field(compare=False)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        return cls(**data)
