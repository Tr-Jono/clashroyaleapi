from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.achievement import Achievement
from royaleapi.models.arena import Arena
from royaleapi.models.base import CRObject
from royaleapi.models.card import Card
from royaleapi.models.chest_cycle import ChestCycle
from royaleapi.models.clan import Clan
from royaleapi.models.player_games import PlayerGames
from royaleapi.models.player_league_stats import PlayerLeagueStats
from royaleapi.models.player_stats import PlayerStats

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient
    from royaleapi.models.battle import Battle


@dataclass
class Player(CRObject):
    tag: str
    name: str = field(compare=False)

    # Player endpoint only
    deck_link: str = field(default=None, compare=False)  # Also in player battles endpoint
    deck: List[Card] = field(default=None, compare=False)  # Also in player battles endpoint
    trophies: int = field(default=None, compare=False)  # Also in player leaderboard endpoint
    arena: Arena = field(default=None, compare=False)  # Also in player leaderboard endpoint
    rank: Optional[int] = field(default=None, compare=False)  # Also in player leaderboard endpoint
    clan: Optional[Clan] = field(default=None, compare=False)  # Also in player leaderboard endpoint
    stats: PlayerStats = field(default=None, compare=False)
    games: PlayerGames = field(default=None, compare=False)
    league_stats: Optional[PlayerLeagueStats] = field(default=None, compare=False)
    cards: List[Card] = field(default=None, compare=False)
    achievements: List[Achievement] = field(default=None, compare=False)

    # Battle participants only
    crowns_earned: Optional[int] = field(default=None, compare=False)
    start_trophies: Optional[int] = field(default=None, compare=False)
    trophy_change: Optional[int] = field(default=None, compare=False)

    # Player leaderboard endpoint only
    previous_rank: Optional[int] = field(default=None, compare=False)
    level: Optional[int] = field(default=None, compare=False)
    donations_delta: None = field(default=None, compare=False)  # Why is this here??? Always None

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.deck = Card.de_list(self.deck, self.client)
        self.arena = Arena.de_json(self.arena, self.client)
        self.clan = Clan.de_json(self.clan, self.client)
        self.stats = PlayerStats.de_json(self.stats, self.client)
        self.games = PlayerGames.de_json(self.games, self.client)
        self.league_stats = PlayerLeagueStats.de_json(self.league_stats, self.client)
        self.cards = Card.de_list(self.cards, self.client)
        self.achievements = Achievement.de_list(self.achievements, self.client)

    def get_player(self, use_cache: bool = True) -> "Player":
        return self.client.get_player(self.tag, use_cache=use_cache)

    def get_clan(self, use_cache: bool = True) -> Optional[Clan]:
        return self.clan.get_clan(use_cache=use_cache) if self.clan else None

    def get_chests(self, use_cache: bool = True) -> ChestCycle:
        return self.client.get_player_chests(self.tag, use_cache=use_cache)

    def get_battles(self, use_cache: bool = True) -> List["Battle"]:
        return self.client.get_player_battles(self.tag, use_cache=use_cache)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["Player"]:
        if not data:
            return None
        data = super().de_json(data, client)
        if "league_statistics" in data:
            data["league_stats"] = data.pop("league_statistics")
        if "current_deck" in data:
            data["deck"] = data.pop("current_deck")
        if "exp_level" in data:
            data["level"] = data.pop("exp_level")
        return cls(client=client, **data)
