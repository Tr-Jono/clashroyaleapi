from dataclasses import dataclass, field
from typing import Dict, Optional, Any, TYPE_CHECKING

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
    level: Optional[int] = field(default=None, compare=False)  # 1 - 5/8/11/13 (old)
    display_level: Optional[int] = field(default=None, compare=False)  # 1/3/6/9 - 13 (new)
    star_level: Optional[int] = field(default=None, compare=False)  # None if star_level is 0
    min_level: Optional[int] = field(default=None, compare=False)  # 1/3/6/9 (old), also in deck popularity endpoint
    max_level: Optional[int] = field(default=None, compare=False)  # 5/8/11/13 (new), also in deck popularity endpoint
    count: Optional[int] = field(default=None, compare=False)
    required_for_upgrade: Optional[int or str] = field(default=None, compare=False)  # int or "Maxed"
    left_to_upgrade: Optional[int] = field(default=None, compare=False)
    icon: Optional[str] = field(default=None, compare=False)  # Also in deck popularity endpoint

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["Card"]:
        if not data:
            return None
        data = super().de_json(data, client)
        if "type" in data:
            data["card_type"] = data.pop("type")
        if "id" in data:
            data["card_id"] = data.pop("id")
        return cls(**data)
