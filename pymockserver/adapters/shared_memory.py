from collections.abc import Iterable
from typing import Any

# The mock store is a plain dict, not a `multiprocessing.Manager` dict. This
# is safe *only* because the app runs as a single uvicorn process with a
# single asyncio event loop and every route handler that touches the store
# is `async def` (never a plain `def`, which Starlette would run in a
# thread pool). Under those conditions, a coroutine only yields control at
# an `await`, and the hot path that reads/matches/decrements/deletes mocks
# (see `pymockserver/domain/response.py::retrieve_matching_response`)
# contains no `await` points, so it always runs atomically with respect to
# every other in-flight request - no locking needed. If a real OS thread
# (or a `def` handler) were ever introduced to touch this store, this
# assumption would break and explicit locking would be required again.
shared_memory: dict[str, Any] = {}


class Db:
    _cache: dict[str, Any]

    def __init__(self) -> None:
        self._cache = shared_memory

    @property
    def cache(self) -> dict[str, Any]:
        return self._cache

    def connect(self) -> dict[str, Any]:
        return self.cache

    def close(self) -> None:
        self.clear()

    def get(self, key: str) -> Any | None:
        return self.cache.get(key, None)

    def all(self) -> Iterable[Any]:
        yield from self.cache.items()

    def set(self, key: str, value: Any) -> Any:
        self.cache[key] = value
        return value

    def delete(self, key: str) -> Any | None:
        return self.cache.pop(key, None)

    def clear(self) -> None:
        self.cache.clear()


db = Db()
