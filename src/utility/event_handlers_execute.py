import flet as ft
import os
from src.entity.controller_type import OutputFormat
from browser_use import BrowserConfig
from src.get_llm import LLMConfig
from src.conponent.ui_components import compose_instruction, get_data_items_from_row


def create_execute_button_handler(
    page: ft.Page,
    purpose_field: ft.TextField,
    detail_field: ft.TextField,
    reference_url_field: ft.TextField,
    llm_provider_dropdown: ft.Dropdown,
    llm_model_dropdown: ft.Dropdown,
    api_key_field: ft.TextField,
    headless_checkbox: ft.Checkbox,
    keep_alive_checkbox: ft.Checkbox,
    output_format_dropdown: ft.Dropdown,
    output_dir_field: ft.TextField,
    progress_bar: ft.ProgressBar,
    status_text: ft.Text,
    result_text: ft.Text,
    data_items_row: ft.Row,
):
    def button_clicked(e):
        if not purpose_field.value:
            purpose_field.error_text = "目的を入力してください"
            page.update()
            return
        if not detail_field.value:
            detail_field.error_text = "詳細を入力してください"
            page.update()
            return
        if not llm_provider_dropdown.value or not llm_model_dropdown.value:
            llm_provider_dropdown.error_text = "LLMプロバイダーを選択してください"
            llm_model_dropdown.error_text = "LLMモデルを選択してください"
        purpose_field.error_text = None
        detail_field.error_text = None
        llm_provider_dropdown.error_text = None
        llm_model_dropdown.error_text = None
        progress_bar.visible = True
        status_text.value = "エージェントを準備中..."
        page.update()
        selected_output_format = OutputFormat.MARKDOWN
        if output_format_dropdown.value:
            selected_output_format = OutputFormat(output_format_dropdown.value)
        api_key = api_key_field.value
        llm_config = LLMConfig(
            provider=llm_provider_dropdown.value or "",
            model=llm_model_dropdown.value or "",
            api_key=api_key or "",
        )
        browser_config = BrowserConfig(
            headless=headless_checkbox.value, keep_alive=keep_alive_checkbox.value
        )
        data_items = get_data_items_from_row(data_items_row)
        instruction = compose_instruction(
            purpose_field.value,
            detail_field.value,
            reference_url_field.value,
            selected_output_format,
            data_items=data_items,
        )
        try:
            from src.utility.agent_executor import execute_agent

            result = execute_agent(
                instruction=instruction,
                llm_config=llm_config,
                browser_profile=browser_config,
                output_format=selected_output_format,
                output_dir=output_dir_field.value or "output",
            )
            status_text.value = "完了"
            result_text.value = str(result)
        except Exception as e:
            status_text.value = f"エラー: {str(e)}"
            result_text.value = ""
        finally:
            progress_bar.visible = False
            page.update()

    return button_clicked
