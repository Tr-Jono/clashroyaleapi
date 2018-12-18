class RoyaleAPIError(Exception):
    pass


class InvalidToken(RoyaleAPIError):
    def __init__(self) -> None:
        super().__init__("Invalid api token")


class InvalidTag(RoyaleAPIError):
    def __init__(self) -> None:
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


class ClanNotTracked(RequestError):
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


error_dict = {
    400: BadRequest,
    401: Unauthorized,
    404: NotFound,
    417: ClanNotTracked,
    429: TooManyRequests,
    500: InternalServerError,
    503: ServerUnderMaintenance,
    522: ServerOffline
}
