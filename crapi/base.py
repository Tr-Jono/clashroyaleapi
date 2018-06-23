import json

from abc import ABCMeta
from .utils import camel_to_underscore


class CRObject:
    """Base class for Clash Royale objects."""
    __metaclass__ = ABCMeta
    _id_attrs = ()

    def __str__(self):
        return str(self.to_dict())

    def __getitem__(self, item):
        return self.__dict__[item]

    @classmethod
    def de_json(cls, data):
        if not data:
            return None
        data = data.copy()
        return {camel_to_underscore(x): data[x] for x in data}

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        data = dict()
        for key in iter(self.__dict__):
            if key in ("_id_attrs",):
                continue

            value = self.__dict__[key]
            if value is not None:
                if hasattr(value, 'to_dict'):
                    data[key] = value.to_dict()
                else:
                    data[key] = value
        if data.get('battle_type'):
            data["type"] = data.pop("battle_type", None)
        if data.get('clan_type'):
            data["type"] = data.pop("clan_type", None)
        if data.get("tournament_type"):
            data["type"] = data.pop("tournament_type", None)
        if data.get("card_type"):
            data["type"] = data.pop("card_type", None)
        if data.get("card_id"):
            data["id"] = data.pop("card_id", None)
        if data.get("season_id"):
            data["id"] = data.pop("season_id", None)
        return data

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._id_attrs and other._id_attrs:
                return self._id_attrs == other._id_attrs
            else:
                raise ValueError("The two objects are not comparable!")
        return super(CRObject, self).__eq__(other)

    def __hash__(self):
        if self._id_attrs:
            return hash((self.__class__, self._id_attrs))
        return super(CRObject, self).__hash__()
