from dataclasses import dataclass
from typing import List

from royaleapi.models.base import CRObject


@dataclass(eq=False)
class ChestCycle(CRObject):
    upcoming: List[str]
    super_magical: int
    magical: int
    legendary: int
    epic: int
    giant: int

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        return cls(**data)
