from dataclasses import dataclass

from royaleapi.models.base import CRObject


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
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        return cls(**data)
