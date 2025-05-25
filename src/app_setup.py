import flet as ft
from flet.core.control_event import ControlEvent
from src.component.ui_components import (
    create_llm_provider_dropdown,
    create_llm_model_dropdown,
    create_api_key_field,
    create_browser_config_section,
    create_output_format_dropdown,
    create_output_dir_field,
    create_submit_button,
)
from src.layout.page_layout import create_page_content
from src.utility.event_handlers_llm import create_provider_changed_handler
from src.utility.event_handlers_execute import create_execute_button_handler
from src.layout.instruction_section import build_instruction_section

LLM_PROVIDERS = ["openrouter", "openai", "google"]
LLM_MODELS = {
    "openrouter": ["meta-llama/llama-4-maverick:free"],
    "openai": ["gpt-3.5-turbo", "gpt-4"],
    "google": ["gemini-2.0-flash", "gemini-2.0-pro"],
}


def setup_app(page: ft.Page):
    page.title = "Browser-Use Agent GUI"
    page.scroll = ft.ScrollMode.AUTO
    # インストラクション欄の構築
    instruction = build_instruction_section(page)
    (
        common_instruction_field,
        purpose_field,
        detail_field,
        reference_url_field,
        data_items_row,
    ) = (
        instruction["common_instruction_field"],
        instruction["purpose_field"],
        instruction["detail_field"],
        instruction["reference_url_field"],
        instruction["data_items_row"],
    )
    output_format_dropdown = create_output_format_dropdown()
    llm_provider_dropdown = create_llm_provider_dropdown(LLM_PROVIDERS)
    llm_model_dropdown = create_llm_model_dropdown()
    llm_model_dropdown.visible = False
    api_key_field = create_api_key_field(provider="", visible=False)
    browser_config_row = create_browser_config_section()
    # CheckBox型で取得
    headless_checkbox = browser_config_row.controls[0]
    keep_alive_checkbox = browser_config_row.controls[1]
    if not isinstance(headless_checkbox, ft.Checkbox):
        headless_checkbox = ft.Checkbox()
    if not isinstance(keep_alive_checkbox, ft.Checkbox):
        keep_alive_checkbox = ft.Checkbox()
    output_dir_field = create_output_dir_field()
    progress_bar = ft.ProgressBar(width=600, visible=False)
    status_text = ft.Text("", size=16)
    result_text = ft.Text("", size=16)

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
        output_dir_field=output_dir_field,
        progress_bar=progress_bar,
        status_text=status_text,
        result_text=result_text,
        data_items_row=data_items_row,
    )
    submit_button = create_submit_button()
    submit_button.on_click = button_clicked
    page_content = create_page_content(
        title="Browser-Use Agent GUI",
        subtitle="AIエージェントのインストラクションと設定",
        instruction_section=[
            common_instruction_field,
            purpose_field,
            detail_field,
            reference_url_field,
            data_items_row,
            output_format_dropdown,
        ],
        llm_section=[llm_provider_dropdown, llm_model_dropdown, api_key_field],
        browser_section=[browser_config_row],
        output_section=[output_dir_field],
        button_section=[submit_button, progress_bar, status_text],
        result_section=[result_text],
    )
    page.add(page_content)
