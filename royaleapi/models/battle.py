from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

from royaleapi.models.arena import Arena
from royaleapi.models.base import CRObject
from royaleapi.models.battle_mode import BattleMode
from royaleapi.models.player import Player

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass
class Battle(CRObject):
    battle_type: str = field(compare=False)
    challenge_type: Optional[str] = field(compare=False)
    mode: BattleMode = field(compare=False)
    win_count_before: Optional[int] = field(compare=False)
    utc_time: int
    deck_type: str = field(compare=False)
    team_size: int = field(compare=False)
    result: int = field(compare=False)
    team_crowns: int = field(compare=False)
    opponent_crowns: int = field(compare=False)
    team: List[Player]
    opponent: List[Player]
    arena: Arena = field(compare=False)
    tournament_tag: Optional[int] = field(default=None, compare=False)
    client: Optional["RoyaleAPIClient"] = field(default=None, compare=False)

    def __post_init__(self):
        self.mode = BattleMode.de_json(self.mode, self.client)
        self.team = Player.de_list(self.team, self.client)
        self.opponent = Player.de_list(self.opponent, self.client)
        self.arena = Arena.de_json(self.arena, self.client)

    def get_team(self, use_cache=True):
        return self.client.get_players([p.tag for p in self.team], use_cache=use_cache)

    def get_opponents(self, use_cache=True):
        return self.client.get_players([p.tag for p in self.opponent], use_cache=use_cache)

    @classmethod
    def de_json(cls, data, client):
        if not data:
            return None
        data = super().de_json(data, client)
        if "type" in data:
            data["battle_type"] = data.pop("type")
        if "winner" in data:
            data["result"] = data.pop("winner")
        return cls(client=client, **data)
