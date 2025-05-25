import flet as ft
from src.entity.controller_type import OutputFormat
from browser_use import BrowserConfig, Agent
from src.get_llm import LLMConfig
from src.component.ui_components import extract_data_items
from src.component.ui_instruction import compose_instruction
from src.global_cache import cache, CacheKey
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
    data_item_controls: ft.Column,
    submit_button: ft.ElevatedButton,
    stop_button: ft.ElevatedButton,
):
    # agent_ref, pause_flagをglobal_cacheで管理

    def set_resume_mode():
        submit_button.text = "エージェントを再開"
        submit_button.icon = ft.Icons.PLAY_ARROW
        submit_button.visible = True
        submit_button.on_click = resume_agent
        page.update()

    def set_normal_mode():
        submit_button.text = "エージェントを実行"
        submit_button.icon = ft.Icons.PLAY_ARROW
        submit_button.visible = True
        submit_button.on_click = button_clicked
        page.update()

    def stop_agent():
        cache.set(CacheKey.STOP, True)
        status_text.value = "エージェントを停止中..."
        agent = cache.get(CacheKey.AGENT, None)
        if agent and hasattr(agent, "stop"):
            import asyncio

            def call_stop():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                coro = agent.stop()
                if asyncio.iscoroutine(coro):
                    loop.run_until_complete(coro)

            threading.Thread(target=call_stop).start()
        page.update()

    def resume_agent(e=None):
        agent = cache.get(CacheKey.AGENT, None)
        if agent and hasattr(agent, "resume"):
            cache.set(CacheKey.PAUSE, False)
            submit_button.visible = False
            stop_button.visible = True
            progress_bar.visible = True
            status_text.value = "エージェントを再開中..."
            page.update()
            agent.resume()

    def button_clicked(e):
        if cache.get(CacheKey.RUNNING, False):
            # 既に実行中なら無視
            return
        cache.set(CacheKey.RUNNING, True)
        cache.set(CacheKey.STOP, False)
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
        data_items = extract_data_items(data_item_controls)
        instruction, message_context, context = compose_instruction(
            purpose_field.value,
            detail_field.value,
            reference_url_field.value,
            selected_output_format,
            data_items=data_items,
        )

        def run_agent():
            try:
                from src.utility.agent_executor import execute_agent, get_agent

                agent = get_agent(
                    instruction=instruction,
                    context=context,
                    message_context=message_context,
                    llm_config=llm_config,
                    browser_profile=browser_config,
                    output_format=selected_output_format,
                    output_dir=output_dir_field.value or "output",
                )
                cache.set(CacheKey.AGENT, agent)
                import asyncio

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(agent.run())
                status_text.value = "完了"
                result_text.value = str(result)
            except Exception as e:
                status_text.value = f"エラー: {str(e)}"
                result_text.value = ""
            finally:
                cache.set(CacheKey.RUNNING, False)
                set_normal_mode()
                stop_button.visible = False
                progress_bar.visible = False
                cache.set(CacheKey.AGENT, None)
                page.update()

        t = threading.Thread(target=run_agent)
        t.start()

    stop_button.on_click = lambda e: stop_agent()
    set_normal_mode()
    return button_clicked
