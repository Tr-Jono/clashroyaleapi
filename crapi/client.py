import json
import requests
import warnings

from crapi.player import Player, Clan
from crapi.utils import validate_tag, is_iterable, is_non_empty_str
from crapi.constants import API_BASE_URL
from crapi.error import (InvalidToken, ServerResponseInvalid, BadRequest, Unauthorized, NotFound, InternalServerError,
                         ServerUnderMaintenance, ServerOffline)


class Client:
    def __init__(self, api_token, custom_headers=None):
        self.api_token = self._validate_token(api_token)
        self.session = requests.Session()
        self.headers = {"auth": api_token}
        if custom_headers:
            self.headers.update(custom_headers)

    @staticmethod
    def _validate_token(api_token):
        """A very basic validation on given api token."""
        if any(x.isspace() for x in api_token):
            raise InvalidToken
        return api_token

    def _request(self, endpoint):
        url = f"{API_BASE_URL}{endpoint}"
        data = self.session.request('GET', url, headers=self.headers).content
        return self._parse(data)

    @staticmethod
    def _parse(json_data):
        try:
            decoded_s = json_data.decode("utf-8")
            data = json.loads(decoded_s)
        except UnicodeDecodeError:
            raise ServerResponseInvalid("Server response could not be decoded using UTF-8.")
        except ValueError:
            raise ServerResponseInvalid("Invalid server response.")
        try:
            if data.get("error"):
                status = data.get("status")
                message = data.get("message")
                if status == 400:
                    raise BadRequest(message)
                elif status == 401:
                    raise Unauthorized(message)
                elif status == 404:
                    raise NotFound(message)
                elif status == 500:
                    raise InternalServerError(message)
                elif status == 503:
                    raise ServerUnderMaintenance(message)
                elif status == 522:
                    raise ServerOffline(message)
        except AttributeError as e:
            if str(e) != "'list' object has no attribute 'get'":
                raise
        return data

    def _get_methods_base(self, endpoint, keys=None, exclude=None, max_results=None, page=None, **kwargs):
        # Check endpoint
        if not is_non_empty_str(endpoint):
            raise ValueError("'Endpoint' must be a non-empty string!")
        # Check keys and exclude
        if keys is not None and exclude is not None:
            exclude = None
            warnings.warn("Keys and exclude should not be used together. Exclude is changed to None.")
        if not is_iterable(keys) and is_non_empty_str(keys):
            keys = (keys,)
        if not is_iterable(exclude) and is_non_empty_str(keys):
            exclude = (exclude,)
        # Check keys, exclude and kwargs
        for param in keys, exclude, kwargs:
            if param is None:
                continue
            elif is_iterable(param):
                if not all([is_non_empty_str(elem) for elem in param]):
                    raise ValueError("Parameters 'keys' and 'exclude' and keyword arguments must be non-empty strings "
                                     "or iterables of them.")
            else:
                raise ValueError("Parameters 'keys' and 'exclude' and keyword arguments must be non-empty strings "
                                 "or iterables of them.")
        # Check max_results and page
        if max_results is None and page is not None:
            raise ValueError("Parameter 'max' must be provided if parameter 'page' is given.")
        for param in max_results, page:
            if param is not None and type(param) != int and param < 0:
                raise ValueError("Parameters 'max_results' and 'page' must be positive integers or None.")
        # Check kwargs
        if any([key for key in kwargs if key in ("keys", "exclude", "max", "page")]):
            raise ValueError("Keyword arguments must not overwrite field filter and pagination arguments.")
        # Real work begins
        if any((keys, exclude, max_results, page, kwargs)):
            endpoint += "?"
            param_dict = {"keys": keys, "exclude": exclude, "max": max_results, "page": page, **kwargs}  # max is a kw
            for key in param_dict:
                if param_dict[key] is not None:
                    if key in ("keys", "exclude"):
                        endpoint += f"{key}={','.join(param_dict[key])}"
                    else:
                        endpoint += f"{key}={param_dict[key]}&"
            endpoint = endpoint[:-1]  # remove the last "&"
        return self._request(endpoint)

    def get_version(self):
        version = self.session.request("GET", f"{API_BASE_URL}version", headers=self.headers).text
        return version

    # def get_constants(self, keys=None, exclude=None, max_results=None, page=None):
    #     return self._get_methods_base("constants", keys, exclude, max_results, page)

    def get_player(self, player_tag, keys=None, exclude=None):
        player_tag = validate_tag(player_tag)
        return Player.de_json(self._get_methods_base(f"player/{player_tag}", keys, exclude))

    def get_players(self, player_tags, keys=None, exclude=None, max_results=None, page=None):
        if not is_iterable(player_tags):
            player_tags = (player_tags,)
        player_tags = [validate_tag(tag) for tag in player_tags]
        return Player.de_list(self._get_methods_base(f"player/{','.join(player_tags)}",
                                                     keys, exclude, max_results, page))

    # def get_player_battles(self, player_tag, keys=None, exclude=None, max_results=None, page=None):
    #     return self._get_methods_base(f"player/{player_tag}/battles", keys, exclude, max_results, page)
    #
    # def get_players_battles(self, player_tags, keys=None, exclude=None, max_results=None, page=None):
    #     return self._get_methods_base(f"player/{player_tags}/battles", keys, exclude, max_results, page)

    def get_clan(self, clan_tag, keys=None, exclude=None):
        clan_tag = validate_tag(clan_tag)
        return Clan.de_json(self._get_methods_base(f"clan/{clan_tag}", keys, exclude))

    def get_clans(self, clan_tags, keys=None, exclude=None, max_results=None, page=None):
        if not is_iterable(clan_tags):
            clan_tags = (clan_tags,)
        clan_tags = [validate_tag(tag) for tag in clan_tags]
        return Clan.de_list(self._get_methods_base(f"clan/{','.join(clan_tags)}",
                                                   keys, exclude, max_results, page))
