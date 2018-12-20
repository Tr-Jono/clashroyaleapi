from dataclasses import dataclass
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass(eq=False)
class PlayerLeagueSeason(CRObject):
    trophies: int
    rank: Optional[int] = None

    # current_season and previous_season only
    best_trophies: Optional[int] = None

    # previous_season and best_season only
    season_id: Optional[str] = None

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["PlayerLeagueSeason"]:
        if not data:
            return None
        data = super().de_json(data, client)
        if "id" in data:
            data["season_id"] = data.pop("id")
        return cls(**data)
