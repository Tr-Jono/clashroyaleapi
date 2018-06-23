from crapi import CRObject


class Clan(CRObject):
    def __init__(self,
                 tag=None,
                 name=None,

                 # Only for clans returned from "player" endpoint
                 role=None,
                 donations=None,
                 donations_received=None,
                 donations_delta=None,
                 badge=None):
        self.tag = tag
        self.name = name

        # Only for clans returned from "player" endpoint
        self.role = role
        self.donations = donations
        self.donations_received = donations_received
        self.donations_delta = donations_delta
        self.badge = badge

        self._id_attrs = None
        if self.tag:
            self._id_attrs = (self.tag,)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(Clan, cls).de_json(data)
        if all(v is None for v in data.values()):
            return None
        return cls(**data)

    @classmethod
    def de_list(cls, data):
        if not data:
            return []
        return [cls.de_json(clan) for clan in data]
