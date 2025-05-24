import flet as ft
from typing import List
import os
from src.entity.controller_type import OutputFormat


def create_instruction_field() -> ft.TextField:
    """
    インストラクションを入力するためのテキストフィールドを作成します
    """
    return ft.TextField(
        label="インストラクション",
        hint_text="Agentに実行させたい指示を入力してください",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=600,
    )


def create_llm_provider_dropdown(providers: List[str]) -> ft.Dropdown:
    """
    LLMプロバイダーを選択するためのドロップダウンを作成します
    """
    return ft.Dropdown(
        label="LLMプロバイダー",
        width=600,
        options=[ft.dropdown.Option(provider) for provider in providers],
    )


def create_llm_model_dropdown() -> ft.Dropdown:
    """
    LLMモデルを選択するためのドロップダウンを作成します
    """
    return ft.Dropdown(
        label="LLMモデル",
        width=600,
        options=[],  # オプションは動的に設定されます
    )


def create_api_key_field(provider: str = None, visible: bool = True) -> ft.TextField:
    """
    APIキーを入力するためのテキストフィールドを作成します
    provider: プロバイダー名（例: 'openai', 'google', 'openrouter'）
    visible: 表示/非表示
    """
    env_key = None
    if provider:
        env_key = f"{provider.upper()}_API_KEY"
    else:
        env_key = "OPENAI_API_KEY"  # デフォルト
    default_value = os.environ.get(env_key, "")
    return ft.TextField(
        label="APIキー",
        hint_text="環境変数が設定されている場合は空のままでもOK",
        password=True,
        can_reveal_password=True,
        width=600,
        value=default_value,
        visible=visible,
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

    return ft.Dropdown(
        label="出力形式",
        width=600,
        options=[ft.dropdown.Option(fmt.value) for fmt in OutputFormat],
        value=OutputFormat.MARKDOWN.value,
    )


def create_output_dir_field() -> ft.TextField:
    """
    出力ディレクトリを入力するためのテキストフィールドを作成します
    """
    return ft.TextField(
        label="出力ディレクトリ",
        hint_text="結果を保存するディレクトリ",
        width=600,
        value="output",
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


def create_purpose_field() -> ft.TextField:
    """
    目的を入力するためのテキストフィールドを作成します
    """
    return ft.TextField(
        label="目的",
        hint_text="Agentに実行させたい目的を入力してください",
        multiline=True,
        min_lines=1,
        max_lines=2,
        width=600,
    )


def create_detail_field() -> ft.TextField:
    """
    詳細を入力するためのテキストフィールドを作成します
    """
    return ft.TextField(
        label="詳細",
        hint_text="タスクの詳細や条件などを入力してください",
        multiline=True,
        min_lines=2,
        max_lines=5,
        width=600,
    )


def create_reference_url_field() -> ft.TextField:
    """
    参考URLを入力するためのテキストフィールドを作成します
    """
    return ft.TextField(
        label="参考URL",
        hint_text="参考となるURLがあれば入力してください（任意）",
        multiline=False,
        width=600,
    )


def compose_instruction(
    purpose: str,
    detail: str,
    reference_url: str | None,
    controller_type: OutputFormat | None,
) -> str:
    """
    目的・詳細・参考URLから自然な指示文を生成します。
    空欄は無視し、必要な部分のみを含めます。
    """
    parts = []
    if purpose:
        parts.append(f"目的: {purpose}")
    if detail:
        parts.append(f"詳細: {detail}")
    if reference_url:
        parts.append(f"参考URL: {reference_url}")
    if controller_type:
        match controller_type:
            case OutputFormat.MARKDOWN:
                parts.append("出力形式: Markdown")
            case OutputFormat.CSV:
                parts.append("出力形式: CSV")
            case OutputFormat.TEXT:
                parts.append("出力形式: プレーンテキスト")
            case _:
                parts.append(f"出力形式: {controller_type.value}")
        parts.append("出力は指定された形式でファイルに保存してください。")
    return "\n".join(parts)
