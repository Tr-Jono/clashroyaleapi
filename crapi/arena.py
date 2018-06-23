from crapi.base import CRObject


class Arena(CRObject):
    def __init__(self, name, arena, arena_id, trophy_limit):
        self.name = name
        self.arena = arena
        self.arena_id = arena_id
        self.trophy_limit = trophy_limit

        self._id_attrs = (self.arena_id,)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(Arena, cls).de_json(data)
        return cls(**data)

    @classmethod
    def de_list(cls, data):
        if not data:
            return []
        return [cls.de_json(arena) for arena in data]
