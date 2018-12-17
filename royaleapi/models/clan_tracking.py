from dataclasses import dataclass
from typing import Dict, Optional, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass(eq=False)
class ClanTracking(CRObject):
    active: bool
    available: bool
    snapshot_count: int

    # If clan is tracked
    legible: Optional[bool] = None

    # Only returned in "tracking" endpoint
    tag: Optional[str] = None

    @classmethod
    def de_json(cls, data: Dict, client: "RoyaleAPIClient") -> Optional["ClanTracking"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(**data)
