from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class Location(CRObject):
    name: str = field(compare=False)
    is_country: bool = field(compare=False)
    code: str

    @classmethod
    def de_json(cls, data: Dict, client: "RoyaleAPIClient") -> Optional["Location"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(**data)
