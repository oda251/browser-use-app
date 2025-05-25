import flet as ft
from typing import List
from src.theme.color import get_highlight_mid


def create_page_content(
    title: str,
    subtitle: str,
    instruction_section: list[ft.Control],
    llm_section: list[ft.Control],
    browser_section: list[ft.Control],
    output_section: list[ft.Control],
    button_section: list[ft.Control],
    result_section: list[ft.Control],
) -> ft.Column:
    """
    ページ全体のレイアウトを作成します
    """
    instruction_controls = instruction_section.copy()
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
                padding=ft.padding.only(bottom=10, left=10),
            ),
            # インストラクションセクション
            create_section("", instruction_controls),
            # LLM設定セクション
            create_section("LLM設定", llm_section),
            # ブラウザ設定セクション
            create_section("ブラウザ設定", browser_section),
            # 出力設定セクション
            create_section("出力設定", output_section),
            # ボタンセクション
            create_section("", button_section),
            # 結果セクション
            create_section("実行結果", result_section),
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        alignment=ft.MainAxisAlignment.CENTER,
    )


def create_section(title: str, controls: List[ft.Control]) -> ft.Container:
    """
    セクションを作成します
    """
    section_controls = []

    if title:
        section_controls.append(ft.Text(title, size=20, weight=ft.FontWeight.BOLD))

    section_controls.extend(controls)

    return ft.Container(
        content=ft.Column(
            controls=section_controls,
            spacing=10,
        ),
        padding=10,
        border=ft.border.all(1, get_highlight_mid()),
        border_radius=10,
        width=640,
    )
