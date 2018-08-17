import json
from itertools import chain

import requests

from royaleapi.error import (CRError, InvalidToken, ServerResponseInvalid, BadRequest, Unauthorized,
                             NotFound, ServerError, ServerUnderMaintenance, ServerOffline)
from royaleapi.models import Battle, ChestCycle, Clan, Player, ServerStatus
from royaleapi.utils import tag_check, ExpiringDict


class RoyaleAPIClient:
    def __init__(self, dev_key, use_cache=False, dynamic_cache_time=180, dynamic_cache_capacity=128,
                 server_info_cache_time=300, constants_cache_time=86400, headers=None,
                 api_base_url="https://api.royaleapi.com/"):
        self.dev_key = self._validate_token(dev_key)
        self.session = requests.Session()
        self._cache = None
        self.headers = {"auth": self.dev_key}
        self.api_base_url = api_base_url
        if use_cache:
            self._cache = {"dynamic": ExpiringDict(timeout=dynamic_cache_time, capacity=dynamic_cache_capacity),
                           "api_info": ExpiringDict(timeout=server_info_cache_time, capacity=3),
                           "constants": ExpiringDict(timeout=constants_cache_time, capacity=2)}
        if headers:
            self.headers.update(headers)

    def __repr__(self):
        return f"<{__name__}.{self.__class__.__name__} use_cache={bool(self._cache)}>"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.session.close()

    @staticmethod
    def _validate_token(api_token):
        if not api_token or not isinstance(api_token, str) or any(c.isspace() for c in api_token):
            raise InvalidToken
        return api_token

    def _request(self, endpoint, params=None, return_text=False):
        if params:
            response = self.session.get(f"{self.api_base_url}{endpoint}", params=params, headers=self.headers)
        else:
            response = self.session.get(f"{self.api_base_url}{endpoint}", headers=self.headers)
        return self._parse(response, return_text)

    @staticmethod
    def _parse(response, return_text=False):
        try:
            data = json.loads(response.content.decode("utf-8"))
        except UnicodeDecodeError:
            raise ServerResponseInvalid("Server response could not be decoded using UTF-8.")
        except ValueError:
            if return_text:
                return response.text
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
                else:
                    raise CRError(message)
        except AttributeError as e:
            if str(e) != "'list' object has no attribute 'get'":
                raise
        return data

    def _get_methods_args_processor(self, endpoint, max_results=None, page=None, **kwargs):
        endpoint = requests.utils.quote(endpoint, safe=":/")
        if max_results is not None and not isinstance(max_results, int) and max_results < 1:
            raise ValueError("Parameter 'max_results' must be a positive integer if given.")
        if page is not None and not isinstance(page, int) and page < 0:
            raise ValueError("Parameters 'page' must be a non-negative integer if given.")
        if page and not max_results:
            raise ValueError("Parameter 'max_results' must be provided if parameter 'page' is given.")
        kwargs.update({"max": max_results, "page": page})
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        if kwargs:
            return self._request(endpoint, params=kwargs)
        return self._request(endpoint)

    def _purge_cache(self, cache_type="dynamic"):
        self._cache[cache_type].purge()

    def _fetch_from_cache(self, keys, cache_type="dynamic"):
        if isinstance(keys, str):
            return self._cache[cache_type][keys]
        return [self._cache[cache_type][key] for key in keys]

    def _save_in_cache(self, keys, data, cache_type="dynamic"):
        if isinstance(keys, str) or len(keys) == 1:
            self._cache[cache_type][(keys if isinstance(keys, str) else keys[0])] = data
        else:
            for key, data_section in list(zip(keys, data)):
                self._cache[cache_type][key] = data_section

    def _get_methods_base(self, endpoint, key, use_cache, cache_type="api_info", return_text=False):
        if self._cache:
            self._purge_cache(cache_type)
        try:
            assert self._cache and use_cache
            data = self._fetch_from_cache(key, cache_type)
        except (AssertionError, KeyError):
            data = self._request(endpoint, return_text=return_text)
            if self._cache:
                self._save_in_cache(key, data, cache_type)
        return data

    def _get_methods_with_tags_base(self, endpoint, tags, keys, use_cache, cache_type="dynamic", **kwargs):
        if self._cache:
            self._purge_cache(cache_type)
        try:
            assert self._cache and use_cache
            data = self._fetch_from_cache(keys, cache_type)
            if len(data) == 1:
                data = data[0]
        except (AssertionError, KeyError):
            path = endpoint.format(f"{','.join(tags)}")
            if kwargs:
                data = self._get_methods_args_processor(path, **kwargs)
            else:
                data = self._request(path)
            if self._cache:
                self._save_in_cache(keys, data, cache_type)
        return data

    def get_player(self, player_tags, *args, use_cache=True):
        tags, given_single_tag = tag_check(player_tags, args)
        keys = [f"p{tag}" for tag in tags]
        data = self._get_methods_with_tags_base("player/{}", tags, keys, use_cache)
        return Player.de_json(data) if given_single_tag else Player.de_list(data)

    def get_player_battles(self, player_tags, *args, max_results=None, page=None, use_cache=True):
        tags = tag_check(player_tags, args)[0]
        keys = [f"pb{tag}" for tag in tags]
        if self._cache:  # This method does not use _get_methods_with_tags_base since all results are in the same list
            self._purge_cache()
        try:
            assert self._cache and use_cache and max_results is page is None
            data = self._fetch_from_cache(keys)
            data = data[0] if len(data) == 1 else list(chain(*data))
        except (AssertionError, KeyError):
            data = self._get_methods_args_processor(f"player/{','.join(tags)}/battle", max_results, page)
            if len(tags) == 1 and max_results is page is None and self._cache:
                self._save_in_cache(keys, data)
        return Battle.de_list(data)

    def get_player_chests(self, player_tags, *args, use_cache=True):
        tags, given_single_tag = tag_check(player_tags, args)
        keys = [f"pc{tag}" for tag in tags]
        data = self._get_methods_with_tags_base("player/{}/chests", tags, keys, use_cache)
        return ChestCycle.de_json(data) if given_single_tag else ChestCycle.de_list(data)

    def get_clan(self, clan_tags, *args, use_cache=True):
        tags, given_single_tag = tag_check(clan_tags, args)
        keys = [f"c{tag}" for tag in tags]
        data = self._get_methods_with_tags_base("clan/{}", tags, keys, use_cache)
        return Clan.de_json(data) if given_single_tag else Clan.de_list(data)

    def get_version(self, use_cache=True):
        data = self._get_methods_base("version", "v", use_cache, return_text=True)
        return data

    def get_health(self, use_cache=True):
        data = self._get_methods_base("health", "h", use_cache, return_text=True)
        return data

    def get_status(self, use_cache=True):
        data = self._get_methods_base("status", "s", use_cache, return_text=True)
        return ServerStatus.de_json(data)

    def get_endpoints(self, use_cache=True):
        data = self._get_methods_base("endpoints", "e", use_cache, cache_type="constants", return_text=True)
        return data

    get_players = get_player
    get_players_battles = get_player_battles
    get_players_chests = get_player_chests
    get_clans = get_clan
