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


def create_instruction_io_buttons(page: ft.Page):
    """
    インストラクションのインポート/エクスポートボタン群を返す。
    戻り値: button_row
    """
    # FilePicker
    file_picker = ft.FilePicker()

    # インポート
    def on_import_result(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            file_path = e.files[0].path
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # ここでインポートデータを必要に応じて処理
                page.open(
                    ft.SnackBar(
                        content=ft.Text("インポート成功: ファイルを読み込みました。"),
                        open=True,
                    )
                )
            except Exception as ex:
                page.open(
                    ft.SnackBar(
                        content=ft.Text(f"インポート失敗: {ex}"),
                        open=True,
                    )
                )
            page.update()

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
        # ここでエクスポートデータを必要に応じて生成
        export_json = json.dumps([], ensure_ascii=False, indent=2)
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
        [export_button, import_button, file_picker],
        spacing=8,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return button_row
