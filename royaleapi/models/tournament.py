from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject
from royaleapi.models.player import Player
from royaleapi.models.popularity import Popularity

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

    # Tournament get and search and popularity endpoints only
    description: Optional[str] = field(default=None, compare=False)
    updated_at: Optional[int] = field(default=None, compare=False)
    creator: Optional[Player] = field(default=None, compare=False)  # Not in tournament search
    players: Optional[List[Player]] = field(default_factory=list, compare=False)  # empty if tournament search

    # Only popularity endpoint
    popularity: Optional[Popularity] = field(default=None, compare=False)

    client: Optional["RoyaleAPIClient"] = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        self.creator = Player.de_json(self.creator, self.client)
        self.players = Player.de_list(self.players, self.client)
        self.popularity = Popularity.de_json(self.popularity, self.client)

    def create_datetime(self, *args, **kwargs) -> datetime:
        return datetime.fromtimestamp(self.create_time, *args, **kwargs)

    def start_datetime(self, *args, **kwargs) -> datetime:
        if not self.start_time:
            raise ValueError("Tournament has not started")
        return datetime.fromtimestamp(self.start_time, *args, **kwargs)

    def end_datetime(self, *args, **kwargs) -> datetime:
        if not self.end_time:
            raise ValueError("Tournament has not ended")
        return datetime.fromtimestamp(self.end_time, *args, **kwargs)

    def updated_at_datetime(self, *args, **kwargs) -> datetime:
        if not self.updated_at:
            raise ValueError("Not a full tournament object")
        return datetime.fromtimestamp(self.updated_at, *args, **kwargs)

    def duration_in_hours(self) -> int or float:
        return 0.5 if self.duration == 1800 else self.duration // 3600

    def get_tournament(self, *args, **kwargs) -> "Tournament":
        return self.client.get_tournament(self.tag, *args, **kwargs)

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["Tournament"]:
        if not data:
            return None
        data = super().de_json(data, client)
        if "current_players" in data:
            data["player_count"] = data.pop("current_players")
        if "members" in data:
            data["players"] = data.pop("members")
        return cls(client=client, **data)
