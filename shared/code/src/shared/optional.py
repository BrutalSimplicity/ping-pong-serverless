
from typing import Generic, TypeVar

T = TypeVar('T')


class OptionalHandler(Generic[T]):
    def __init__(self, obj: T):
        self._src = obj

    def value(self):
        return self._src

    def __getitem__(self, key):
        if not self._src:
            return OptionalHandler(None)

        try:
            return OptionalHandler(self._src.get(key))
        except AttributeError:
            try:
                return OptionalHandler(self._src[key])
            except Exception:
                return OptionalHandler(None)

    def __getattr__(self, name: str):
        try:
            return OptionalHandler(object.__getattribute__(self._src, name))
        except AttributeError:
            return OptionalHandler(None)

    def __bool__(self):
        return bool(self._src)
