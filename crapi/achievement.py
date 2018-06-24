from crapi.base import CRObject


class Achievement(CRObject):
    def __init__(self, name, stars, value, target, info):
        self.name = name
        self.stars = stars
        self.value = value
        self.target = target
        self.info = info

        self._id_attrs = (self.name,)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(Achievement, cls).de_json(data)
        return cls(**data)

    @classmethod
    def de_list(cls, data):
        if not data:
            return []
        return [cls.de_json(achv) for achv in data]
