import flet as ft
from flet.core.control_event import ControlEvent
from src.component.ui_components import (
    create_llm_provider_dropdown,
    create_llm_model_dropdown,
    create_api_key_field,
    create_browser_config_section,
    create_output_format_dropdown,
    create_submit_button,
)
from src.component.ui_buttons import create_stop_button
from src.layout.page_layout import create_page_content
from src.utility.event_handlers_llm import create_provider_changed_handler
from src.utility.event_handlers_execute import create_execute_button_handler
from src.layout.section.instruction_section import build_instruction_section
from src.layout.section.llm_section import build_llm_section
from src.layout.section.browser_section import build_browser_section
from src.layout.section.output_section import build_output_section
from src.layout.section.button_section import build_button_section
from src.layout.section.result_section import build_result_section
from src.component.ui_fields import create_output_dir_field
from src.component.ui_instruction import create_instruction_io_buttons

LLM_PROVIDERS = ["openrouter", "openai", "google"]
LLM_MODELS = {
    "openrouter": ["meta-llama/llama-4-maverick:free"],
    "openai": ["gpt-3.5-turbo", "gpt-4"],
    "google": ["gemini-2.0-flash", "gemini-2.0-pro"],
}


def setup_app(page: ft.Page):
    page.title = "Browser-Use Agent GUI"
    page.scroll = ft.ScrollMode.AUTO

    # --- セクションごとにUI構築 ---
    instruction = build_instruction_section(page)
    llm = build_llm_section(page)
    browser = build_browser_section()
    output = build_output_section()
    button = build_button_section()
    result = build_result_section()

    (
        common_instruction_field,
        purpose_field,
        detail_field,
        reference_url_field,
        data_item_controls,
        output_format_dropdown,
    ) = (
        instruction["common_instruction_field"],
        instruction["purpose_field"],
        instruction["detail_field"],
        instruction["reference_url_field"],
        instruction["data_item_controls"],
        instruction["output_format_dropdown"],
    )
    instruction_button_row = create_instruction_io_buttons(page)

    llm_provider_dropdown = llm["llm_provider_dropdown"]
    llm_model_dropdown = llm["llm_model_dropdown"]
    api_key_field = llm["api_key_field"]
    browser_config_row = browser["browser_config_row"]
    headless_checkbox = browser["headless_checkbox"]
    keep_alive_checkbox = browser["keep_alive_checkbox"]
    output_dir_row = output["output_dir_row"]
    submit_button = button["submit_button"]
    stop_button = button["stop_button"]
    progress_bar = button["progress_bar"]
    status_text = button["status_text"]
    result_text = result["result_text"]

    # --- LLMプロバイダー変更ハンドラ ---
    provider_changed = create_provider_changed_handler(
        llm_provider_dropdown, llm_model_dropdown, LLM_MODELS, page
    )
    llm_provider_dropdown.on_change = provider_changed

    def on_provider_change(e):
        selected_provider = llm_provider_dropdown.value
        models = (
            LLM_MODELS[selected_provider] if selected_provider in LLM_MODELS else []
        )
        llm_model_dropdown.options = [ft.dropdown.Option(model) for model in models]
        if llm_model_dropdown.options:
            llm_model_dropdown.value = llm_model_dropdown.options[0].key
            llm_model_dropdown.visible = True
        else:
            llm_model_dropdown.value = None
            llm_model_dropdown.visible = False
        if selected_provider:
            api_key_field.visible = True
            import os

            env_key = f"{selected_provider.upper()}_API_KEY"
            api_key_field.value = os.environ.get(env_key, "")
        else:
            api_key_field.visible = False
            api_key_field.value = ""
        page.update()

    llm_provider_dropdown.on_change = on_provider_change

    # --- 実行ボタンハンドラ ---
    button_clicked = create_execute_button_handler(
        page=page,
        purpose_field=purpose_field,
        detail_field=detail_field,
        reference_url_field=reference_url_field,
        llm_provider_dropdown=llm_provider_dropdown,
        llm_model_dropdown=llm_model_dropdown,
        api_key_field=api_key_field,
        headless_checkbox=headless_checkbox,
        keep_alive_checkbox=keep_alive_checkbox,
        output_format_dropdown=output_format_dropdown,
        output_dir_field=output_dir_row,
        progress_bar=progress_bar,
        status_text=status_text,
        result_text=result_text,
        data_item_controls=data_item_controls,
        submit_button=submit_button,
        stop_button=stop_button,
    )
    submit_button.on_click = button_clicked

    # --- ページレイアウト構築 ---
    page_content = create_page_content(
        title="Browser-Use Agent GUI",
        subtitle="AIエージェントのインストラクションと設定",
        instruction_section=[
            ft.Row(
                [
                    ft.Text("インストラクション", size=20, weight=ft.FontWeight.BOLD),
                    instruction_button_row,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            common_instruction_field,
            purpose_field,
            detail_field,
            reference_url_field,
            data_item_controls,
            output_format_dropdown,
        ],
        llm_section=[llm_provider_dropdown, llm_model_dropdown, api_key_field],
        browser_section=[browser_config_row],
        output_section=[output_dir_row],
        button_section=[submit_button, stop_button, progress_bar, status_text],
        result_section=[result_text],
    )
    page.add(page_content)
