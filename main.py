from dotenv import load_dotenv
import flet as ft

from src.conponent.ui_components import (
    create_instruction_field,
    create_llm_provider_dropdown,
    create_llm_model_dropdown,
    create_api_key_field,
    create_browser_config_section,
    create_controller_type_checkboxes,
    create_output_dir_field,
    create_submit_button,
)
from src.conponent.page_layout import create_page_content
from src.utility.event_handlers import (
    create_provider_changed_handler,
    create_execute_button_handler,
)

# 環境変数の読み込み
load_dotenv()

# LLMプロバイダーのオプション
LLM_PROVIDERS = ["openrouter", "openai", "google"]

# LLMモデル（プロバイダーごと）
LLM_MODELS = {
    "openrouter": ["meta-llama/llama-4-maverick:free"],
    "openai": ["gpt-3.5-turbo", "gpt-4"],
    "google": ["gemini-2.0-flash", "gemini-2.0-pro"],
}


def main(page: ft.Page):
    # ページの設定
    page.title = "Browser-Use Agent GUI"
    page.scroll = "auto"

    # UI要素の作成
    instruction_field = create_instruction_field()

    llm_provider_dropdown = create_llm_provider_dropdown(LLM_PROVIDERS)
    # LLMモデル欄は最初は非表示
    llm_model_dropdown = create_llm_model_dropdown()
    llm_model_dropdown.visible = False
    # APIキー欄は最初は非表示
    api_key_field = create_api_key_field(visible=False)

    headless_checkbox = create_browser_config_section()

    controller_type_checkboxes = create_controller_type_checkboxes()

    output_dir_field = create_output_dir_field()

    # 進行状況表示用のコンポーネント
    progress_bar = ft.ProgressBar(width=600, visible=False)
    status_text = ft.Text("", size=16)
    result_text = ft.Text("", size=16)

    # イベントハンドラの設定
    provider_changed = create_provider_changed_handler(
        llm_provider_dropdown, llm_model_dropdown, LLM_MODELS, page
    )
    llm_provider_dropdown.on_change = provider_changed

    def on_provider_change(e):
        selected_provider = llm_provider_dropdown.value
        # モデルの選択肢を更新
        llm_model_dropdown.options = [
            ft.dropdown.Option(model)
            for model in LLM_MODELS.get(selected_provider, [])
        ]
        if llm_model_dropdown.options:
            llm_model_dropdown.value = llm_model_dropdown.options[0].key
            llm_model_dropdown.visible = True
        else:
            llm_model_dropdown.value = None
            llm_model_dropdown.visible = False
        # APIキー欄の表示・値を切り替え
        if selected_provider:
            api_key_field.visible = True
            env_key = f"{selected_provider.upper()}_API_KEY"
            import os

            api_key_field.value = os.environ.get(env_key, "")
        else:
            api_key_field.visible = False
            api_key_field.value = ""
        page.update()

    llm_provider_dropdown.on_change = on_provider_change

    button_clicked = create_execute_button_handler(
        page=page,
        instruction_field=instruction_field,
        llm_provider_dropdown=llm_provider_dropdown,
        llm_model_dropdown=llm_model_dropdown,
        api_key_field=api_key_field,
        headless_checkbox=headless_checkbox,
        controller_type_checkboxes=controller_type_checkboxes,
        output_dir_field=output_dir_field,
        progress_bar=progress_bar,
        status_text=status_text,
        result_text=result_text,
    )

    # 実行ボタン
    submit_button = create_submit_button()
    submit_button.on_click = button_clicked

    # ページコンテンツの構築
    page_content = create_page_content(
        title="Browser-Use Agent GUI",
        subtitle="AIエージェントのインストラクションと設定",
        instruction_section=[instruction_field],
        llm_section=[llm_provider_dropdown, llm_model_dropdown, api_key_field],
        browser_section=[headless_checkbox],
        controller_section=[controller_type_checkboxes],
        output_section=[output_dir_field],
        button_section=[submit_button, progress_bar, status_text],
        result_section=[result_text],
    )

    # ページにコンテンツを追加
    page.add(page_content)


# アプリケーションを実行
ft.app(target=main)
