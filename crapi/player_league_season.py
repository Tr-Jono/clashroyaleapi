from crapi.base import CRObject


class PlayerLeagueSeason(CRObject):
    def __init__(self, season_id, rank, trophies, best_trophies):
        self.season_id = season_id
        self.rank = rank
        self.trophies = trophies
        self.best_trophies = best_trophies

        self._id_attrs = None

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(PlayerLeagueSeason, cls).de_json(data)
        return cls(**data)
