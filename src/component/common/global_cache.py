from cachetools import Cache

# シンプルなグローバルキャッシュ（必要に応じてサイズ調整）
global_cache = Cache(maxsize=32)


def set_global(key, value):
    global_cache[key] = value


def get_global(key, default=None):
    return global_cache.get(key, default)


def set_theme_mode(is_dark: bool):
    set_global("theme_mode", "dark" if is_dark else "light")


def get_theme_mode():
    return get_global("theme_mode", "light")
