from abc import ABCMeta
from typing import Dict, List, Any, TYPE_CHECKING

from royaleapi.utils import camel_to_snake

if TYPE_CHECKING:
    from royaleapi.client import RoyaleAPIClient


class CRObject(metaclass=ABCMeta):
    def __eq__(self, other: Any) -> bool:  # CRObjects that do not implement __eq__ fall back to this
        if self.__class__ is other.__class__:
            raise ValueError("The two objects are not comparable!")
        return NotImplemented

    def __getitem__(self, item: str) -> Any:
        return self.__dict__[item]

    def to_dict(self, _pretty_format: bool = False) -> Dict:
        if _pretty_format:
            return {**self.__dict__, "_": self.__class__.__name__}
        else:
            data = {}
            for k, v in self.__dict__.items():
                if k != "client" and v not in (None, []):
                    if isinstance(v, CRObject):
                        data[k] = v.to_dict()
                    elif isinstance(v, list):
                        data[k] = [i.to_dict() for i in v]
                    else:
                        data[k] = v
            return data

    def stringify(self) -> str:
        return CRObject._pretty_format(self)

    @classmethod
    def de_json(cls, data: Dict, client: "RoyaleAPIClient") -> Dict or "CRObject":
        return {camel_to_snake(x): data[x] for x in data.copy()}

    @classmethod
    def de_list(cls, data: List[Dict], client: "RoyaleAPIClient") -> List[Dict or "CRObject"]:
        return [] if not data else [cls.de_json(obj, client) for obj in ([data] if isinstance(data, dict) else data)]

    @staticmethod
    def _pretty_format(obj: Any, indent: int = 0) -> str:
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
