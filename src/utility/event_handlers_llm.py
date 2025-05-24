import flet as ft
from typing import Dict, List


def create_provider_changed_handler(
    provider_dropdown: ft.Dropdown,
    model_dropdown: ft.Dropdown,
    llm_models: Dict[str, List[str]],
    page: ft.Page,
):
    def provider_changed(e):
        selected_provider = provider_dropdown.value
        if selected_provider:
            model_dropdown.options = [
                ft.dropdown.Option(model)
                for model in llm_models.get(selected_provider, [])
            ]
            if model_dropdown.options:
                model_dropdown.value = model_dropdown.options[0].key
        else:
            model_dropdown.options = []
            model_dropdown.value = None
        page.update()

    return provider_changed
