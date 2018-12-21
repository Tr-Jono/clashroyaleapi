VALID_TAG_CHARS = "0289CGJLPQRUVY"


class CardType:
    TROOP = "Troop"
    SPELL = "Spell"
    BUILDING = "Building"


class CardRarity:
    COMMON = "Common"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


class ClanType:
    OPEN = "open"
    INVITE_ONLY = "invite only"
    CLOSED = "closed"


class ClanRole:
    MEMBER = "member"
    ELDER = "elder"
    CO_LEADER = "coLeader"
    LEADER = "leader"


class ClanBattleType:
    ALL = "all"
    WAR = "war"
    CLANMATE = "clanMate"


class ClanWarState:
    NOT_IN_WAR = "notInWar"
    COLLECTION_DAY = "collectionDay"
    MATCHMAKING = "matchmaking"
    WAR_DAY = "warDay"


class TournamentState:
    IN_PREPARATION = "inPreparation"
    IN_PROGRESS = "inProgress"
    ENDED = "ended"


# I have no clue what most of the following battle stuff means


class BattleType:  # Battle.battle_type
    FRIENDLY = "friendly"
    CHALLENGE = "challenge"
    CLANMATE = "clanMate"  # In-clan friendly battle
    CLAN_WAR_WAR_DAY = "clanWarWarDay"
    TWO_VS_TWO = "2v2"


class BattleModeName:  # BattleMode.name
    CHALLENGE = "Challenge"
    CARD_RELEASE_DRAFT = "CardReleaseDraft"  # New card release draft challenge (e.g. ewiz draft)
    SHOWDOWN_LADDER = "Showdown_Ladder"  # ???
    TEAM_VS_TEAM_LADDER = "TeamVsTeamLadder"  # 2v2


class DeckType:  # Battle.deck_type
    COLLECTION = "Collection"  # From your own card collection
    DRAFT = "Draft"
    SLOT_DECK = "slotDeck"  # ???


class CardLevelType:  # BattleMode.card_levels
    FRIENDLY = "Friendly"  # Lv.9
    LADDER = "Ladder"  # Lv.1 - Lv.13
    TOURNAMENT = "Tournament"  # Lv.1 - Specified cap (usually Lv.9)


class PlayerType:  # BattleMode.players
    PVP = "PvP"  # 1v1
    TVT = "TvT"  # 2v2
