import re
import time
from collections import OrderedDict
from types import GeneratorType

from royaleapi.constants import VALID_TAG_CHARS
from royaleapi.error import InvalidTag

FIRST_CAP_REGEX = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_REGEX = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(string):
    return ALL_CAP_REGEX.sub(r'\1_\2', FIRST_CAP_REGEX.sub(r'\1_\2', string)).lower()


def to_camel_case(string):
    c = string.split('_')
    return c[0] + ''.join(x.title() for x in c[1:])


def is_iterable(obj):
    return isinstance(obj, (list, tuple, dict, set, GeneratorType))


def validate_tag(tag):
    tag = tag.strip("#").upper().replace("O", "0")
    if not isinstance(tag, str) or tag == "" or len(tag) < 3 or any([c for c in tag if c not in VALID_TAG_CHARS]):
        raise InvalidTag
    return tag


def tag_check(tags, args):
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
        raise ValueError("Given argument(s) is/are not a tag nor iterables of them.")
    return tags, given_single_tag


class ExpiringDict(OrderedDict):
    # Users should purge the dict themselves if they access client cache or use this dict for other purposes
    def __init__(self, *args, timeout=300, capacity=None, **kwargs):
        assert timeout > 0 and (isinstance(capacity, int) or capacity is None)
        super().__init__(*args, **kwargs)
        self.timeout = timeout
        self.capacity = capacity

    def __getitem__(self, key):
        return super().__getitem__(key)[0]

    def __setitem__(self, key, value):
        super().__setitem__(key, (value, time.time()))

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def items(self):
        return ((k, v) for k, (v, _) in super().items())

    def values(self):
        return (v for v, _ in super().values())

    def purge(self):
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
