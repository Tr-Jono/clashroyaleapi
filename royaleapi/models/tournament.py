from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Optional, TYPE_CHECKING

from royaleapi.models.base import CRObject
from royaleapi.models.tournament_player import TournamentPlayer

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class Tournament(CRObject):
    tag: str
    name: str = field(compare=False)
    open: bool = field(compare=False)
    max_players: int = field(compare=False)
    player_count: int = field(compare=False)
    status: str = field(compare=False)
    create_time: int = field(compare=False)
    prep_time: int = field(compare=False)
    start_time: Optional[int] = field(compare=False)
    end_time: Optional[int] = field(compare=False)
    duration: int = field(compare=False)
    description: str = field(compare=False)
    updated_at: int = field(compare=False)
    creator: TournamentPlayer = field(compare=False)
    players: List[TournamentPlayer] = field(compare=False)

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.creator = TournamentPlayer.de_json(self.creator, self.client)
        self.players = TournamentPlayer.de_list(self.players, self.client)

    def create_datetime(self) -> datetime:
        return datetime.utcfromtimestamp(self.create_time).replace(tzinfo=timezone.utc)

    def start_datetime(self) -> datetime:
        if not self.start_time:
            raise ValueError("Tournament has not started")
        return datetime.utcfromtimestamp(self.start_time).replace(tzinfo=timezone.utc)

    def end_datetime(self) -> datetime:
        if not self.end_time:
            raise ValueError("Tournament has not ended")
        return datetime.utcfromtimestamp(self.end_time).replace(tzinfo=timezone.utc)

    def updated_at_datetime(self) -> datetime:
        return datetime.utcfromtimestamp(self.updated_at).replace(tzinfo=timezone.utc)

    def duration_in_hours(self) -> int:
        return self.duration // 3600

    @classmethod
    def de_json(cls, data: Dict, client: "RoyaleAPIClient") -> Optional["Tournament"]:
        if not data:
            return None
        data = super().de_json(data, client)
        if "current_players" in data:
            data["player_count"] = data.pop("current_players")
        if "members" in data:
            data["players"] = data.pop("members")
        return cls(client=client, **data)
