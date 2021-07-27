from multiprocessing import Manager
from threading import Lock
from typing import Any, Iterable, Optional

manager = Manager()
shared_memory: dict[str, Any] = manager.dict()
lock: Lock = manager.Lock()


class Db:
    _cache: dict[str, Any]
    _lock: Lock

    def __init__(self) -> None:
        self._cache = shared_memory
        self._lock = lock

    @property
    def cache(self) -> dict[str, Any]:
        return self._cache

    def connect(self) -> dict[str, Any]:
        return self.cache

    def close(self) -> None:
        self.clear()

    def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key, None)

    def all(self) -> Iterable[Any]:
        for key, value in self.cache.items():
            yield key, value

    def set(self, key: str, value: Any) -> Any:
        lock.acquire()
        self.cache[key] = value
        lock.release()
        return value

    def delete(self, key: str) -> Optional[Any]:
        return self.cache.pop(key, None)

    def clear(self) -> None:
        self.cache.clear()


db = Db()
