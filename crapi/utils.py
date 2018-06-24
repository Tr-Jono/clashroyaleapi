import re
from types import GeneratorType

from crapi.constants import VALID_TAG_CHARS
from crapi.error import InvalidTag


def camel_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def validate_tag(tag):
    tag = tag.strip("#").upper().replace("O", "0")
    if not isinstance(tag, str) or tag == "" or len(tag) < 3:
        raise InvalidTag
    for char in tag:
        if char not in VALID_TAG_CHARS:
            raise InvalidTag
    return tag


def is_iterable(obj):
    return isinstance(obj, (list, tuple, dict, set, GeneratorType))


def is_non_empty_str(obj):
    return isinstance(obj, str) and obj != ""
