from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class Card(CRObject):
    key: str
    name: str = field(compare=False)
    elixir: int = field(compare=False)
    card_type: str = field(compare=False)
    rarity: str = field(compare=False)
    arena: int = field(compare=False)
    description: str = field(compare=False)
    card_id: int = field(compare=False)

    # Players' cards only
    level: Optional[int] = field(default=None, compare=False)
    star_level: Optional[int] = field(default=None, compare=False)  # Not given if star_level is 0
    max_level: Optional[int] = field(default=None, compare=False)
    count: Optional[int] = field(default=None, compare=False)
    required_for_upgrade: Optional[int or str] = field(default=None, compare=False)  # str can only be "Maxed"
    left_to_upgrade: Optional[int] = field(default=None, compare=False)
    icon: Optional[str] = field(default=None, compare=False)

    @classmethod
    def de_json(cls, data: Dict, client: "RoyaleAPIClient") -> Optional["Card"]:
        if not data:
            return None
        data = super().de_json(data, client)
        if "type" in data:
            data["card_type"] = data.pop("type")
        if "id" in data:
            data["card_id"] = data.pop("id")
        return cls(**data)
