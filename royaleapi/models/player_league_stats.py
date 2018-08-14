from dataclasses import dataclass
from typing import Optional

from royaleapi.models.base import CRObject
from royaleapi.models.player_league_season import PlayerLeagueSeason


@dataclass(eq=False)
class PlayerLeagueStats(CRObject):
    current_season: PlayerLeagueSeason
    previous_season: Optional[PlayerLeagueSeason]
    best_season: Optional[PlayerLeagueSeason]

    def __post_init__(self):
        self.current_season = PlayerLeagueSeason.de_json(self.current_season)
        self.previous_season = PlayerLeagueSeason.de_json(self.previous_season)
        self.best_season = PlayerLeagueSeason.de_json(self.best_season)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        return cls(**data)
