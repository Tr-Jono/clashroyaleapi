from crapi.base import CRObject


class ClanBadge(CRObject):
    def __init__(self, name, category, badge_id, image):
        self.name = name
        self.category = category
        self.badge_id = badge_id
        self.image = image

        self._id_attrs = (badge_id,)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(ClanBadge, cls).de_json(data)
        if data.get("id"):
            data["badge_id"] = data.pop("id")
        return cls(**data)