from crapi.base import CRObject
from crapi.player_league_season import PlayerLeagueSeason


class PlayerLeagueStats(CRObject):
    def __init__(self, current_season, previous_season, best_season):
        self.current_season = PlayerLeagueSeason.de_json(current_season)
        self.previous_season = PlayerLeagueSeason.de_json(previous_season)
        self.best_season = PlayerLeagueSeason.de_json(best_season)

        self._id_attrs = None

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(PlayerLeagueStats, cls).de_json(data)
        return cls(**data)
