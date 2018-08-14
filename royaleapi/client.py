import json
import requests

from royaleapi.models import Clan
from royaleapi.models import Player
from royaleapi.utils import validate_tag, is_iterable
from royaleapi.constants import API_BASE_URL
from royaleapi.error import (InvalidToken, ServerResponseInvalid, BadRequest, Unauthorized, NotFound,
                             ServerError, ServerUnderMaintenance, ServerOffline)


class CRClient:
    def __init__(self, api_token, headers=None):
        self.api_token = self._validate_token(api_token)
        self.session = requests.Session()
        self.headers = {"auth": api_token}
        if headers:
            self.headers.update(headers)

    @staticmethod
    def _validate_token(api_token):
        if any(x.isspace() for x in api_token):
            raise InvalidToken
        return api_token

    def _request(self, endpoint):
        return self._parse(self.session.request("GET", f"{API_BASE_URL}{endpoint}", headers=self.headers).content)

    @staticmethod
    def _parse(json_data):
        try:
            data = json.loads(json_data.decode("utf-8"))
        except UnicodeDecodeError:
            raise ServerResponseInvalid("Server response could not be decoded using UTF-8.")
        except ValueError:
            raise ServerResponseInvalid("Invalid server response.")
        try:
            if data.get("error"):
                status, message = data.get("status"), data.get("message", "")
                if status == 400:
                    raise BadRequest(message)
                elif status == 401:
                    raise Unauthorized(message)
                elif status == 404:
                    raise NotFound(message)
                elif status == 500:
                    raise ServerError(message)
                elif status == 503:
                    raise ServerUnderMaintenance(message)
                elif status == 522:
                    raise ServerOffline(message)
        except AttributeError as e:
            if str(e) != "'list' object has no attribute 'get'":
                raise
        return data

    def _get_methods_base(self, endpoint, max_results=None, page=None, **kwargs):
        if max_results is not None and not isinstance(max_results, int) and max_results < 1:
            raise ValueError("Parameter 'max_results' must be a positive integer if given.")
        if page is not None and not isinstance(page, int) and page < 0:
            raise ValueError("Parameters 'page' must be a non-negative integer if given.")
        if not max_results and page:
            raise ValueError("Parameter 'max_results' must be provided if parameter 'page' is given.")
        if len([key for key in kwargs if key in ("max", "page")]):
            raise ValueError("Keyword arguments must not overwrite pagination arguments.")
        if any((max_results, page, kwargs)):
            endpoint += "?"
            param_dict = {"max": max_results, "page": page, **kwargs}
            for key in param_dict:
                if param_dict[key] is not None:
                    endpoint += f"{key}={param_dict[key]}&"
            endpoint = endpoint[:-1]  # remove last "&"
        return self._request(endpoint)

    def get_version(self):
        return self.session.request("GET", f"{API_BASE_URL}version", headers=self.headers).text

    # def get_constants(self, max_results=None, page=None):
    #     return self._get_methods_base("constants", max_results, page)

    def get_player(self, player_tag):
        return Player.de_json(self._get_methods_base(f"player/{validate_tag(player_tag)}"))

    def get_players(self, player_tags, max_results=None, page=None):
        if not is_iterable(player_tags):
            player_tags = (player_tags,)
        player_tags = [validate_tag(tag) for tag in player_tags]
        return Player.de_list(self._get_methods_base(f"player/{','.join(player_tags)}", max_results, page))

    # def get_player_battles(self, player_tag, max_results=None, page=None):
    #     return self._get_methods_base(f"player/{player_tag}/battles", max_results, page)
    #
    # def get_players_battles(self, player_tags, max_results=None, page=None):
    #     return self._get_methods_base(f"player/{player_tags}/battles", max_results, page)

    def get_clan(self, clan_tag):
        return Clan.de_json(self._get_methods_base(f"clan/{validate_tag(clan_tag)}"))

    def get_clans(self, clan_tags):
        if not is_iterable(clan_tags):
            clan_tags = (clan_tags,)
        clan_tags = [validate_tag(tag) for tag in clan_tags]
        return Clan.de_list(self._get_methods_base(f"clan/{','.join(clan_tags)}"))
