import re
import time
from collections import OrderedDict
from typing import Tuple, Generator, Iterable, Any, Optional

from royaleapi.constants import VALID_TAG_CHARS
from royaleapi.error import InvalidTag

FIRST_CAP_REGEX = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_REGEX = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(string) -> str:
    return ALL_CAP_REGEX.sub(r'\1_\2', FIRST_CAP_REGEX.sub(r'\1_\2', string)).lower()


def is_iterable(obj: Any) -> bool:
    return isinstance(obj, (list, tuple, dict, set, Generator))


def validate_tag(tag: str) -> str:
    tag = tag.lstrip("#").upper().replace("O", "0")
    if not isinstance(tag, str) or tag == "" or len(tag) < 3 or any([c for c in tag if c not in VALID_TAG_CHARS]):
        raise InvalidTag
    return tag


class ExpiringDict(OrderedDict):
    # Users should purge the dict themselves if they access client cache or use this dict for other purposes
    def __init__(self, *args: Iterable[Iterable[Any]], timeout: int = 300, capacity: Optional[int] = None,
                 **kwargs: Any) -> None:
        assert timeout > 0 and (isinstance(capacity, int) or capacity is None)
        super().__init__(*args, **kwargs)
        self.timeout = timeout
        self.capacity = capacity

    def __getitem__(self, key: Any) -> Any:
        return super().__getitem__(key)[0]

    def __setitem__(self, key: Any, value: Any) -> None:
        super().__setitem__(key, (value, time.time()))

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def items(self) -> Generator[Tuple[Any, Any], None, None]:
        return ((k, v) for k, (v, _) in super().items())

    def values(self) -> Generator[Any, None, None]:
        return (v for v, _ in super().values())

    def purge(self) -> None:
        if self.capacity:
            overflowing = max(0, len(self) - self.capacity)
            for _ in range(overflowing):
                self.popitem(last=False)
        limit = time.time() - self.timeout
        to_del = []
        for key, (_, set_time) in super().items():
            if set_time <= limit:
                to_del.append(key)
        for key in to_del:
            del self[key]
