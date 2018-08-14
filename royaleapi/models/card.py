from dataclasses import dataclass, field
from typing import Union, Optional

from royaleapi.models.base import CRObject


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

    # only returned from player objects
    level: Optional[int] = field(default=None, compare=False)
    max_level: Optional[int] = field(default=None, compare=False)
    count: Optional[int] = field(default=None, compare=False)
    required_for_upgrade: Optional[Union[int, str]] = field(default=None, compare=False)  # str can only be "Maxed"
    left_to_upgrade: Optional[int] = field(default=None, compare=False)
    icon: Optional[str] = field(default=None, compare=False)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(Card, cls).de_json(data)
        if "type" in data:
            data["card_type"] = data.pop("type")
        if "id" in data:
            data["card_id"] = data.pop("id")
        return cls(**data)
