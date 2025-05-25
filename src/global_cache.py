from cachetools import Cache
from enum import Enum
from typing import cast, TypeVar


T = TypeVar("T")


# キャッシュキーの列挙型
class CacheKey(Enum):
    RUNNING = "running"
    STOP = "stop"
    PAUSE = "pause"
    AGENT = "cache"


class GlobalCache:
    def __init__(self):
        self.cache = Cache(maxsize=32)

    def set(self, key: CacheKey, value) -> None:
        self.cache[key.value] = value

    def get(self, key: CacheKey, default: T) -> T:
        val = self.cache.get(key.value, default)
        return cast(T, val)


cache = GlobalCache()