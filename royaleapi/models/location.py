from dataclasses import dataclass, field
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class Location(CRObject):
    name: str
    is_country: bool = field(compare=False)
    code: Optional[str] = None  # This is required and name will not be compared after Oceania bug is fixed

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["Location"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(**data)
