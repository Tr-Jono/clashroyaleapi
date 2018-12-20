from dataclasses import dataclass, field
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class Achievement(CRObject):
    name: str
    stars: int = field(compare=False)
    value: int = field(compare=False)
    target: int = field(compare=False)
    info: str = field(compare=False)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["Achievement"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(**data)
