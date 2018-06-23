class CRError(Exception):
    def __init__(self, message=None):
        super(CRError, self).__init__()
        if message:
            self.message = message
        else:
            self.message = ""

    def __str__(self):
        return str(self.message)


class InvalidToken(CRError):
    def __init__(self):
        super(InvalidToken, self).__init__("Invalid api token.")


class InvalidTag(CRError):
    def __init__(self):
        super(InvalidTag, self).__init__("Invalid Clash Royale tag.")


class ServerResponseInvalid(CRError):
    pass


class RequestError(CRError):
    pass


class BadRequest(RequestError):
    pass


class Unauthorized(RequestError):
    pass


class NotFound(RequestError):
    pass


class ServerError(CRError):
    pass


class InternalServerError(ServerError):
    pass


class ServerUnderMaintenance(ServerError):
    pass


class ServerOffline(ServerError):
    pass
