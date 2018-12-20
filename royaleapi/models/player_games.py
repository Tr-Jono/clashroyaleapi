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
    wins_percent: float = field(init=False)
    losses: int
    losses_percent: float = field(init=False)
    draws: int
    draws_percent: float = field(init=False)

    def __post_init__(self) -> None:
        self.wins_percent = round(100 * (self.wins / self.total), 2)
        self.losses_percent = round(100 * (self.losses / self.total), 2)
        self.draws_percent = round(100 * (self.draws / self.total), 2)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["PlayerGames"]:
        if not data:
            return None
        data = super().de_json(data, client)
        for key in "wins_percent", "losses_percent", "draws_percent":
            if key in data:
                del data[key]
        return cls(**data)
