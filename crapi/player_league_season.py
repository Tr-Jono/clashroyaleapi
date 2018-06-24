from crapi.base import CRObject


class PlayerLeagueSeason(CRObject):
    def __init__(self, trophies, best_trophies=None, season_id=None, rank=None):
        self.trophies = trophies
        self.best_trophies = best_trophies
        self.season_id = season_id
        self.rank = rank

        self._id_attrs = None

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(PlayerLeagueSeason, cls).de_json(data)
        if data.get("id"):
            data["season_id"] = data.pop("id")
        return cls(**data)
