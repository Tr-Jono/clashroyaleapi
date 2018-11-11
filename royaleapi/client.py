import json

import requests

from royaleapi.constants import ClanBattleType
from royaleapi.error import (RoyaleAPIError, InvalidToken, ServerResponseInvalid, BadRequest, Unauthorized,
                             NotFound, TooManyRequests, InternalServerError, ServerUnderMaintenance, ServerOffline)
from royaleapi.models import Battle, ChestCycle, Clan, Player, ServerStatus
from royaleapi.utils import tag_check, ExpiringDict


class RoyaleAPIClient:
    def __init__(self, dev_key, use_cache=False, dynamic_cache_time=60, dynamic_cache_capacity=128,
                 server_info_cache_time=180, constants_cache_time=86400, headers=None,
                 api_base_url="https://api.royaleapi.com/"):
        self._dev_key = self._validate_token(dev_key)
        self.session = requests.Session()
        self._cache = None
        self.headers = {"auth": self._dev_key}
        self.api_base_url = api_base_url
        if use_cache:
            self._cache = {"dynamic": None, "server_info": None, "constants": None}
            if dynamic_cache_time > 0:
                self._cache["dynamic"] = ExpiringDict(timeout=dynamic_cache_time, capacity=dynamic_cache_capacity)
            if server_info_cache_time > 0:
                self._cache["server_info"] = ExpiringDict(timeout=server_info_cache_time, capacity=3)
            if constants_cache_time > 0:
                self._cache["constants"] = ExpiringDict(timeout=constants_cache_time, capacity=2)
        if headers:
            self.headers.update(headers)

    def __repr__(self):
        return f"{self.__class__.__name__}(dev_key=\"{self._dev_key}\", use_cache={bool(self._cache)})"

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
            if return_text:
                return response.text
            data = json.loads(response.content.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            raise ServerResponseInvalid("Invalid server response")
        if isinstance(data, dict) and data.get("error"):
            status, message = data.get("status"), data.get("message", "")
            if status == 400:
                raise BadRequest(message)
            elif status == 401:
                raise Unauthorized(message)
            elif status == 404:
                raise NotFound(message)
            elif status == 429:
                raise TooManyRequests(message)
            elif status == 500:
                raise InternalServerError(message)
            elif status == 503:
                raise ServerUnderMaintenance(message)
            elif status == 522:
                raise ServerOffline(message)
            else:
                raise RoyaleAPIError(message)
        return data

    def _get_methods_args_processor(self, endpoint, max_results=None, page=None, **kwargs):
        endpoint = requests.utils.quote(endpoint, safe=":/")
        if max_results is not None and not isinstance(max_results, int) and max_results < 1:
            raise ValueError("Parameter 'max_results' must be a positive integer if given")
        if page is not None and not isinstance(page, int) and page < 0:
            raise ValueError("Parameters 'page' must be a non-negative integer if given")
        if page and not max_results:
            raise ValueError("Parameter 'max_results' must be provided if parameter 'page' is given")
        kwargs.update({"max": max_results, "page": page})
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        if kwargs:
            return self._request(endpoint, params=kwargs)
        return self._request(endpoint)

    def _purge_cache(self, cache_type="dynamic"):
        self._cache[cache_type].purge()

    def _fetch_from_cache(self, keys, cache_type):
        if isinstance(keys, str):
            return self._cache[cache_type][keys]
        return [self._cache[cache_type][key] for key in keys]

    def _save_in_cache(self, keys, data, cache_type="dynamic"):
        if isinstance(keys, str) or len(keys) == 1:
            self._cache[cache_type][(keys if isinstance(keys, str) else keys[0])] = data
        else:
            for key, data_section in list(zip(keys, data)):
                self._cache[cache_type][key] = data_section

    def _get_methods_base(self, endpoint, key, use_cache, cache_type="server_info", return_text=False):
        if self._cache and self._cache[cache_type] is not None:
            self._purge_cache(cache_type)
        try:
            assert self._cache and use_cache and self._cache[cache_type] is not None
            data = self._fetch_from_cache(key, cache_type)
        except (AssertionError, KeyError) as e:
            data = self._request(endpoint, return_text=return_text)
            if self._cache and isinstance(e, KeyError):
                self._save_in_cache(key, data, cache_type)
        return data

    def _get_methods_with_tags_base(self, endpoint, tags, keys, use_cache, cache_type="dynamic", **kwargs):
        if self._cache and self._cache[cache_type] is not None:
            self._purge_cache(cache_type)
        try:
            assert self._cache and use_cache and self._cache[cache_type] is not None
            data = self._fetch_from_cache(keys, cache_type)
            if len(data) == 1:
                data = data[0]
        except (AssertionError, KeyError) as e:
            path = endpoint.format(f"{','.join(tags)}")
            data = self._get_methods_args_processor(path, **kwargs) if kwargs else self._request(path)
            if isinstance(e, KeyError):
                self._save_in_cache(keys, data, cache_type)
        return data

    def get_player(self, player_tags, *args, use_cache=True):
        tags, given_single_tag = tag_check(player_tags, args)
        keys = [f"p{tag}" for tag in tags]
        data = self._get_methods_with_tags_base("player/{}", tags, keys, use_cache)
        return Player.de_json(data, self) if given_single_tag else Player.de_list(data, self)

    def get_player_battles(self, player_tags, *args, max_results=None, page=None, use_cache=True):
        tags = tag_check(player_tags, args)[0]
        keys = [f"pb{tag}" for tag in tags]
        # Does not use _get_methods_with_tags_base since all battles of diff players are merged into same list
        if self._cache and self._cache["dynamic"] is not None:
            self._purge_cache()
        try:
            assert self._cache and use_cache and self._cache["dynamic"] is not None and max_results is page is None
            data = self._fetch_from_cache(keys, "dynamic")
            data = data[0] if len(data) == 1 else [b for i in data for b in i]
        except (AssertionError, KeyError) as e:
            data = self._get_methods_args_processor(f"player/{','.join(tags)}/battle", max_results, page)
            if not data:
                raise NotFound("Response code 404 (Not Found) | Additional information and support: "
                               "http://discord.me/royaleapi")
            if len(tags) == 1 and isinstance(e, KeyError):
                self._save_in_cache(keys, data)
        return Battle.de_list(data, self)

    def get_clan_battles(self, clan_tags, *args, battle_type=ClanBattleType.CLANMATE,
                         max_results=None, page=None, use_cache=True):
        if battle_type not in (ClanBattleType.ALL, ClanBattleType.CLANMATE, ClanBattleType.WAR):
            raise ValueError("Invalid battle type")
        tags = tag_check(clan_tags, args)[0]
        keys = [f"cb{battle_type[0].lower()}{tag}" for tag in tags]
        # Does not use _get_methods_with_tags_base since all battles of diff players are merged into same list
        if self._cache and self._cache["dynamic"] is not None:
            self._purge_cache()
        try:
            assert self._cache and use_cache and self._cache["dynamic"] is not None and max_results is page is None
            data = self._fetch_from_cache(keys, "dynamic")
            data = data[0] if len(data) == 1 else [b for i in data for b in i]
        except (AssertionError, KeyError) as e:
            data = self._get_methods_args_processor(f"clan/{','.join(tags)}/battle",
                                                    max_results, page, type=battle_type)
            if not data:
                raise NotFound("Response code 404 (Not Found) | Additional information and support: "
                               "http://discord.me/royaleapi")
            if len(tags) == 1 and isinstance(e, KeyError):
                self._save_in_cache(keys, data)
        return Battle.de_list(data, self)

    def get_player_chests(self, player_tags, *args, use_cache=True):
        tags, given_single_tag = tag_check(player_tags, args)
        keys = [f"pc{tag}" for tag in tags]
        data = self._get_methods_with_tags_base("player/{}/chests", tags, keys, use_cache)
        return ChestCycle.de_json(data, self) if given_single_tag else ChestCycle.de_list(data, self)

    def get_clan(self, clan_tags, *args, use_cache=True):
        tags, given_single_tag = tag_check(clan_tags, args)
        keys = [f"c{tag}" for tag in tags]
        data = self._get_methods_with_tags_base("clan/{}", tags, keys, use_cache)
        return Clan.de_json(data, self) if given_single_tag else Clan.de_list(data, self)

    def get_version(self, use_cache=True):
        data = self._get_methods_base("version", "v", use_cache, return_text=True)
        return data

    def get_health(self, use_cache=True):
        data = self._get_methods_base("health", "h", use_cache, return_text=True)
        return data

    def get_status(self, use_cache=True):
        data = self._get_methods_base("status", "s", use_cache, return_text=True)
        return ServerStatus.de_json(data, self)

    def get_endpoints(self, use_cache=True):
        data = self._get_methods_base("endpoints", "e", use_cache, cache_type="constants", return_text=True)
        return data

    get_players = get_player
    get_players_battles = get_player_battles
    get_players_chests = get_player_chests
    get_clans = get_clan
    get_clans_battles = get_clan_battles
