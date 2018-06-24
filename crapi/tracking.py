from crapi.base import CRObject


class Tracking(CRObject):
    def __init__(self, active, available, snapshot_count):
        self.active = active
        self.available = available
        self.snapshot_count = snapshot_count

        self._id_attrs = None

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        return cls(**data)
