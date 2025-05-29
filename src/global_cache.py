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
    OUTPUT_FORMAT = "output_format"


class GlobalCache:
    def __init__(self):
        self.cache = Cache(maxsize=32)

    def set(self, key: CacheKey | str, value) -> None:
        if isinstance(key, CacheKey):
            key = key.value
        self.cache[key] = value

    def get(self, key: CacheKey | str, default: T) -> T:
        if isinstance(key, CacheKey):
            key = key.value
        val = self.cache.get(key, default)
        return cast(T, val)


cache = GlobalCache()
