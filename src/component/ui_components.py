import flet as ft
from typing import List
import os
from src.entity.controller_type import OutputFormat
from src.component.common.custom_fields import CustomDropdown

# 各種UI生成関数を分割ファイルからインポート
from .ui_fields import (
    create_instruction_field,
    create_purpose_field,
    create_detail_field,
    create_reference_url_field,
    create_api_key_field,
    create_output_dir_field,
    create_common_instruction_field,
)
from .ui_dropdowns import (
    create_llm_provider_dropdown,
    create_llm_model_dropdown,
    create_output_format_dropdown,
)
from .ui_data_items import (
    create_data_item_controls,
    extract_data_items,
)
from .ui_instruction import compose_instruction
from .ui_buttons import create_submit_button
from .ui_fields import create_browser_config_section


def create_llm_provider_dropdown(providers: List[str]) -> ft.Dropdown:
    """
    LLMプロバイダーを選択するためのドロップダウンを作成します
    """
    return CustomDropdown(
        label="LLMプロバイダー",
        width=600,
        options=[ft.dropdown.Option(provider) for provider in providers],
    )


def create_llm_model_dropdown() -> ft.Dropdown:
    """
    LLMモデルを選択するためのドロップダウンを作成します
    """
    return CustomDropdown(
        label="LLMモデル",
        width=600,
        options=[],  # オプションは動的に設定されます
    )


def create_browser_config_section() -> ft.Column:
    """
    ブラウザの設定を行うためのチェックボックス群を作成します
    """
    headless_checkbox = ft.Checkbox(
        label="ヘッドレスモード（ブラウザを表示せずに実行）",
        value=False,
    )
    keep_alive_checkbox = ft.Checkbox(
        label="keep-alive（ブラウザプロセスを維持）",
        value=True,
    )
    return ft.Column(controls=[headless_checkbox, keep_alive_checkbox], spacing=20)


def create_output_format_dropdown() -> ft.Dropdown:
    """
    出力形式を選択するためのドロップダウンを作成します
    """
    from src.entity.controller_type import OutputFormat

    return CustomDropdown(
        label="出力形式",
        width=600,
        options=[ft.dropdown.Option(fmt.value) for fmt in OutputFormat],
        value=OutputFormat.MARKDOWN.value,
    )


def create_submit_button() -> ft.ElevatedButton:
    """
    実行ボタンを作成します
    """
    return ft.ElevatedButton(
        text="エージェントを実行",
        width=600,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
        ),
        icon=ft.Icons.PLAY_ARROW,
    )


def compose_instruction(
    purpose: str,
    detail: str,
    reference_url: str | None,
    controller_type: OutputFormat | None,
    data_items: list[str] | None = None,
    common_instruction: str | None = None,
) -> str:
    """
    目的・詳細・参考URL・データ項目・出力形式から自然な指示文を生成します。
    空欄は無視し、必要な部分のみを含めます。
    """
    parts = []
    if common_instruction and common_instruction.strip():
        parts.append(f"【共通指示】\n{common_instruction.strip()}")
    if purpose:
        parts.append(f"【目的】\n{purpose}")
    if detail:
        parts.append(f"【詳細】\n{detail}")
    if reference_url:
        parts.append(f"【参考URL】\n{reference_url}")
    if data_items:
        filtered = [item for item in data_items if item.strip() != ""]
        if filtered:
            parts.append("【データ項目】\n- " + "\n- ".join(filtered))
    if controller_type:
        match controller_type:
            case OutputFormat.MARKDOWN:
                parts.append(
                    "【出力形式】\n出力は見やすく構造化されたMarkdown形式で作成してください。必要に応じて見出しやリスト、テーブルを活用し、情報を整理してください。ファイルとして保存してください。"
                )
            case OutputFormat.CSV:
                parts.append(
                    """【出力形式】
出力はCSV形式で作成してください。カラム名は上記データ項目に従い、各行のデータがカラムと正しく対応するようにしてください。カラム名は1行目に記載し、データは2行目以降に記載してください。ファイルとして保存してください。"""
                )
            case OutputFormat.TEXT:
                parts.append(
                    "【出力形式】\n出力はプレーンテキスト形式で作成してください。必要に応じて改行やインデントで情報を整理してください。ファイルとして保存してください。"
                )
    return "\n\n".join(parts)
