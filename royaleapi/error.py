class RoyaleAPIError(Exception):
    pass


class InvalidToken(RoyaleAPIError):
    def __init__(self):
        super().__init__("Invalid api token")


class InvalidTag(RoyaleAPIError):
    def __init__(self):
        super().__init__("Invalid Clash Royale tag")


class ServerResponseInvalid(RoyaleAPIError):
    pass


class RequestError(RoyaleAPIError):
    pass


class BadRequest(RequestError):
    pass


class Unauthorized(RequestError):
    pass


class NotFound(RequestError):
    pass


class TooManyRequests(RequestError):
    pass


class ServiceUnavailable(RoyaleAPIError):
    pass


class InternalServerError(ServiceUnavailable):
    pass


class ServerUnderMaintenance(ServiceUnavailable):
    pass


class ServerOffline(ServiceUnavailable):
    pass
