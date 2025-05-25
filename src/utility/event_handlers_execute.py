import flet as ft
from src.entity.controller_type import OutputFormat
from browser_use import BrowserConfig
from src.get_llm import LLMConfig
from src.component.ui_components import compose_instruction, get_data_items_from_row
from src.component.common.global_cache import set_global, get_global
import threading


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
    submit_button: ft.ElevatedButton,
    stop_button: ft.ElevatedButton,
):
    def stop_agent():
        set_global("agent_stop_flag", True)
        status_text.value = "エージェントを停止中..."
        page.update()

    def button_clicked(e):
        if get_global("agent_running", False):
            # 既に実行中なら無視
            return
        set_global("agent_running", True)
        set_global("agent_stop_flag", False)
        submit_button.visible = False
        stop_button.visible = True
        progress_bar.visible = True
        status_text.value = "エージェントを準備中..."
        page.update()
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

        def run_agent():
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
                set_global("agent_running", False)
                submit_button.visible = True
                stop_button.visible = False
                progress_bar.visible = False
                page.update()

        t = threading.Thread(target=run_agent)
        t.start()

    stop_button.on_click = lambda e: stop_agent()
    return button_clicked
