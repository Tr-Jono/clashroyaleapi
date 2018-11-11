from dataclasses import dataclass, field

from royaleapi.models.base import CRObject


@dataclass
class Location(CRObject):
    name: str = field(compare=False)
    is_country: bool = field(compare=False)
    code: str

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(**data)
