from crapi.base import CRObject


class Card(CRObject):
    def __init__(self,
                 key,
                 name,
                 elixir,
                 card_type,
                 rarity,
                 arena,
                 description,
                 card_id,

                 # Only for cards returned from "player" endpoint
                 level=None,
                 max_level=None,
                 count=None,
                 required_for_upgrade=None,
                 left_to_upgrade=None,
                 icon=None):
        self.key = key
        self.name = name
        self.elixir = elixir
        self.card_type = card_type
        self.rarity = rarity
        self.arena = arena
        self.description = description
        self.card_id = card_id

        # only returned from player objects
        self.level = level
        self.max_level = max_level,
        self.count = count,
        self.required_for_upgrade = required_for_upgrade,
        self.left_to_upgrade = left_to_upgrade,
        self.icon = icon

        self._id_attrs = None
        if self.key:
            self._id_attrs = (self.key,)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(Card, cls).de_json(data)
        if data.get("type"):
            data["card_type"] = data.pop("type")
        if data.get("id"):
            data["card_id"] = data.pop("id")
        return cls(**data)

    @classmethod
    def de_list(cls, data):
        if not data:
            return []
        return [cls.de_json(card) for card in data]
