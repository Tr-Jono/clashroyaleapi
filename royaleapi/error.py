class CRError(Exception):
    def __init__(self, message=""):
        super().__init__()
        self.message = message

    def __str__(self):
        return str(self.message)


class InvalidToken(CRError):
    def __init__(self):
        super().__init__("Invalid api token.")


class InvalidTag(CRError):
    def __init__(self):
        super().__init__("Invalid Clash Royale tag.")


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


class ServiceUnavailable(CRError):
    pass


class ServerError(ServiceUnavailable):
    pass


class ServerUnderMaintenance(ServiceUnavailable):
    pass


class ServerOffline(ServiceUnavailable):
    pass
