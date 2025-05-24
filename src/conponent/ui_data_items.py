import flet as ft


def create_data_items_row(data_items: list[str], on_change) -> ft.Row:
    fields = []
    for i, value in enumerate(data_items):
        fields.append(
            ft.TextField(
                label=f"データ項目{i+1}",
                value=value,
                width=200,
                on_change=lambda e, idx=i: on_change(e, idx),
            )
        )
    if not data_items or data_items[-1] != "":
        fields.append(
            ft.TextField(
                label=f"データ項目{len(data_items)+1}",
                value="",
                width=200,
                on_change=lambda e, idx=len(data_items): on_change(e, idx),
            )
        )
    return ft.Row(controls=fields, spacing=10)


def get_data_items_from_row(row: ft.Row) -> list[str]:
    return [
        f.value
        for f in row.controls
        if isinstance(f, ft.TextField) and f.value is not None and f.value.strip() != ""
    ]
