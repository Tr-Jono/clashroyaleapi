from dataclasses import dataclass, field
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class Arena(CRObject):
    name: str
    arena: str = field(default=None, compare=False)
    arena_id: str = field(default=None, compare=False)
    trophy_limit: int = field(default=None, compare=False)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["Arena"]:
        if not data or data["name"] == "unknown":
            return None
        if "id" in data:
            data["arena_id"] = data.pop("id")
        data = super(Arena, cls).de_json(data, client)
        return cls(**data)
