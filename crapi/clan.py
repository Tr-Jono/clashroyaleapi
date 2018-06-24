from crapi.base import CRObject
from crapi.clan_badge import ClanBadge


class Clan(CRObject):
    def __init__(self,
                 tag=None,
                 name=None,
                 badge=None,
                 donations=None,  # Different for "clan" (clan's donations) and "player" (player's donations) endpoint

                 # Only for clans returned from "clan" endpoint
                 clan_type=None,
                 score=None,
                 member_count=None,
                 required_score=None,
                 location=None,
                 members=None,

                 # Only for clans returned from "player" endpoint
                 role=None,
                 donations_received=None,
                 donations_delta=None):
        self.tag = tag
        self.name = name
        self.donations = donations  # Different for "clan" (clan's donations) and "player" (player's donations) endpoint

        # Only for clans returned from "clan" endpoint
        self.clan_type = clan_type
        self.score = score
        self.member_count = members
        self.required_score = required_score
        self.location = location
        self.members = members

        # Only for clans returned from "player" endpoint
        self.role = role
        self.donations = donations
        self.donations_received = donations_received
        self.donations_delta = donations_delta
        self.badge = ClanBadge.de_json(badge)

        self._id_attrs = None
        if self.tag:
            self._id_attrs = (self.tag,)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(Clan, cls).de_json(data)
        if data.get("type"):
            data["clan_type"] = data.pop("type")
        return cls(**data)

    @classmethod
    def de_list(cls, data):
        if not data:
            return []
        return [cls.de_json(clan) for clan in data]
