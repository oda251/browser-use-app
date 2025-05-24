import flet as ft
from flet.core.control_event import ControlEvent
from src.conponent.ui_components import (
    create_purpose_field,
    create_detail_field,
    create_reference_url_field,
    create_data_items_row,
    create_common_instruction_field,
)


def build_instruction_section(page: ft.Page):
    purpose_field = create_purpose_field()
    detail_field = create_detail_field()
    reference_url_field = create_reference_url_field()
    data_items = [""]
    data_items_row = ft.Row()
    common_instruction_field = create_common_instruction_field()

    def on_data_item_submit(e: ControlEvent, idx):
        nonlocal data_items, data_items_row
        value = e.control.value
        if idx < len(data_items):
            data_items[idx] = value
        else:
            data_items.append(value)
        data_items = [v for v in data_items]
        if not data_items or data_items[-1] != "":
            data_items.append("")
        data_items_row.controls = create_data_items_row(
            data_items, on_data_item_submit
        ).controls
        page.update()
        data_items_row.controls[-1].focus()

    data_items_row = create_data_items_row(data_items, on_data_item_submit)
    return {
        "fields": [
            common_instruction_field,
            purpose_field,
            detail_field,
            reference_url_field,
            data_items_row,
        ],
        "data_items_row": data_items_row,
        "purpose_field": purpose_field,
        "detail_field": detail_field,
        "reference_url_field": reference_url_field,
        "common_instruction_field": common_instruction_field,
    }
