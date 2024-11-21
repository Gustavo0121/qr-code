"""Appbar."""

import flet as ft

class AppBar(ft.AppBar):
    """Appbar component."""

    def __init__(
        self,
        events: ft.ControlEvent,
        titulo: str = '',
    ):
        """Init for Appbar class."""
        super().__init__()
        self.events = events
        self.title = ft.Text(
            titulo,
            selectable=True,
            weight=ft.FontWeight.BOLD,
            size=30,
            color='black',
        )
        self.center_title = True
        self.toolbar_height = 60
        self.bgcolor = '#10A7E3'

        self.leading = ft.Icon(ft.icons.QR_CODE_2_OUTLINED, size=40, color='black')

        self.actions = [ft.IconButton(icon=ft.icons.CLOSE, icon_color='red', icon_size=40,on_click=self.close_app)]

    def close_app(self, event: ft.ControlEvent) -> None:
        """Close app."""
        event.page.window_close()