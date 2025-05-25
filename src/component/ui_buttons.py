import flet as ft


def create_submit_button() -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text="エージェントを実行",
        width=600,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
        ),
        icon=ft.Icons.PLAY_ARROW,
    )


def create_stop_button() -> ft.ElevatedButton:
    return ft.ElevatedButton(
        text="エージェントを停止",
        width=600,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
        ),
        icon=ft.Icons.STOP,
    )
