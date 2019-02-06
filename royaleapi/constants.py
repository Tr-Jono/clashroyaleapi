VALID_TAG_CHARS = "0289CGJLPQRUVY"


class Chest:
    SILVER = "silver"
    GOLD = "gold"
    GIANT = "giant"
    MAGICAL = "magical"
    EPIC = "epic"
    LEGENDARY = "legendary"
    MEGA_LIGHTNING = "megaLightning"


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


class TournamentStatus:
    IN_PREPARATION = "inPreparation"
    IN_PROGRESS = "inProgress"
    ENDED = "ended"
