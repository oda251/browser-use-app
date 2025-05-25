from operator import ge
from turtle import bgcolor, fillcolor
from src.entity.controller_type import OutputFormat
from src.entity.agent_context import AgentContext
from src.entity.prompt_templates import (
    COMMON_INSTRUCTION_DEFAULT,
    INITIAL_MARKDOWN_OUTPUT_PROMPT,
    RECURRING_MARKDOWN_OUTPUT_PROMPT,
    INITIAL_JSON_OUTPUT_PROMPT,
    RECURRING_JSON_OUTPUT_PROMPT,
    RECURRING_JSON_DATA_COLLECTION_RULE,
    INITIAL_TEXT_OUTPUT_PROMPT,
    RECURRING_TEXT_OUTPUT_PROMPT,
    LINK_FOLLOWING_RULE,
)
import flet as ft
import json
from src.entity.instruction_db import InstructionDB


def compose_instruction(
    purpose: str,
    detail: str,
    reference_url: str | None,
    controller_type: OutputFormat | None,
    data_items: list[str] | None = None,
    common_instruction: str | None = None,
) -> tuple[str, str, AgentContext]:
    parts_main = []
    parts_context = []
    context = AgentContext()
    # 共通指示
    if common_instruction and common_instruction.strip():
        parts_main.append(f"[Common Instruction]\n{common_instruction.strip()}")
        parts_context.append(f"[Common Instruction]\n{common_instruction.strip()}")
    # 目的
    if purpose:
        parts_main.append(f"[Purpose]\n{purpose}")
        parts_context.append(f"[Purpose]\n{purpose}")
    # 詳細
    if detail:
        parts_main.append(f"[Detail]\n{detail}")
        parts_context.append(f"[Detail]\n{detail}")
    # 参考URL
    if reference_url:
        parts_main.append(f"[Reference URL]\n{reference_url}")
        parts_context.append(f"[Reference URL]\n{reference_url}")
    # データ項目
    filtered = [item for item in (data_items or []) if item.strip() != ""]
    if filtered:
        data_items_str = "[Data Items]\n- " + "\n- ".join(filtered)
        parts_main.append(data_items_str)
        parts_context.append(data_items_str)
    # 出力形式
    if controller_type:
        match controller_type:
            case OutputFormat.MARKDOWN:
                parts_main.append(INITIAL_MARKDOWN_OUTPUT_PROMPT)
                parts_context.append(RECURRING_MARKDOWN_OUTPUT_PROMPT)
            case OutputFormat.CSV:
                parts_main.append(INITIAL_JSON_OUTPUT_PROMPT)
                parts_context.append(RECURRING_JSON_OUTPUT_PROMPT)
                parts_context.append(RECURRING_JSON_DATA_COLLECTION_RULE)
            case OutputFormat.TEXT:
                parts_main.append(INITIAL_TEXT_OUTPUT_PROMPT)
                parts_context.append(RECURRING_TEXT_OUTPUT_PROMPT)
            case _:
                other_rule = f"[Output Format Rule]\nSave as a file in {controller_type.value} format."
                parts_main.append(
                    f"[Output Format]\nSave as a file in {controller_type.value} format."
                )
                parts_context.append(other_rule)
    # --- ここで必ずリンク探索ルールを追加 ---
    parts_context.append(LINK_FOLLOWING_RULE)
    return "\n\n".join(parts_main), "\n\n".join(parts_context), context

from src.component.common.custom_fields import CustomDropdown
from src.theme.color import get_highlight_low
def create_instruction_dropdown_and_io(
    page: ft.Page, instruction
):
    """
    インストラクションのインポート/エクスポートボタン群を返す。
    戻り値: button_row
    """
    db = InstructionDB()
    db.ensure_default("デフォルト", COMMON_INSTRUCTION_DEFAULT)
    instructions = db.get_instructions()
    options = [ft.dropdown.Option(str(i[1]), str(i[0])) for i in instructions]
    dropdown = CustomDropdown(
        label="テンプレート",
        width=140,
        item_height=50,
        options=options,
        value=options[0].key if options else None,
        text_size=12,
        bgcolor=get_highlight_low(),
        fill_color=get_highlight_low(),
    )
    # FilePicker
    file_picker = ft.FilePicker()

    def on_dropdown_change(e):
        None

    dropdown.on_change = on_dropdown_change

    # インポート
    def on_import_result(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data:
                    db.add_instruction(
                        item.get("name", "インポート"), item.get("content", "")
                    )
                new_instructions = db.get_instructions()
                dropdown.options = [
                    ft.dropdown.Option(str(i[1]), str(i[0])) for i in new_instructions
                ]
                dropdown.value = dropdown.options[0].key if dropdown.options else None
                dropdown.update()
            except Exception as ex:
                # エラー時はドロップダウンのラベルを一時的に変更
                dropdown.label = f"インポート失敗: {ex}"
                dropdown.update()

    file_picker.on_result = on_import_result
    import_button = ft.IconButton(
        icon=ft.Icons.FILE_DOWNLOAD,
        tooltip="インストラクションをインポート(JSON)",
        on_click=lambda e: file_picker.pick_files(
            allow_multiple=False, allowed_extensions=["json"]
        ),
        icon_size=20,
    )

    # エクスポート
    def on_export_click(e):
        all_instructions = db.get_instructions()
        export_data = [{"name": rec[1], "content": rec[2]} for rec in all_instructions]
        export_json = json.dumps(export_data, ensure_ascii=False, indent=2)
        dropdown.label = "エクスポート内容をコピーしてください"
        dropdown.value = None
        dropdown.options = dropdown.options  # 強制update
        dropdown.update()
        page.open(
            ft.SnackBar(
                content=ft.Text(
                    "エクスポート内容をクリップボード等にコピーしてください。"
                ),
                open=True,
            )
        )
        page.update()

    export_button = ft.IconButton(
        icon=ft.Icons.FILE_UPLOAD,
        tooltip="インストラクションをエクスポート(JSON)",
        on_click=on_export_click,
        icon_size=20,
    )
    button_row = ft.Row(
        [export_button, import_button, dropdown, file_picker],
        spacing=8,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return button_row
