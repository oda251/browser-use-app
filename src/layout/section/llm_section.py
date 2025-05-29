import flet as ft
from src.component.ui_components import (
    create_llm_provider_dropdown,
    create_llm_model_dropdown,
    create_api_key_field,
)
from src.global_cache import cache
from src.entity.input_values import LLMInputKey

LLM_PROVIDERS = ["openrouter", "openai", "google"]
LLM_MODELS = {
    "openrouter": ["meta-llama/llama-4-maverick:free"],
    "openai": ["gpt-3.5-turbo", "gpt-4"],
    "google": ["gemini-2.0-flash", "gemini-2.0-pro"],
}


def build_llm_section(page: ft.Page):
    llm_provider_dropdown = create_llm_provider_dropdown(LLM_PROVIDERS)
    llm_model_dropdown = create_llm_model_dropdown()
    llm_model_dropdown.visible = False
    api_key_field = create_api_key_field(provider="", visible=False)

    def cache_on_change(field, key):
        def handler(e):
            cache.set(key.value, field.value)

        return handler

    llm_provider_dropdown.on_change = cache_on_change(
        llm_provider_dropdown, LLMInputKey.PROVIDER
    )
    llm_model_dropdown.on_change = cache_on_change(
        llm_model_dropdown, LLMInputKey.MODEL
    )
    api_key_field.on_change = cache_on_change(api_key_field, LLMInputKey.API_KEY)

    return {
        "llm_provider_dropdown": llm_provider_dropdown,
        "llm_model_dropdown": llm_model_dropdown,
        "api_key_field": api_key_field,
    }
