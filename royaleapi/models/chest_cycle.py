from dataclasses import dataclass
from typing import List, Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass(eq=False)
class ChestCycle(CRObject):
    upcoming: List[str]
    mega_lightning: int
    magical: int
    legendary: int
    epic: int
    giant: int

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["ChestCycle"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(**data)
