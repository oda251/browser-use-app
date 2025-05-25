import flet as ft
import darkdetect

def get_font_color() -> str:
    if darkdetect.isDark():
        return ft.Colors.GREY_300
    return ft.Colors.GREY_700

def get_highlight_low() -> str:
    if darkdetect.isDark():
        return ft.Colors.BLUE_GREY_800
    return ft.Colors.BLUE_GREY_100

def get_highlight_mid() -> str:
    if darkdetect.isDark():
        return ft.Colors.DEEP_ORANGE_700
    return ft.Colors.BLUE_GREY_200

def get_highlight() -> str:
    if darkdetect.isDark():
        return ft.Colors.GREY_300
    return ft.Colors.BLUE_600
