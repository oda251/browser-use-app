import flet as ft
import os
from src.component.common.custom_fields import CustomTextField
from src.entity.prompt_templates import COMMON_INSTRUCTION_DEFAULT


def create_instruction_field() -> ft.TextField:
    return CustomTextField(
        label="インストラクション",
        hint_text="Agentに実行させたい指示を入力してください",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=600,
    )


def _expand_lines(e, min_lines, max_lines):
    field = e.control
    field.min_lines = min_lines
    field.max_lines = max_lines
    field.update()


def create_purpose_field() -> ft.TextField:
    field = CustomTextField(
        label="目的",
        hint_text="Agentに実行させたい目的を入力してください",
        multiline=True,
        min_lines=1,
        max_lines=2,
        width=600,
    )
    field.on_focus = lambda e: _expand_lines(e, 2, 6)
    field.on_blur = lambda e: _expand_lines(e, 1, 1)
    return field


def create_detail_field() -> ft.TextField:
    field = CustomTextField(
        label="詳細",
        hint_text="タスクの詳細や条件などを入力してください",
        multiline=True,
        width=600,
    )
    field.on_focus = lambda e: _expand_lines(e, 5, 15)
    field.on_blur = lambda e: _expand_lines(e, 1, 1)
    return field


def create_reference_url_field() -> ft.TextField:
    return CustomTextField(
        label="参考URL",
        hint_text="参考となるURLがあれば入力してください（任意）",
        multiline=False,
        width=600,
    )


def create_api_key_field(provider: str, visible: bool = True) -> ft.TextField:
    env_key = f"{provider.upper()}_API_KEY" if provider else "OPENAI_API_KEY"
    default_value = os.environ.get(env_key, "")
    return CustomTextField(
        label="APIキー",
        hint_text="環境変数が設定されている場合は空のままでもOK",
        password=True,
        can_reveal_password=True,
        width=600,
        value=default_value,
        visible=visible,
    )


def create_output_dir_field() -> ft.TextField:
    return CustomTextField(
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


def create_common_instruction_field() -> ft.TextField:
    field = CustomTextField(
        label="共通指示",
        hint_text="毎回共通でAgentに伝えたい指示",
        multiline=True,
        min_lines=1,
        max_lines=1,
        width=600,
        value=COMMON_INSTRUCTION_DEFAULT,
        visible=True,
    )
    field.on_focus = lambda e: _expand_lines(e, 3, 10)
    field.on_blur = lambda e: _expand_lines(e, 1, 1)
    return field
