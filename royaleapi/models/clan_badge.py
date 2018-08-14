from dataclasses import dataclass, field

from royaleapi.models.base import CRObject


@dataclass
class ClanBadge(CRObject):
    name: str = field(compare=False)
    category: str = field(compare=False)
    badge_id: int
    image: str = field(compare=False)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        if "id" in data:
            data["badge_id"] = data.pop("id")
        return cls(**data)
