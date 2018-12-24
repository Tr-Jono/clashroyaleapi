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
    deck_link: Optional[str] = field(default=None, compare=False)  # Also in player battles endpoint
    deck: Optional[List[Card]] = field(default=None, compare=False)  # Also in player battles endpoint
    trophies: Optional[int] = field(default=None, compare=False)  # Also in clan and player leaderboard endpoint
    arena: Optional[Arena] = field(default=None, compare=False)  # Also in clan and player leaderboard endpoint
    rank: Optional[int] = field(default=None, compare=False)  # Also in clan, player leaderboard and tournament endpoint
    clan: Optional[Clan] = field(default=None, compare=False)  # Also in player leaderboard and tournament endpoint
    stats: Optional[PlayerStats] = field(default=None, compare=False)
    games: Optional[PlayerGames] = field(default=None, compare=False)
    league_stats: Optional[PlayerLeagueStats] = field(default=None, compare=False)
    cards: Optional[List[Card]] = field(default=None, compare=False)
    achievements: Optional[List[Achievement]] = field(default=None, compare=False)

    # Clan endpoint only
    level: Optional[int] = field(default=None, compare=False)  # Also in player leaderboard endpoint
    role: Optional[str] = field(default=None, compare=False)
    donations: Optional[int] = field(default=None, compare=False)
    donations_received: Optional[int] = field(default=None, compare=False)
    donations_delta: Optional[int] = field(default=None, compare=False)  # Also in player leaderboard endpoint (somehow)
    donations_percent: Optional[float] = field(default=None, compare=False)
    previous_rank: Optional[int] = field(default=None, compare=False)  # Also in player leaderboard endpoint

    # Battle participants only
    crowns_earned: Optional[int] = field(default=None, compare=False)
    start_trophies: Optional[int] = field(default=None, compare=False)
    trophy_change: Optional[int] = field(default=None, compare=False)

    # Clan war endpoint only
    cards_earned: Optional[int] = field(default=None, compare=False)
    battles_played: Optional[int] = field(default=None, compare=False)
    wins: Optional[int] = field(default=None, compare=False)
    collection_day_battles_played: Optional[int] = field(default=None, compare=False)

    # Tournament endpoint only
    score: Optional[int] = field(default=None, compare=False)
    is_creator: Optional[bool] = field(default=None, compare=False)

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

    def get_player(self, *args, **kwargs) -> "Player":
        return self.client.get_player(self.tag, *args, **kwargs)

    def get_chests(self, *args, **kwargs) -> ChestCycle:
        return self.client.get_player_chests(self.tag, *args, **kwargs)

    def get_battles(self, *args, **kwargs) -> List["Battle"]:
        return self.client.get_player_battles(self.tag, *args, **kwargs)

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
        if "creator" in data:
            data["is_creator"] = data.pop("creator")
        return cls(client=client, **data)
