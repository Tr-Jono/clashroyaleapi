from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Optional, TYPE_CHECKING

from royaleapi.constants import ClanWarState
from royaleapi.models.base import CRObject
from royaleapi.models.clan import Clan
from royaleapi.models.clan_war_participant import ClanWarParticipant

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass(eq=False)
class ClanWar(CRObject):
    state: str

    # In war only
    clan: Optional[Clan] = None
    participants: Optional[List[ClanWarParticipant]] = field(default_factory=list)

    # Collection day only
    collection_end_time: Optional[int] = None

    # Matchmaking / war day only
    war_end_time: Optional[int] = None
    standings: Optional[List[Clan]] = field(default_factory=list)

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.clan = Clan.de_json(self.clan, self.client)
        self.participants = ClanWarParticipant.de_list(self.participants, self.client)
        self.standings = Clan.de_list(self.standings, self.client)

    def end_datetime(self) -> datetime:
        if self.state == ClanWarState.NOT_IN_WAR:
            raise ValueError("No ongoing war")
        return datetime.utcfromtimestamp(self.collection_end_time or self.war_end_time).replace(tzinfo=timezone.utc)

    @classmethod
    def de_json(cls, data: Dict, client: "RoyaleAPIClient") -> Optional["ClanWar"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(client=client, **data)
