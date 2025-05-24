import flet as ft
import os
import sys
import traceback
from typing import Dict, List
from src.entity.controller_type import OutputFormat
from browser_use import BrowserConfig
from src.get_llm import LLMConfig
from src.conponent.ui_components import compose_instruction


def create_provider_changed_handler(
    provider_dropdown: ft.Dropdown,
    model_dropdown: ft.Dropdown,
    llm_models: Dict[str, List[str]],
    page: ft.Page,
):
    """
    プロバイダー変更時のイベントハンドラを作成します
    """

    def provider_changed(e):
        selected_provider = provider_dropdown.value
        if selected_provider:
            # モデルの選択肢を更新
            model_dropdown.options = [
                ft.dropdown.Option(model)
                for model in llm_models.get(selected_provider, [])
            ]
            # 最初のモデルを選択
            if model_dropdown.options:
                model_dropdown.value = model_dropdown.options[0].key
        else:
            model_dropdown.options = []
            model_dropdown.value = None

        page.update()

    return provider_changed


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
    data_items_row: ft.Row,  # 追加
):
    """
    実行ボタンクリック時のイベントハンドラを作成します
    """

    def button_clicked(e):
        # バリデーション
        if not purpose_field.value:
            purpose_field.error_text = "目的を入力してください"
            page.update()
            return
        if not detail_field.value:
            detail_field.error_text = "詳細を入力してください"
            page.update()
            return
        # instruction_fieldは使わない
        if not llm_provider_dropdown.value or not llm_model_dropdown.value:
            llm_provider_dropdown.error_text = "LLMプロバイダーを選択してください"
            llm_model_dropdown.error_text = "LLMモデルを選択してください"
            page.update()
            return
        # エラーテキストをクリア
        purpose_field.error_text = None
        detail_field.error_text = None
        llm_provider_dropdown.error_text = None
        llm_model_dropdown.error_text = None

        # 進行状況表示
        progress_bar.visible = True
        status_text.value = "エージェントを準備中..."
        page.update()

        # 選択されたコントローラータイプを取得
        selected_output_format = OutputFormat.MARKDOWN
        if output_format_dropdown.value:
            selected_output_format = OutputFormat(output_format_dropdown.value)

        # APIキーの取得（優先順位: 入力値 > 環境変数）
        api_key = api_key_field.value
        if not api_key:
            env_key = f"{llm_provider_dropdown.value.upper()}_API_KEY"
            api_key = os.environ.get(env_key, "")

        # LLM設定
        llm_config = LLMConfig(
            provider=llm_provider_dropdown.value,
            model=llm_model_dropdown.value,
            api_key=api_key,
        )

        # ブラウザ設定
        browser_config = BrowserConfig(
            headless=headless_checkbox.value, keep_alive=keep_alive_checkbox.value
        )

        # インストラクションを合成
        from src.conponent.ui_components import get_data_items_from_row

        # データ項目の取得
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
