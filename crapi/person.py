from crapi.base import CRObject
from crapi.arena import Arena


class Person(CRObject):
    def __init__(self,
                 tag=None,
                 name=None,
                 trophies=None,
                 arena=None):
        self.tag = tag
        self.name = name
        self.trophies = trophies
        self.arena = Arena.de_json(arena)

        self._id_attrs = None
        if self.tag:
            self._id_attrs = (self.tag,)

    @classmethod
    def de_list(cls, data):
        if not data:
            return []
        return [cls.de_json(person) for person in data]
