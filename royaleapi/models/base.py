from abc import ABCMeta
from dataclasses import dataclass

from royaleapi.utils import camel_to_snake


@dataclass(init=False, repr=False, eq=False)
class CRObject(metaclass=ABCMeta):
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            raise ValueError("The two objects are not comparable!")
        return NotImplemented

    def __getitem__(self, item):
        return self.__dict__[item]

    def to_dict(self, _pretty_format=False):
        if _pretty_format:
            return {**self.__dict__, "_": self.__class__.__name__}
        else:
            data = {}
            for k, v in self.__dict__.items():
                if v not in (None, []):
                    if isinstance(v, CRObject):
                        data[k] = v.to_dict()
                    elif isinstance(v, list):
                        data[k] = [i.to_dict() for i in v]
                    else:
                        data[k] = v
            return data

    def stringify(self, omit_none_values=True):
        return self._pretty_format(self)

    @classmethod
    def de_json(cls, data, client):
        data = data.copy()
        return {camel_to_snake(x): data[x] for x in data}

    @classmethod
    def de_list(cls, data, client):
        if not data:
            return []
        if isinstance(data, dict):
            data = [data]
        return [cls.de_json(obj, client) for obj in data]

    @staticmethod
    def _pretty_format(obj, indent=0):
        result = []
        if isinstance(obj, CRObject):
            obj = obj.to_dict(_pretty_format=True)
        if isinstance(obj, dict):
            result += [obj.get("_", "dict"), "("]
            if obj:
                result.append("\n")
                indent += 1
                for k, v in obj.items():
                    if k in ("_", "client") or v in (None, []):
                        continue
                    result += ["\t" * indent, k, "=", CRObject._pretty_format(v, indent), ",\n"]
                del result[-1]  # remove last ",\n"
                indent -= 1
                result += ["\n", "\t" * indent]
            result.append(")")
        elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes)):
            result.append("[\n")
            indent += 1
            for x in obj:
                result += ["\t" * indent, CRObject._pretty_format(x, indent), ",\n"]
            indent -= 1
            result += ["\t" * indent, "]"]
        else:
            result.append(repr(obj))
        return "".join(result)
