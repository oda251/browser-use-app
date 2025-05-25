import flet as ft
from flet.core.control_event import ControlEvent
from src.component.ui_components import (
    create_purpose_field,
    create_detail_field,
    create_reference_url_field,
    create_data_item_controls,
    create_common_instruction_field,
    create_output_format_dropdown,
)

from src.global_cache import cache, CacheKey


def build_instruction_section(page: ft.Page):
    # --- 各フィールド生成 ---
    purpose_field = create_purpose_field()
    detail_field = create_detail_field()
    reference_url_field = create_reference_url_field()
    common_instruction_field = create_common_instruction_field()
    output_format_dropdown = create_output_format_dropdown()
    data_items = [""]
    data_item_controls = ft.Column()

    # --- cache保存用ハンドラ ---
    def cache_on_change(field, key):
        def handler(e):
            cache.set(key, field.value)

        return handler

    # --- データ項目入力のsubmitハンドラ ---
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
        cache.set(CacheKey.DATA_ITEMS, data_items)
        page.update()
        last_row = data_item_controls.controls[-1]
        if isinstance(last_row, ft.Row) and len(last_row.controls) > 0:
            last_control = last_row.controls[-1]
            if isinstance(last_control, ft.TextField):
                last_control.focus()

    # --- 各フィールドon_changeにcache保存を設定 ---
    purpose_field.on_change = cache_on_change(purpose_field, CacheKey.PURPOSE)
    detail_field.on_change = cache_on_change(detail_field, CacheKey.DETAIL)
    reference_url_field.on_change = cache_on_change(
        reference_url_field, CacheKey.REFERENCE_URL
    )
    common_instruction_field.on_change = cache_on_change(
        common_instruction_field, CacheKey.COMMON_INSTRUCTION
    )
    if output_format_dropdown:
        output_format_dropdown.on_change = cache_on_change(
            output_format_dropdown, CacheKey.OUTPUT_FORMAT
        )

    # --- データ項目コントロール初期化 ---
    data_item_controls = create_data_item_controls(data_items, on_data_item_submit)

    # --- fieldsリスト構築 ---
    fields = [
        common_instruction_field,
        purpose_field,
        detail_field,
        reference_url_field,
        data_item_controls,
    ]
    if output_format_dropdown:
        fields.append(output_format_dropdown)

    return {
        "fields": fields,
        "data_item_controls": data_item_controls,
        "purpose_field": purpose_field,
        "detail_field": detail_field,
        "reference_url_field": reference_url_field,
        "common_instruction_field": common_instruction_field,
        "output_format_dropdown": output_format_dropdown,
    }
