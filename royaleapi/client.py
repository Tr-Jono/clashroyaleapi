import json
from types import TracebackType
from typing import List, Tuple, Dict, Optional, Type

import requests

from royaleapi.constants import ClanBattleType
from royaleapi.error import RoyaleAPIError, InvalidToken, ServerResponseInvalid, error_dict
from royaleapi.models import Battle, ChestCycle, Clan, ClanTracking, ClanWar, Player, ServerStatus
from royaleapi.utils import is_iterable, validate_tag, ExpiringDict


class RoyaleAPIClient:
    def __init__(self, dev_key: str, use_cache: bool = False, dynamic_cache_time: int = 180,
                 dynamic_cache_capacity: int = 128, server_info_cache_time: int = 60,
                 constants_cache_time: int = 86400, headers: Optional[Dict] = None,
                 api_base_url: str = "https://api.royaleapi.com/"):
        self._dev_key = self._validate_token(dev_key)
        self.session = requests.Session()
        self._cache = None
        self.headers = {"auth": self._dev_key, **(headers or {})}
        self.api_base_url = api_base_url
        if use_cache:
            self._cache = {"dynamic": None, "server_info": None, "constants": None}
            if dynamic_cache_time > 0:
                self._cache["dynamic"] = ExpiringDict(timeout=dynamic_cache_time, capacity=dynamic_cache_capacity)
            if server_info_cache_time > 0:
                self._cache["server_info"] = ExpiringDict(timeout=server_info_cache_time, capacity=3)
            if constants_cache_time > 0:
                self._cache["constants"] = ExpiringDict(timeout=constants_cache_time, capacity=2)

    def __repr__(self):
        return f"{self.__class__.__name__}(use_cache={self._cache is not None})"

    def __enter__(self) -> "RoyaleAPIClient":
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:  # goddamn typing
        self.close()

    def close(self) -> None:
        self.session.close()

    @staticmethod
    def _validate_token(api_token: str) -> str:
        if not api_token or not isinstance(api_token, str) or any(c.isspace() for c in api_token):
            raise InvalidToken
        return api_token

    @staticmethod
    def _tag_check(tags: str or List[str], args: Tuple[str, ...]) -> Tuple[List[str], bool]:
        given_single_tag = False
        if isinstance(tags, str):
            if args:
                tags = [validate_tag(tag) for tag in (tags, *args)]
            else:
                tags = [validate_tag(tags)]
                given_single_tag = True
        elif is_iterable(tags):
            tags = [validate_tag(tag) for tag in (*tags, *args)] if args else [validate_tag(tag) for tag in tags]
        else:
            raise ValueError("Given argument(s) is/are not a tag nor iterables of them")
        return tags, given_single_tag

    def _purge_cache(self, cache_type: str = "dynamic") -> None:
        self._cache[cache_type].purge()

    def _fetch_from_cache(self, keys: str or List[str], cache_type: str = "dynamic") -> Dict or List[Dict]:
        if isinstance(keys, str):
            return self._cache[cache_type][keys]
        return [self._cache[cache_type][key] for key in keys]

    def _save_in_cache(self, keys: str or List[str], data: Dict or List[Dict], cache_type: str = "dynamic") -> None:
        if isinstance(keys, str) or len(keys) == 1:
            self._cache[cache_type][(keys if isinstance(keys, str) else keys[0])] = data  # it has to work like that smh
            return
        for k, v in zip(keys, data):
            self._cache[cache_type][k] = v

    def _request(self, endpoint: str, params: Optional[Dict] = None, return_text: bool = False) -> Dict or List[Dict]:
        response = self.session.get(f"{self.api_base_url}{endpoint}", params=params or {}, headers=self.headers)
        return self._parse(response, return_text)

    @staticmethod
    def _parse(response: requests.Response, return_text: bool = False) -> str or Dict or List[Dict]:
        if return_text:
            return response.text
        try:
            data = json.loads(response.content.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            raise ServerResponseInvalid("Invalid server response")
        if isinstance(data, dict) and "error" in data:
            status = data["status"]
            message = data["message"]
            if status in error_dict:
                raise error_dict[status](message)
            raise RoyaleAPIError(message)
        return data

    def _get_methods_args_processor(self, endpoint: str, max_results: Optional[int] = None,
                                    page: Optional[int] = None, **kwargs) -> Dict or List[Dict]:
        endpoint = requests.utils.quote(endpoint, safe=":/")
        assert max_results is None or max_results > 0, "Parameter 'max_results' must be > 0 if given"
        assert page is None or page >= 0, "Parameter 'page' must be >= 0 if given"
        if page is not None:
            assert max_results is not None, "Parameter 'max_results' must be provided if parameter 'page' is given"
        kwargs.update({"max": max_results, "page": page})
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return self._request(endpoint, params=kwargs)

    def _get_methods_base(self, endpoint: str, key: str, use_cache: bool, cache_type: str = "server_info",
                          return_text: bool = False) -> Dict or List[Dict]:
        try:
            assert self._cache and use_cache and self._cache[cache_type] is not None
            self._purge_cache(cache_type)
            data = self._fetch_from_cache(key, cache_type)
        except (AssertionError, KeyError):
            data = self._request(endpoint, return_text=return_text)
            if self._cache and self._cache[cache_type] is not None:
                self._save_in_cache(key, data, cache_type)
        return data

    def _get_methods_with_tags_base(self, endpoint: str, tags: List[str], keys: List[str], use_cache: bool,
                                    cache_type: str = "dynamic", **kwargs) -> Dict or List[Dict]:
        try:
            assert self._cache and use_cache and self._cache[cache_type] is not None
            self._purge_cache(cache_type)
            data = self._fetch_from_cache(keys, cache_type)
            if len(data) == 1:
                data = data[0]
        except (AssertionError, KeyError):
            path = endpoint.format(",".join(tags))
            data = self._get_methods_args_processor(path, **kwargs) if kwargs else self._request(path)
            if self._cache and self._cache[cache_type] is not None:
                self._save_in_cache(keys, data, cache_type)
        return data

    def get_player(self, player_tags: str or List[str], *args: str, use_cache: bool = True) -> Player or List[Player]:
        tags, given_single_tag = self._tag_check(player_tags, args)
        keys = [f"p{tag}" for tag in tags]
        data = self._get_methods_with_tags_base("player/{}", tags, keys, use_cache)
        return Player.de_json(data, self) if given_single_tag else Player.de_list(data, self)

    def get_player_chests(self, player_tags: str or List[str], *args: str,
                          use_cache: bool = True) -> ChestCycle or List[ChestCycle]:
        tags, given_single_tag = self._tag_check(player_tags, args)
        keys = [f"pc{tag}" for tag in tags]
        data = self._get_methods_with_tags_base("player/{}/chests", tags, keys, use_cache)
        return ChestCycle.de_json(data, self) if given_single_tag else ChestCycle.de_list(data, self)

    def get_player_battles(self, player_tags: str or List[str], *args: str, max_results: Optional[int] = None,
                           page: Optional[int] = None, use_cache: bool = True) -> List[Battle]:
        tags = self._tag_check(player_tags, args)[0]
        keys = [f"pb{tag}" for tag in tags]
        # Does not use _get_methods_with_tags_base since all battles of diff players are merged into same list
        try:
            assert self._cache and use_cache and self._cache["dynamic"] is not None and max_results is page is None
            self._purge_cache()
            data = self._fetch_from_cache(keys)
            data = data[0] if len(data) == 1 else [b for i in data for b in i]
        except (AssertionError, KeyError):
            data = self._get_methods_args_processor(f"player/{','.join(tags)}/battle", max_results, page)
            if len(tags) == 1 and self._cache and self._cache["dynamic"] is not None:
                self._save_in_cache(keys, data)
        return Battle.de_list(data, self)

    def get_clan(self, clan_tags: str or List[str], *args: str, use_cache: bool = True) -> Clan or List[Clan]:
        tags, given_single_tag = self._tag_check(clan_tags, args)
        keys = [f"c{tag}" for tag in tags]
        data = self._get_methods_with_tags_base("clan/{}", tags, keys, use_cache)
        return Clan.de_json(data, self) if given_single_tag else Clan.de_list(data, self)

    def get_clan_battles(self, clan_tag: str, battle_type: str = ClanBattleType.CLANMATE,
                         max_results: Optional[int] = None, page: Optional[int] = None,
                         use_cache: bool = True) -> List[Battle]:
        if battle_type not in (ClanBattleType.ALL, ClanBattleType.CLANMATE, ClanBattleType.WAR):
            raise ValueError("Invalid battle type")
        tag = validate_tag(clan_tag)
        key = f"cb{battle_type[0].lower()}{tag}"
        data = self._get_methods_with_tags_base("clan/{}/battle", [tag], [key], use_cache,
                                                max_results=max_results, page=page)
        return Battle.de_list(data, self)

    def get_clan_war(self, clan_tag: str, use_cache: bool = True) -> ClanWar:
        tag = validate_tag(clan_tag)
        key = f"cw{tag}"
        data = self._get_methods_with_tags_base("clan/{}/war", [tag], [key], use_cache)
        return ClanWar.de_json(data, self)

    def get_clan_war_log(self, clan_tag: str, use_cache: bool = True,
                         max_results: Optional[int] = None, page: Optional[int] = None) -> List[ClanWar]:
        tag = validate_tag(clan_tag)
        key = f"cwl{tag}"
        data = self._get_methods_with_tags_base("clan/{}/warlog", [tag], [key], use_cache,
                                                max_results=max_results, page=page)
        return ClanWar.de_list(data, self)

    def get_clan_tracking(self, clan_tags: str or List[str], *args: str,
                          use_cache: bool = True) -> ClanTracking or List[ClanTracking]:
        tags, given_single_tag = self._tag_check(clan_tags, args)
        keys = [f"ct{tag}" for tag in tags]
        data = self._get_methods_with_tags_base("clan/{}/tracking", tags, keys, use_cache)
        return ClanTracking.de_json(data, self) if given_single_tag else ClanTracking.de_list(data, self)

    def track_clan(self, clan_tags: str or List[str], *args: str) -> bool:
        tags = self._tag_check(clan_tags, args)[0]
        data = self._request(f"clan/{','.join(tags)}/track")
        return data["success"]

    def search_clans(self, name: Optional[str] = None, min_score: Optional[int] = None,
                     min_members: Optional[int] = None, max_members: Optional[int] = None,
                     location_id: Optional[int] = None, max_results: Optional[int] = None,
                     page: Optional[int] = None, use_cache: bool = True) -> List[Clan]:
        assert len(name) > 3, "The length of parameter 'name' must be >= 3 if given"
        assert min_score is None or min_score >= 0, "Parameter 'score' must be a non-negative integer if given"
        assert min_members is None or 2 <= min_members <= 50, "2 <= paramter 'min_members' <= 50 must be True if given"
        assert max_members is None or 2 <= max_members <= 50, "2 <= paramter 'max_members' <= 50 must be True if given"
        if min_members and max_members:
            assert min_members <= max_members, "Paramter 'min_members' must be <= parameter 'max_members'"
        assert location_id is None or 57000000 <= location_id <= 57000260, "Parameter 'location_id' is not a valid"
        assert any([param is not None for param in (name, min_score, min_members, max_members, location_id)]), (
            "At least one search parameter is required")
        key = f"cs?n={name}&ms={min_score}&mim={min_members}&mam={max_members}&li={location_id}"
        try:
            assert self._cache and use_cache and self._cache["dynamic"] is not None
            self._purge_cache()
            data = self._fetch_from_cache(key)
        except (AssertionError, KeyError):
            data = self._get_methods_args_processor("clan/search", max_results, page, name=name,
                                                    score=min_score, minMembers=min_members,
                                                    maxMembers=max_members, locationId=location_id)
            if self._cache and self._cache["dynamic"] is not None:
                self._save_in_cache(key, data)
        return Clan.de_list(data, self)

    def get_version(self, use_cache: bool = True) -> str:
        return self._get_methods_base("version", "v", use_cache, return_text=True)

    def get_health(self, use_cache: bool = True) -> str:
        return self._get_methods_base("health", "h", use_cache, return_text=True)

    def get_status(self, use_cache: bool = True) -> ServerStatus:
        return ServerStatus.de_json(self._get_methods_base("status", "s", use_cache), self)

    def get_endpoints(self, use_cache: bool = True) -> List[str]:
        return self._get_methods_base("endpoints", "e", use_cache, cache_type="constants")

    get_players = get_player
    get_players_battles = get_player_battles
    get_players_chests = get_player_chests
    get_clans = get_clan
    get_clans_tracking = get_clan_tracking
    track_clans = track_clan
