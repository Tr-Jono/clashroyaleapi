# GAMES NOT FINISHED, PLAYER.__INIT__ NOT DONE
# CHECK IF ALL STUFF IN __INIT__.PY

from crapi.achievement import Achievement
from crapi.arena import Arena
from crapi.card import Card
from crapi.clan import Clan
from crapi.base import CRObject
from crapi.player_stats import PlayerStats
from crapi.player_games import PlayerGames
from crapi.player_league_stats import PlayerLeagueStats


class Player(CRObject):
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
        self.tag = tag
        self.name = name
        self.trophies = trophies
        self.rank = rank
        self.arena = Arena.de_json(arena)
        self.clan = Clan.de_json(clan)
        self.stats = PlayerStats.de_json(stats)
        self.games = PlayerGames.de_json(games)
        self.league_statistics = PlayerLeagueStats.de_json(league_statistics)
        self.deck_link = deck_link
        self.current_deck = Card.de_list(current_deck)
        self.cards = Card.de_list(cards)
        self.achievements = Achievement.de_list(achievements)

        self._id_attrs = None
        if self.tag:
            self._id_attrs = (self.tag,)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(Player, cls).de_json(data)
        if all(v is None for v in data.values()):
            return None
        return cls(**data)

    @classmethod
    def de_list(cls, data):
        if not data:
            return []
        return [cls.de_json(player) for player in data]
