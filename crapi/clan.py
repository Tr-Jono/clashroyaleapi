from crapi.base import CRObject
from crapi.clan_badge import ClanBadge
from crapi.clan_member import ClanMember
from crapi.location import Location
from crapi.tracking import Tracking


class Clan(CRObject):
    def __init__(self,
                 tag=None,
                 name=None,
                 badge=None,

                 # Only for clans returned from "clan" endpoint
                 description=None,
                 clan_type=None,
                 score=None,
                 member_count=None,
                 required_score=None,
                 total_donations=None,
                 location=None,
                 members=None,
                 tracking=None,

                 # Only for clans returned from "player" endpoint
                 role=None,
                 player_donations=None,
                 donations_received=None,
                 donations_delta=None):
        self.tag = tag
        self.name = name
        self.badge = ClanBadge.de_json(badge)

        # Only for clans returned from "clan" endpoint
        self.description = description
        self.clan_type = clan_type
        self.score = score
        self.member_count = member_count
        self.required_score = required_score
        self.total_donations = total_donations
        self.location = Location.de_json(location)
        self.members = ClanMember.de_list(members)
        self.tracking = Tracking.de_json(tracking)

        # Only for clans returned from "player" endpoint
        self.role = role
        self.player_donations = player_donations
        self.donations_received = donations_received
        self.donations_delta = donations_delta

        self._id_attrs = None
        if self.tag:
            self._id_attrs = (self.tag,)

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        if data.get("type"):
            data["clan_type"] = data.pop("type")
        if data.get("donations"):
            if data.get("donations_delta"):  # Clan object is from "player" endpoint
                data["player_donations"] = data.pop("donations")
            else:  # Clan object is from "clan" endpoint
                data["total_donations"] = data.pop("donations")
        if data.get("clan_chest"):  # no longer in game
            del data["clan_chest"]
        return cls(**data)

    @classmethod
    def de_list(cls, data):
        if not data:
            return []
        return [cls.de_json(clan) for clan in data]
