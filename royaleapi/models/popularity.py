from dataclasses import dataclass
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass(eq=False)
class Popularity(CRObject):
    hits: int
    hits_per_day_avg: float

    def __post_init__(self):
        self.hits_per_day_avg = float(self.hits_per_day_avg)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["Popularity"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(**data)
