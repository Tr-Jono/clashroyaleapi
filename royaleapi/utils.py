import re
from types import GeneratorType

from royaleapi.constants import VALID_TAG_CHARS
from royaleapi.error import InvalidTag


def camel_to_underscore(name):
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)).lower()


def validate_tag(tag):
    tag = tag.strip("#").upper().replace("O", "0")
    if not isinstance(tag, str) or tag == "" or len(tag) < 3 or any([c for c in tag if c not in VALID_TAG_CHARS]):
        raise InvalidTag
    return tag


def is_iterable(obj):
    return isinstance(obj, (list, tuple, dict, set, GeneratorType))
