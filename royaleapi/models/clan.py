from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, TYPE_CHECKING

from royaleapi.constants import ClanRole
from royaleapi.models.base import CRObject
from royaleapi.models.clan_badge import ClanBadge
from royaleapi.models.clan_tracking import ClanTracking
from royaleapi.models.location import Location
from royaleapi.models.popularity import Popularity

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient
    from royaleapi.models.battle import Battle
    from royaleapi.models.clan_war import ClanWar
    from royaleapi.models.player import Player


@dataclass
class Clan(CRObject):
    # All endpoints except history
    tag: Optional[str] = None
    name: Optional[str] = field(default=None, compare=False)

    # Most endpoints have this
    badge: Optional[ClanBadge] = field(default=None, compare=False)

    # Tournament endpoint only
    badge_id: Optional[int] = field(default=None, compare=False)

    # Clan and search and popularity endpoint only
    description: Optional[str] = field(default=None, compare=False)
    clan_type: Optional[str] = field(default=None, compare=False)
    score: Optional[int] = field(default=None, compare=False)  # Also in clan leaderboard & history endpoint
    war_trophies: Optional[int] = field(default=None, compare=False)  # Also in clan war endpoint
    member_count: Optional[int] = field(default=None, compare=False)  # Also in clan leaderboard & history endpoint
    required_score: Optional[int] = field(default=None, compare=False)
    total_donations: Optional[int] = field(default=None, compare=False)
    location: Optional[Location] = field(default=None, compare=False)  # Also in clan leaderboard endpoint
    # Not returned in "clan/search" endpoint
    members: Optional[List["Player"]] = field(default_factory=list, compare=False)  # Also in history endpoint
    tracking: Optional[ClanTracking] = field(default=None, compare=False)
    leader: Optional["Player"] = field(default=None, compare=False)
    co_leaders: Optional[List["Player"]] = field(default_factory=list, compare=False)
    elders: Optional[List["Player"]] = field(default_factory=list, compare=False)

    # Player endpoint only
    role: Optional[str] = field(default=None, compare=False)
    player_donations: Optional[int] = field(default=None, compare=False)
    donations_received: Optional[int] = field(default=None, compare=False)
    donations_delta: Optional[int] = field(default=None, compare=False)

    # Clan war endpoint only
    participants: Optional[int] = field(default=None, compare=False)
    battles_played: Optional[int] = field(default=None, compare=False)
    wins: Optional[int] = field(default=None, compare=False)
    crowns: Optional[int] = field(default=None, compare=False)  # War day only

    # Clan war log endpoint only
    war_trophies_change: Optional[int] = field(default=None, compare=False)

    # Clan leaderboard endpoint only
    rank: Optional[int] = field(default=None, compare=False)
    previous_rank: Optional[int] = field(default=None, compare=False)

    # Popularity endpoint only
    popularity: Optional[Popularity] = field(default=None, compare=False)

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        from royaleapi.models.player import Player  # I did not want to do this
        self.badge = ClanBadge.de_json(self.badge, self.client)
        self.location = Location.de_json(self.location, self.client)
        self.members = Player.de_list(self.members, self.client)
        self.tracking = ClanTracking.de_json(self.tracking, self.client)
        self.popularity = Popularity.de_json(self.popularity, self.client)
        if self.members:
            self.leader = [p for p in self.members if p.role == ClanRole.LEADER][0]
            self.co_leaders = [p for p in self.members if p.role == ClanRole.CO_LEADER]
            self.elders = [p for p in self.members if p.role == ClanRole.ELDER]

    def get_clan(self, *args, **kwargs) -> "Clan":
        return self.client.get_clan(self.tag, *args, **kwargs)

    def get_battles(self, *args, **kwargs) -> List["Battle"]:
        return self.client.get_clan_battles(self.tag, *args, **kwargs)

    def get_war(self, *args, **kwargs) -> "ClanWar":
        return self.client.get_clan_war(self.tag, *args, **kwargs)

    def get_war_log(self, *args, **kwargs) -> List["ClanWar"]:
        return self.client.get_clan_war_log(self.tag, *args, **kwargs)

    def get_history(self, *args, **kwargs) -> Dict[str, "Clan"]:
        return self.client.get_clan_history(self.tag, *args, **kwargs)

    def get_tracking(self, *args, **kwargs) -> ClanTracking:
        return self.client.get_clan_tracking(self.tag, *args, **kwargs)

    def track(self, *args, **kwargs) -> bool:
        return self.client.track_clan(self.tag, *args, **kwargs)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["Clan"]:
        if not data:
            return None
        data = super().de_json(data, client)
        if "type" in data:
            data["clan_type"] = data.pop("type")
        if "donations" in data:
            if "role" in data:  # Clan object is from "player" endpoint
                data["player_donations"] = data.pop("donations")
            else:  # Clan object is from "clan" endpoint
                data["total_donations"] = data.pop("donations")
        return cls(client=client, **data)
