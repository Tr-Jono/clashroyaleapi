from dataclasses import dataclass, field
from typing import List, Optional

from royaleapi.models.base import CRObject
from royaleapi.models.clan_badge import ClanBadge
from royaleapi.models.clan_member import ClanMember
from royaleapi.models.location import Location
from royaleapi.models.clan_tracking import ClanTracking


@dataclass
class Clan(CRObject):
    tag: str
    name: str = field(compare=False)
    badge: ClanBadge = field(compare=False)

    # Only for clans returned from "clan" endpoint
    description: Optional[str] = field(default=None, compare=False)
    clan_type: Optional[str] = field(default=None, compare=False)
    score: Optional[int] = field(default=None, compare=False)
    member_count: Optional[int] = field(default=None, compare=False)
    required_score: Optional[int] = field(default=None, compare=False)
    total_donations: Optional[int] = field(default=None, compare=False)
    location: Optional[Location] = field(default=None, compare=False)
    members: List[ClanMember] = field(default_factory=list, compare=False)
    tracking: Optional[ClanTracking] = field(default=None, compare=False)

    # Only for clans returned from "player" endpoint
    role: Optional[str] = field(default=None, compare=False)
    player_donations: Optional[int] = field(default=None, compare=False)
    donations_received: Optional[int] = field(default=None, compare=False)
    donations_delta: Optional[int] = field(default=None, compare=False)

    def __post_init__(self):
        self.badge = ClanBadge.de_json(self.badge)
        self.location = Location.de_json(self.location)
        self.members = ClanMember.de_list(self.members)
        self.tracking = ClanTracking.de_json(self.tracking)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        if "type" in data:
            data["clan_type"] = data.pop("type")
        if "donations" in data:
            if "role" in data:  # Clan object is from "player" endpoint
                data["player_donations"] = data.pop("donations")
            else:  # Clan object is from "clan" endpoint
                data["total_donations"] = data.pop("donations")
        return cls(**data)
