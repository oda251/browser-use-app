from dotenv import load_dotenv
import flet as ft

from src.conponent.ui_components import (
    create_purpose_field,
    create_detail_field,
    create_reference_url_field,
    create_llm_provider_dropdown,
    create_llm_model_dropdown,
    create_api_key_field,
    create_browser_config_section,
    create_output_format_dropdown,
    create_output_dir_field,
    create_submit_button,
    create_data_items_row,
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
    page.scroll = ft.ScrollMode.AUTO

    # UI要素の作成
    purpose_field = create_purpose_field()
    detail_field = create_detail_field()
    reference_url_field = create_reference_url_field()
    output_format_dropdown = create_output_format_dropdown()

    llm_provider_dropdown = create_llm_provider_dropdown(LLM_PROVIDERS)
    # LLMモデル欄は最初は非表示
    llm_model_dropdown = create_llm_model_dropdown()
    llm_model_dropdown.visible = False
    # APIキー欄は最初は非表示
    api_key_field = create_api_key_field(visible=False)

    browser_config_row = create_browser_config_section()
    headless_checkbox = browser_config_row.controls[0]
    keep_alive_checkbox = browser_config_row.controls[1]

    output_dir_field = create_output_dir_field()

    # 進行状況表示用のコンポーネント
    progress_bar = ft.ProgressBar(width=600, visible=False)
    status_text = ft.Text("", size=16)
    result_text = ft.Text("", size=16)

    # データ項目の状態管理
    data_items = [""]
    data_items_row = None  # 後で初期化

    def on_data_item_change(e, idx):
        nonlocal data_items, data_items_row
        value = e.control.value
        # 入力値を更新
        if idx < len(data_items):
            data_items[idx] = value
        else:
            data_items.append(value)
        # 空欄を除外し、最後が空でなければ空欄を追加
        data_items = [v for v in data_items]
        if not data_items or data_items[-1] != "":
            data_items.append("")
        # Rowを再生成
        data_items_row.controls = create_data_items_row(
            data_items, on_data_item_change
        ).controls
        page.update()

    # 初期Row生成
    data_items_row = create_data_items_row(data_items, on_data_item_change)

    # イベントハンドラの設定
    provider_changed = create_provider_changed_handler(
        llm_provider_dropdown, llm_model_dropdown, LLM_MODELS, page
    )
    llm_provider_dropdown.on_change = provider_changed

    def on_provider_change(e):
        selected_provider = llm_provider_dropdown.value
        # モデルの選択肢を更新
        llm_model_dropdown.options = [
            ft.dropdown.Option(model) for model in LLM_MODELS.get(selected_provider, [])
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
        purpose_field=purpose_field,
        detail_field=detail_field,
        reference_url_field=reference_url_field,
        llm_provider_dropdown=llm_provider_dropdown,
        llm_model_dropdown=llm_model_dropdown,
        api_key_field=api_key_field,
        headless_checkbox=headless_checkbox,
        keep_alive_checkbox=keep_alive_checkbox,  # 追加
        output_format_dropdown=output_format_dropdown,
        output_dir_field=output_dir_field,
        progress_bar=progress_bar,
        status_text=status_text,
        result_text=result_text,
        data_items_row=data_items_row,
    )

    # 実行ボタン
    submit_button = create_submit_button()
    submit_button.on_click = button_clicked

    # ページコンテンツの構築
    page_content = create_page_content(
        title="Browser-Use Agent GUI",
        subtitle="AIエージェントのインストラクションと設定",
        instruction_section=[
            purpose_field,
            detail_field,
            reference_url_field,
            output_format_dropdown,
            data_items_row=data_items_row,
        ],
        llm_section=[llm_provider_dropdown, llm_model_dropdown, api_key_field],
        browser_section=[browser_config_row],
        controller_section=[],
        output_section=[output_dir_field],
        button_section=[submit_button, progress_bar, status_text],
        result_section=[result_text],
    )

    # ページにコンテンツを追加
    page.add(page_content)


# アプリケーションを実行
ft.app(target=main)
