import flet as ft
from src.component.ui_buttons import create_stop_button
from src.component.ui_components import create_submit_button


def build_button_section():
    submit_button = create_submit_button()
    stop_button = create_stop_button()
    stop_button.visible = False
    progress_bar = ft.ProgressBar(width=600, visible=False)
    status_text = ft.Text("", size=16)
    return {
        "submit_button": submit_button,
        "stop_button": stop_button,
        "progress_bar": progress_bar,
        "status_text": status_text,
    }
