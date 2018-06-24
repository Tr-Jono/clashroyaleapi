from crapi.base import CRObject


class Location(CRObject):
    def __init__(self, name, is_country, code):
        self.name = name
        self.is_country = is_country
        self.code = code

        self._id_attrs = (self.code,)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        return cls(**data)
