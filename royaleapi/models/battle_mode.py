from dataclasses import dataclass, field
from typing import Optional, Dict, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class BattleMode(CRObject):
    name: str
    mode_id: Optional[int] = None
    deck: Optional[str] = None
    card_levels: Optional[int] = field(default=None, compare=False)
    overtime_seconds: Optional[int] = field(default=None, compare=False)
    players: Optional[str] = field(default=None, compare=False)
    same_deck: Optional[bool] = field(default=None, compare=False)

    @classmethod
    def de_json(cls, data: Dict, client: "RoyaleAPIClient") -> Optional["BattleMode"]:
        if not data:
            return None
        if "id" in data:
            data["mode_id"] = data.pop("id")
        data = super().de_json(data, client)
        return cls(**data)
