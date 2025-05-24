import flet as ft
import os
import sys
import traceback
from typing import Dict, List

# 最初にプロジェクトのルートディレクトリをパスに追加
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.entity.controller_type import ControllerType
from browser_use import BrowserConfig
from src.get_llm import LLMConfig


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
    instruction_field: ft.TextField,
    llm_provider_dropdown: ft.Dropdown,
    llm_model_dropdown: ft.Dropdown,
    api_key_field: ft.TextField,
    headless_checkbox: ft.Checkbox,
    keep_alive_checkbox: ft.Checkbox,
    controller_type_checkboxes: ft.Row,
    output_dir_field: ft.TextField,
    progress_bar: ft.ProgressBar,
    status_text: ft.Text,
    result_text: ft.Text,
):
    """
    実行ボタンクリック時のイベントハンドラを作成します
    """

    # 非同期処理をシンプルにするため、クラス内関数として定義せず、別のアプローチを使用
    def button_clicked(e):
        # 同期関数内で処理を行う
        # バリデーション
        if not instruction_field.value:
            instruction_field.error_text = "インストラクションを入力してください"
            page.update()
            return

        if not llm_provider_dropdown.value or not llm_model_dropdown.value:
            llm_provider_dropdown.error_text = (
                "LLMプロバイダーとモデルを選択してください"
            )
            page.update()
            return

        # エラーテキストをクリア
        instruction_field.error_text = None
        llm_provider_dropdown.error_text = None

        # 進行状況表示
        progress_bar.visible = True
        status_text.value = "エージェントを準備中..."
        page.update()

        # 選択されたコントローラータイプを取得
        from src.entity.controller_type import ControllerType

        selected_controller_types = []
        for idx, ct in enumerate(ControllerType):
            if controller_type_checkboxes.controls[idx].value:
                selected_controller_types.append(ct)

        # APIキーの取得（優先順位: 入力値 > 環境変数）
        api_key = api_key_field.value
        if not api_key:
            env_var_name = f"{llm_provider_dropdown.value.upper()}_API_KEY"
            api_key = os.getenv(env_var_name, "")

        # LLM設定
        from src.get_llm import LLMConfig

        llm_config = LLMConfig(
            provider=llm_provider_dropdown.value,
            model=llm_model_dropdown.value,
            api_key=api_key,
        )

        # ブラウザ設定
        from browser_use import BrowserConfig

        browser_config = BrowserConfig(
            headless=headless_checkbox.value, keep_alive=keep_alive_checkbox.value
        )

        try:
            # エージェントの取得
            status_text.value = "エージェントを作成中..."
            page.update()

            from src.utility.agent_executor import execute_agent

            # バックグラウンドでエージェントを実行（非同期処理ではなく別スレッドで実行）
            status_text.value = (
                "エージェントを実行中...これには数分かかる場合があります"
            )
            page.update()

            import threading

            def run_in_thread():
                try:
                    result = execute_agent(
                        instruction=instruction_field.value,
                        llm_config=llm_config,
                        browser_profile=browser_config,
                        controller_types=selected_controller_types,
                        output_dir=output_dir_field.value,
                    )

                    # 実行完了時の処理
                    def on_complete():
                        status_text.value = "実行完了！"
                        result_text.value = f"Agentの実行が完了しました。出力は {output_dir_field.value} ディレクトリに保存されています。"
                        progress_bar.visible = False
                        page.update()

                    # メインスレッドでUIを更新
                    page.window_to_front = True  # ウィンドウを前面に
                    on_complete()  # 直接呼び出し
                except Exception as ex:
                    # エラーをstderrに出力
                    error_details = traceback.format_exc()
                    sys.stderr.write(f"エラー発生: {str(ex)}\n{error_details}\n")

                    # エラー発生時の処理
                    def on_error():
                        status_text.value = "エラーが発生しました"
                        result_text.value = f"エラー: {str(ex)}\nコンソールの詳細なエラーメッセージを確認してください。"
                        progress_bar.visible = False
                        page.update()

                    # メインスレッドでUIを更新
                    page.window_to_front = True  # ウィンドウを前面に
                    on_error()  # 直接呼び出し

            # スレッドを開始
            threading.Thread(target=run_in_thread).start()

        except Exception as e:
            # エラーをstderrに出力
            error_details = traceback.format_exc()
            sys.stderr.write(f"初期化エラー: {str(e)}\n{error_details}\n")

            status_text.value = "エラーが発生しました"
            result_text.value = f"エラー: {str(e)}\nコンソールの詳細なエラーメッセージを確認してください。"
            progress_bar.visible = False
            page.update()

    return button_clicked
