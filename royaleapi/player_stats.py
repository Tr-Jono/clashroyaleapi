from royaleapi.base import CRObject
from royaleapi.card import Card


class PlayerStats(CRObject):
    def __init__(self, clan_cards_collected, tournament_cards_won, max_trophies, three_crown_wins, cards_found,
                 favorite_card, total_donations, challenge_max_wins, challenge_cards_won, level):
        self.clan_cards_collected = clan_cards_collected
        self.tournament_cards_won = tournament_cards_won
        self.max_trophies = max_trophies
        self.three_crown_wins = three_crown_wins
        self.cards_found = cards_found
        self.favorite_card = Card.de_json(favorite_card)
        self.total_donations = total_donations
        self.challenge_max_wins = challenge_max_wins
        self.challenge_cards_won = challenge_cards_won
        self.level = level

        self._id_attrs = None

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = super(PlayerStats, cls).de_json(data)
        return cls(**data)
