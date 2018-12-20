from dataclasses import dataclass, field
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class ClanBadge(CRObject):
    name: str = field(compare=False)
    category: str = field(compare=False)
    badge_id: int
    image: str = field(compare=False)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["ClanBadge"]:
        if not data:
            return None
        data = super().de_json(data, client)
        if "id" in data:
            data["badge_id"] = data.pop("id")
        return cls(**data)
