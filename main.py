from dotenv import load_dotenv
import flet as ft
from src.app_setup import setup_app

# 環境変数の読み込み
load_dotenv()


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM
    setup_app(page)


ft.app(target=main)
