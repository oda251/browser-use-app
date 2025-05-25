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
    # --- instruction関連 ---
    PURPOSE = "purpose"
    DETAIL = "detail"
    REFERENCE_URL = "reference_url"
    COMMON_INSTRUCTION = "common_instruction"
    DATA_ITEMS = "data_items"


class GlobalCache:
    def __init__(self):
        self.cache = Cache(maxsize=32)

    def set(self, key: CacheKey, value) -> None:
        self.cache[key.value] = value

    def get(self, key: CacheKey, default: T) -> T:
        val = self.cache.get(key.value, default)
        return cast(T, val)


cache = GlobalCache()
