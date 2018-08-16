from dataclasses import dataclass, field
from typing import List, Optional

from royaleapi.models.arena import Arena
from royaleapi.models.base import CRObject
from royaleapi.models.battle_mode import BattleMode
from royaleapi.models.player import Player


@dataclass
class Battle(CRObject):
    battle_type: str = field(compare=False)
    challenge_type: str = field(compare=False)
    mode: BattleMode = field(compare=False)
    win_count_before: Optional[int] = field(compare=False)
    utc_time: int
    deck_type: str = field(compare=False)
    team_size: int = field(compare=False)
    winner: int = field(compare=False)
    team_crowns: int = field(compare=False)
    opponent_crowns: int = field(compare=False)
    team: List[Player]
    opponent: List[Player]
    arena: Arena = field(compare=False)

    def __post_init__(self):
        self.mode = BattleMode.de_json(self.mode)
        self.team = Player.de_list(self.team)
        self.opponent = Player.de_list(self.opponent)
        self.arena = Arena.de_json(self.arena)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        if "type" in data:
            data["battle_type"] = data.pop("type")
        return cls(**data)
