from royaleapi.person import Person


class ClanMember(Person):
    def __init__(self, tag, name, trophies, arena, rank, role, level, donations, donations_received, donations_delta,
                 donations_percent, previous_rank=None):
        super().__init__(tag, name, trophies, arena)
        self.rank = rank
        self.role = role
        self.level = level
        self.donations = donations
        self.donations_received = donations_received
        self.donations_delta = donations_delta
        self.donations_percent = donations_percent
        self.previous_rank = previous_rank

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super().de_json(data)
        if data.get("exp_level"):
            data["level"] = data.pop("exp_level")
        del data["clan_chest_crowns"]  # no longer in game
        return cls(**data)
