from royaleapi.base import CRObject


class PlayerGames(CRObject):
    def __init__(self, total, tournament_games, wins, war_day_wins, wins_percent, losses, losses_percent, draws,
                 draws_percent):
        self.total = total
        self.tournament_games = tournament_games
        self.wins = wins
        self.war_day_wins = war_day_wins
        self.wins_percent = wins_percent
        self.losses = losses
        self.losses_percent = losses_percent
        self.draws = draws
        self.draws_percent = draws_percent

        self._id_attrs = None

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(PlayerGames, cls).de_json(data)
        return cls(**data)
