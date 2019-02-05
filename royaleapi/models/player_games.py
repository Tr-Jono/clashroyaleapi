from dataclasses import dataclass, field
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass(eq=False)
class PlayerGames(CRObject):
    total: int
    tournament_games: int
    wins: int
    war_day_wins: int
    wins_percent: float
    losses: int
    losses_percent: float
    draws: int
    draws_percent: float

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["PlayerGames"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(**data)
