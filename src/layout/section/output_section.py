import flet as ft
from src.component.ui_fields import create_output_dir_field
from src.global_cache import cache
from src.entity.input_values import OutputInputKey


def build_output_section():
    output_dir_row = create_output_dir_field()
    # output_dir_row.controls[0]がCustomTextField想定
    text_field = output_dir_row.controls[0] if output_dir_row.controls else None

    def cache_on_change(field, key):
        def handler(e):
            cache.set(key.value, field.value)

        return handler

    # FletのTextFieldはon_change属性を持つ
    if text_field and hasattr(text_field, "on_change"):
        setattr(
            text_field,
            "on_change",
            cache_on_change(text_field, OutputInputKey.OUTPUT_DIR),
        )
    return {"output_dir_row": output_dir_row}
