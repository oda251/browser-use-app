import flet as ft
from src.component.common.custom_fields import CustomTextField


def create_data_items_row(data_items: list[str], on_submit) -> ft.Row:
    fields = []
    for i, value in enumerate(data_items):
        fields.append(
            CustomTextField(
                label=f"データ項目{i+1}",
                value=value,
                width=194,
                on_submit=lambda e, idx=i: on_submit(e, idx),
            )
        )
    if not data_items or data_items[-1] != "":
        fields.append(
            CustomTextField(
                label=f"データ項目{len(data_items)+1}",
                value="",
                width=194,
                on_submit=lambda e, idx=len(data_items): on_submit(e, idx),
            )
        )
    return ft.Row(controls=fields, spacing=9)


def get_data_items_from_row(row: ft.Row) -> list[str]:
    return [
        f.value
        for f in row.controls
        if isinstance(f, CustomTextField)
        and f.value is not None
        and f.value.strip() != ""
    ]
