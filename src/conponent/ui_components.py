import flet as ft
from typing import List
import os


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


def create_controller_type_checkboxes() -> ft.Row:
    """
    コントローラータイプを選択するためのチェックボックスグループを作成します
    """
    from src.entity.controller_type import ControllerType

    return ft.Row(
        controls=[
            ft.Checkbox(
                label=ct.value, value=True if ct == ControllerType.MARKDOWN else False
            )
            for ct in ControllerType
        ],
        wrap=True,
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
