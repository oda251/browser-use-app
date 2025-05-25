import flet as ft
from flet.core.control_event import ControlEvent
from src.component.ui_components import (
    create_purpose_field,
    create_detail_field,
    create_reference_url_field,
    create_data_item_controls,
    create_common_instruction_field,
)


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
        page.update()
        last_row = data_item_controls.controls[-1]
        if isinstance(last_row, ft.Row) and len(last_row.controls) > 0:
            last_control = last_row.controls[-1]
            if isinstance(last_control, ft.TextField):
                last_control.focus()

    data_item_controls = create_data_item_controls(data_items, on_data_item_submit)
    return {
        "data_item_controls": data_item_controls,
        "purpose_field": purpose_field,
        "detail_field": detail_field,
        "reference_url_field": reference_url_field,
        "common_instruction_field": common_instruction_field,
    }
