from cachetools import Cache

global_cache = Cache(maxsize=32)


def set_global(key, value):
    global global_cache
    global_cache[key] = value


def get_global(key):
    global global_cache
    return global_cache.get(key)
