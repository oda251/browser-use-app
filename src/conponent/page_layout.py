import flet as ft
from typing import List


def create_page_content(
    title: str,
    subtitle: str,
    instruction_section: List[ft.Control],
    llm_section: List[ft.Control],
    browser_section: List[ft.Control],
    controller_section: List[ft.Control],
    output_section: List[ft.Control],
    button_section: List[ft.Control],
    result_section: List[ft.Control],
) -> ft.Column:
    """
    ページ全体のレイアウトを作成します
    """
    return ft.Column(
        controls=[
            # ヘッダー
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(title, size=30, weight=ft.FontWeight.BOLD),
                        ft.Text(subtitle, size=16),
                    ],
                ),
                padding=ft.padding.only(bottom=20),
            ),
            # インストラクションセクション
            create_section("インストラクション", instruction_section),
            # LLM設定セクション
            create_section("LLM設定", llm_section),
            # ブラウザ設定セクション
            create_section("ブラウザ設定", browser_section),
            # コントローラー設定セクション
            create_section("コントローラー設定", controller_section),
            # 出力設定セクション
            create_section("出力設定", output_section),
            # ボタンセクション
            create_section("", button_section),
            # 結果セクション
            create_section("実行結果", result_section),
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
    )


def create_section(title: str, controls: List[ft.Control]) -> ft.Container:
    """
    セクションを作成します
    """
    section_controls = []

    if title:
        section_controls.append(ft.Text(title, size=18, weight=ft.FontWeight.BOLD))

    section_controls.extend(controls)

    return ft.Container(
        content=ft.Column(
            controls=section_controls,
            spacing=10,
        ),
        padding=10,
        border=ft.border.all(1, ft.Colors.BLACK12),
        border_radius=10,
    )
