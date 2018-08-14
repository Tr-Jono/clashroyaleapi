from abc import ABCMeta
from dataclasses import dataclass, asdict

from royaleapi.utils import camel_to_underscore


@dataclass(init=False)
class CRObject:
    __metaclass__ = ABCMeta

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            raise ValueError("The two objects are not comparable!")
        return NotImplemented

    def __str__(self):
        return CRObject._pretty_format(self)

    def __getitem__(self, item):
        return self.__dict__[item]

    def to_dict(self, _pretty_format=False):
        return {**self.__dict__, "_": self.__class__.__name__} if _pretty_format else asdict(self)

    def stringify(self):
        return self._pretty_format(self, indent=0)

    @classmethod
    def de_json(cls, data):
        data = data.copy()
        return {camel_to_underscore(x): data[x] for x in data}

    @classmethod
    def de_list(cls, data):
        if not data:
            return []
        return [cls.de_json(obj) for obj in data]

    @staticmethod
    def _pretty_format(obj, indent=None):
        """Referenced from Telethon (https://github.com/LonamiWebs/Telethon/blob/master/telethon/tl/tlobject.py)"""
        if indent is None:
            return repr(obj)
        else:
            result = []
            if isinstance(obj, CRObject):
                obj = obj.to_dict(_pretty_format=True)
            if isinstance(obj, dict):
                result += [obj.get("_", "dict"), "("]
                if obj:
                    result.append("\n")
                    indent += 1
                    for k, v in obj.items():
                        if k != "_":
                            result += ["\t" * indent, k, "=", CRObject._pretty_format(v, indent), ",\n"]
                    result.pop()  # remove last ",\n"
                    indent -= 1
                    result += ["\n", "\t" * indent]
                result.append(")")
            elif isinstance(obj, (str, bytes)):
                result.append(repr(obj))
            elif hasattr(obj, "__iter__"):
                result.append("[\n")
                indent += 1
                for x in obj:
                    result += ["\t" * indent, CRObject._pretty_format(x, indent), ",\n"]
                indent -= 1
                result += ["\t" * indent, "]"]
            else:
                result.append(repr(obj))
            return "".join(result)
