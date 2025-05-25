import flet as ft
from src.entity.controller_type import OutputFormat
from src.component.common.custom_fields import CustomDropdown


def create_llm_provider_dropdown(providers):
    return CustomDropdown(
        label="LLMプロバイダー",
        width=600,
        options=[ft.dropdown.Option(provider) for provider in providers],
    )


def create_llm_model_dropdown():
    return CustomDropdown(
        label="LLMモデル",
        width=600,
        options=[],
    )


def create_output_format_dropdown():
    return CustomDropdown(
        label="出力形式",
        width=600,
        options=[ft.dropdown.Option(fmt.value) for fmt in OutputFormat],
        value=OutputFormat.MARKDOWN.value,
    )
