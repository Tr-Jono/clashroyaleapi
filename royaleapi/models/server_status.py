from dataclasses import dataclass
from typing import Dict, Optional, Any, TYPE_CHECKING

from royaleapi.models.base import CRObject

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


@dataclass(eq=False)
class ServerStatus(CRObject):
    env: str
    server_time: str
    server_version: str
    node_version: str
    host: str
    uptime: float
    uptime_human: str
    free_memory: str
    memory_usage: str

    @classmethod
    def de_json(cls, data: Dict[str, Any], client: "RoyaleAPIClient") -> Optional["ServerStatus"]:
        if not data:
            return None
        data = super().de_json(data, client)
        return cls(**data)
