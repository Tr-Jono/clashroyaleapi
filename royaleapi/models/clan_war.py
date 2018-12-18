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
    # Clan war endpoint only
    state: Optional[str] = None

    # Collection day / Matchmaking / War day only
    clan: Optional[Clan] = None

    # Collection day / Matchmaking / War day / War log only
    participants: Optional[List[ClanWarParticipant]] = field(default_factory=list)

    # Collection day only
    collection_end_time: Optional[int] = None

    # Matchmaking / War day only
    war_end_time: Optional[int] = None

    # Matchmaking / War day / War log only
    standings: Optional[List[Clan]] = field(default_factory=list)

    # War log only
    created_date: Optional[int] = None
    season_number: Optional[int] = None

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self.clan = Clan.de_json(self.clan, self.client)
        self.participants = ClanWarParticipant.de_list(self.participants, self.client)
        self.standings = Clan.de_list(self.standings, self.client)

    def end_datetime(self) -> datetime:
        if self.state == ClanWarState.NOT_IN_WAR:
            raise ValueError("No ongoing war")
        return datetime.utcfromtimestamp(self.collection_end_time or self.war_end_time).replace(tzinfo=timezone.utc)

    def created_datetime(self) -> datetime:
        if not self.created_date:
            raise ValueError("War is not in war log")
        return datetime.utcfromtimestamp(self.created_date).replace(tzinfo=timezone.utc)

    @classmethod
    def de_json(cls, data: Dict, client: "RoyaleAPIClient") -> Optional["ClanWar"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(client=client, **data)
