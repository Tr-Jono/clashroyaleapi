from dataclasses import dataclass, field
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject
from royaleapi.models.player_league_season import PlayerLeagueSeason

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass(eq=False)
class PlayerLeagueStats(CRObject):
    current_season: PlayerLeagueSeason
    previous_season: Optional[PlayerLeagueSeason] = None
    best_season: Optional[PlayerLeagueSeason] = None

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self.current_season = PlayerLeagueSeason.de_json(self.current_season, self.client)
        self.previous_season = PlayerLeagueSeason.de_json(self.previous_season, self.client)
        self.best_season = PlayerLeagueSeason.de_json(self.best_season, self.client)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["PlayerLeagueStats"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(client=client, **data)
