from dataclasses import dataclass, field
from typing import List, Optional

from royaleapi.models.achievement import Achievement
from royaleapi.models.arena import Arena
from royaleapi.models.base import CRObject
from royaleapi.models.card import Card
from royaleapi.models.clan import Clan
from royaleapi.models.player_games import PlayerGames
from royaleapi.models.player_league_stats import PlayerLeagueStats
from royaleapi.models.player_stats import PlayerStats


@dataclass
class Player(CRObject):
    tag: str
    name: str = field(compare=False)
    trophies: int = field(compare=False)
    arena: Arena = field(compare=False)
    stats: PlayerStats = field(compare=False)
    games: PlayerGames = field(compare=False)
    deck_link: str = field(compare=False)
    current_deck: List[Card] = field(compare=False)
    cards: List[Card] = field(compare=False)
    achievements: List[Achievement] = field(compare=False)
    clan: Optional[Clan] = field(default=None, compare=False)
    rank: Optional[int] = field(default=None, compare=False)
    league_stats: Optional[PlayerLeagueStats] = field(default=None, compare=False)

    def __post_init__(self):
        self.arena = Arena.de_json(self.arena)
        self.clan = Clan.de_json(self.clan)
        self.stats = PlayerStats.de_json(self.stats)
        self.games = PlayerGames.de_json(self.games)
        self.league_stats = PlayerLeagueStats.de_json(self.league_stats)
        self.current_deck = Card.de_list(self.current_deck)
        self.cards = Card.de_list(self.cards)
        self.achievements = Achievement.de_list(self.achievements)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        if "league_statistics" in data:
            data["league_stats"] = data.pop("league_statistics")
        return cls(**data)
