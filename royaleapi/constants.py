VALID_TAG_CHARS = "0289CGJLPQRUVY"


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
