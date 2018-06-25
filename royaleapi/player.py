from royaleapi.achievement import Achievement
from royaleapi.card import Card
from royaleapi.clan import Clan
from royaleapi.person import Person
from royaleapi.player_stats import PlayerStats
from royaleapi.player_games import PlayerGames
from royaleapi.player_league_stats import PlayerLeagueStats


class Player(Person):
    def __init__(self,
                 tag=None,
                 name=None,
                 trophies=None,
                 rank=None,
                 arena=None,
                 clan=None,
                 stats=None,
                 games=None,
                 league_statistics=None,
                 deck_link=None,
                 current_deck=None,
                 cards=None,
                 achievements=None):
        super().__init__(tag, name, trophies, arena)
        self.rank = rank
        self.clan = Clan.de_json(clan)
        self.stats = PlayerStats.de_json(stats)
        self.games = PlayerGames.de_json(games)
        self.league_statistics = PlayerLeagueStats.de_json(league_statistics)
        self.deck_link = deck_link
        self.current_deck = Card.de_list(current_deck)
        self.cards = Card.de_list(cards)
        self.achievements = Achievement.de_list(achievements)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        return cls(**data)
