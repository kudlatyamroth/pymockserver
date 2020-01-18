from pathlib import Path

from diskcache import Cache


class Db:
    _cache: Cache = None
    _dick_settings = {
        "disk_pickle_protocol": 4,
        "cull_limit": 0,
        "eviction_policy": "none",
    }

    @property
    def cache(self):
        if not self._cache:
            self._cache = Cache(str(Path(__file__).parent), **self._dick_settings)
        return self._cache

    def connect(self):
        return self.cache

    def close(self):
        self.clear()
        self.cache.close()

    def get(self, key):
        return self.cache.get(key)

    def all(self):
        for key in self.cache.iterkeys():
            yield key, self.get(key)

    def set(self, key, value):
        self.cache.set(key, value)
        return value

    def delete(self, key):
        return self.cache.pop(key, None)

    def clear(self):
        self.cache.clear()


db = Db()
