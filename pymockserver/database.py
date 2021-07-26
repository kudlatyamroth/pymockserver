from pathlib import Path
from typing import Any, Iterable, Optional

from diskcache import Cache

DEFAULT_DB_DIR = "/data/sqlite"
DB_DIR = DEFAULT_DB_DIR if Path(DEFAULT_DB_DIR).is_dir() else None


class Db:
    _cache: Cache = None
    _disk_settings = {
        "disk_pickle_protocol": 4,
        "cull_limit": 0,
        "eviction_policy": "none",
    }

    @property
    def cache(self) -> Cache:
        if self._cache is None:
            self._cache = Cache(DB_DIR, **self._disk_settings)
        return self._cache

    def connect(self) -> Cache:
        return self.cache

    def close(self) -> None:
        self.clear()
        self.cache.close()

    def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key)

    def all(self) -> Iterable[Any]:
        for key in self.cache.iterkeys():
            yield key, self.get(key)

    def set(self, key: str, value: Any) -> Any:
        self.cache.set(key, value)
        return value

    def delete(self, key: str) -> Optional[Any]:
        return self.cache.pop(key, None)

    def clear(self) -> None:
        self.cache.clear()


db = Db()
