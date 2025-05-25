import flet as ft
from src.theme.color import get_highlight_low, get_highlight, get_font_color


class CustomTextField(ft.TextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_color = get_highlight_low()
        self.focused_border_color = get_highlight()
        self.color = get_font_color()


class CustomDropdown(ft.Dropdown):
    def __init__(self, *args, **kwargs):
        page = kwargs.pop("page", None)
        super().__init__(*args, **kwargs)
        self.border_color = get_highlight_low()
        self.focused_border_color = get_highlight()
        self.color = get_font_color()
