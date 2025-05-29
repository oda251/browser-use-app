import flet as ft
from src.component.ui_components import create_browser_config_section
from src.global_cache import cache
from src.entity.input_values import BrowserInputKey


def build_browser_section():
    browser_config_row = create_browser_config_section()
    headless_checkbox = (
        browser_config_row.controls[0]
        if isinstance(browser_config_row.controls[0], ft.Checkbox)
        else ft.Checkbox()
    )
    keep_alive_checkbox = (
        browser_config_row.controls[1]
        if isinstance(browser_config_row.controls[1], ft.Checkbox)
        else ft.Checkbox()
    )

    # on_changeでcache保存
    def cache_on_change(field, key):
        def handler(e):
            cache.set(key.value, field.value)

        return handler

    headless_checkbox.on_change = cache_on_change(
        headless_checkbox, BrowserInputKey.HEADLESS
    )
    keep_alive_checkbox.on_change = cache_on_change(
        keep_alive_checkbox, BrowserInputKey.KEEP_ALIVE
    )
    return {
        "browser_config_row": browser_config_row,
        "headless_checkbox": headless_checkbox,
        "keep_alive_checkbox": keep_alive_checkbox,
    }
