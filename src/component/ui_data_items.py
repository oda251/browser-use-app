import flet as ft
from src.component.common.custom_fields import CustomTextField


def create_data_item_controls(data_items: list[str], on_submit) -> ft.Column:
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
    # 1行に3つまで、それを超える分は次のRowへ
    rows = []
    for i in range(0, len(fields), 3):
        rows.append(ft.Row(controls=fields[i : i + 3], spacing=9))
    return ft.Column(controls=rows, spacing=6)


def extract_data_items(column: ft.Column) -> list[str]:
    items = []
    for row in column.controls:
        if isinstance(row, ft.Row):
            for f in row.controls:
                if (
                    isinstance(f, CustomTextField)
                    and f.value is not None
                    and f.value.strip() != ""
                ):
                    items.append(f.value)
    return items
