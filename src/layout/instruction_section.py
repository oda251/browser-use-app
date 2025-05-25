import flet as ft
from flet.core.control_event import ControlEvent
from src.component.ui_components import (
    create_purpose_field,
    create_detail_field,
    create_reference_url_field,
    create_data_item_controls,
    create_common_instruction_field,
)
from src.global_cache import cache, CacheKey


def build_instruction_section(page: ft.Page):
    purpose_field = create_purpose_field()
    detail_field = create_detail_field()
    reference_url_field = create_reference_url_field()
    data_items = [""]
    data_item_controls = ft.Column()
    common_instruction_field = create_common_instruction_field()

    def on_data_item_submit(e: ControlEvent, idx):
        nonlocal data_items, data_item_controls
        value = e.control.value
        if idx < len(data_items):
            data_items[idx] = value
        else:
            data_items.append(value)
        data_items = [v for v in data_items]
        if not data_items or data_items[-1] != "":
            data_items.append("")
        data_item_controls.controls = create_data_item_controls(
            data_items, on_data_item_submit
        ).controls
        # --- cacheに保存 ---
        cache.set(CacheKey.DATA_ITEMS, data_items)
        page.update()
        last_row = data_item_controls.controls[-1]
        if isinstance(last_row, ft.Row) and len(last_row.controls) > 0:
            last_control = last_row.controls[-1]
            if isinstance(last_control, ft.TextField):
                last_control.focus()

    # --- 各フィールドのon_changeでcacheに保存 ---
    def cache_on_change(field, key):
        def handler(e):
            cache.set(key, field.value)

        return handler

    purpose_field.on_change = cache_on_change(purpose_field, CacheKey.PURPOSE)
    detail_field.on_change = cache_on_change(detail_field, CacheKey.DETAIL)
    reference_url_field.on_change = cache_on_change(
        reference_url_field, CacheKey.REFERENCE_URL
    )
    common_instruction_field.on_change = cache_on_change(
        common_instruction_field, CacheKey.COMMON_INSTRUCTION
    )

    data_item_controls = create_data_item_controls(data_items, on_data_item_submit)
    return {
        "fields": [
            common_instruction_field,
            purpose_field,
            detail_field,
            reference_url_field,
            data_item_controls,
        ],
        "data_item_controls": data_item_controls,
        "purpose_field": purpose_field,
        "detail_field": detail_field,
        "reference_url_field": reference_url_field,
        "common_instruction_field": common_instruction_field,
    }
