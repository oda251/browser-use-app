import flet as ft
import os


def create_instruction_field() -> ft.TextField:
    return ft.TextField(
        label="インストラクション",
        hint_text="Agentに実行させたい指示を入力してください",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=600,
    )


def create_purpose_field() -> ft.TextField:
    return ft.TextField(
        label="目的",
        hint_text="Agentに実行させたい目的を入力してください",
        multiline=True,
        min_lines=1,
        max_lines=2,
        width=600,
    )


def create_detail_field() -> ft.TextField:
    return ft.TextField(
        label="詳細",
        hint_text="タスクの詳細や条件などを入力してください",
        multiline=True,
        min_lines=2,
        max_lines=5,
        width=600,
    )


def create_reference_url_field() -> ft.TextField:
    return ft.TextField(
        label="参考URL",
        hint_text="参考となるURLがあれば入力してください（任意）",
        multiline=False,
        width=600,
    )


def create_api_key_field(provider: str, visible: bool = True) -> ft.TextField:
    env_key = f"{provider.upper()}_API_KEY" if provider else "OPENAI_API_KEY"
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


def create_output_dir_field() -> ft.TextField:
    return ft.TextField(
        label="出力ディレクトリ",
        hint_text="結果を保存するディレクトリ",
        width=600,
        value="output",
    )


def create_browser_config_section() -> ft.Column:
    headless_checkbox = ft.Checkbox(
        label="ヘッドレスモード（ブラウザを表示せずに実行）",
        value=False,
    )
    keep_alive_checkbox = ft.Checkbox(
        label="keep-alive（ブラウザプロセスを維持）",
        value=True,
    )
    return ft.Column(controls=[headless_checkbox, keep_alive_checkbox], spacing=20)
