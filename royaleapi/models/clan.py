from dataclasses import dataclass, field
from typing import List, Dict, Optional, TYPE_CHECKING

from royaleapi.models.base import CRObject
from royaleapi.models.clan_badge import ClanBadge
from royaleapi.models.clan_member import ClanMember
from royaleapi.models.clan_tracking import ClanTracking
from royaleapi.models.location import Location

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class Clan(CRObject):
    tag: str
    name: str = field(compare=False)
    badge: ClanBadge = field(compare=False)

    # Only returned from "clan" endpoint
    description: Optional[str] = field(default=None, compare=False)
    clan_type: Optional[str] = field(default=None, compare=False)
    score: Optional[int] = field(default=None, compare=False)
    member_count: Optional[int] = field(default=None, compare=False)
    required_score: Optional[int] = field(default=None, compare=False)
    total_donations: Optional[int] = field(default=None, compare=False)
    location: Optional[Location] = field(default=None, compare=False)
    # Not returned in "clan/search" endpoint
    members: List[ClanMember] = field(default_factory=list, compare=False)
    tracking: Optional[ClanTracking] = field(default=None, compare=False)

    # Only present in Player objects
    role: Optional[str] = field(default=None, compare=False)
    player_donations: Optional[int] = field(default=None, compare=False)
    donations_received: Optional[int] = field(default=None, compare=False)
    donations_delta: Optional[int] = field(default=None, compare=False)

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.badge = ClanBadge.de_json(self.badge, self.client)
        self.location = Location.de_json(self.location, self.client)
        self.members = ClanMember.de_list(self.members, self.client)
        self.tracking = ClanTracking.de_json(self.tracking, self.client)

    def get_full_clan(self, use_cache: bool = True) -> "Clan":
        return self.client.get_clan(self.tag, use_cache=use_cache)

    @classmethod
    def de_json(cls, data: Dict, client: "RoyaleAPIClient") -> Optional["Clan"]:
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
