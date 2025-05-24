import flet as ft
from src.entity.controller_type import OutputFormat


def create_llm_provider_dropdown(providers):
    return ft.Dropdown(
        label="LLMプロバイダー",
        width=600,
        options=[ft.dropdown.Option(provider) for provider in providers],
    )


def create_llm_model_dropdown():
    return ft.Dropdown(
        label="LLMモデル",
        width=600,
        options=[],
    )


def create_output_format_dropdown():
    return ft.Dropdown(
        label="出力形式",
        width=600,
        options=[ft.dropdown.Option(fmt.value) for fmt in OutputFormat],
        value=OutputFormat.MARKDOWN.value,
    )
