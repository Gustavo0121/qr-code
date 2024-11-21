"""Pages."""

import logging
from pathlib import Path

import flet as ft
from application.controllers.actions import gen_qr, read_qr
from application.controllers.appbar import AppBar


class Main(ft.View):
    """Main page."""

    def __init__(self, events: ft.ControlEvent, **kwargs: str):
        """Init it."""
        super().__init__()
        self.events = events
        self.route: str | None = kwargs.get('route')
        self.appbar = AppBar(self.events, 'QR Code')
        self.bgcolor = '#074166'
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.dlg_modal = ft.AlertDialog
        self.file_picker = ft.FilePicker(on_result=self.files_result)
        self.events.page.overlay.append(self.file_picker)
        self.conteudo = ''
        self.spacing = 75

        self.controls = [
            ft.Text(
                'Read and Generate QR Codes',
                theme_style=ft.TextThemeStyle.TITLE_LARGE,
                style=ft.TextStyle(
                    shadow=ft.BoxShadow(
                        blur_radius=3.0,
                        color='#10A7E3',
                        blur_style=ft.ShadowBlurStyle.OUTER,
                        offset=ft.Offset(4, 3),
                    ),
                ),
                size=40,
                color='black',
                weight=ft.FontWeight.BOLD,
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.TextButton(
                            'Gerar QR Code',
                            style=ft.ButtonStyle(
                                bgcolor='#0E8BDB',
                                shape=ft.RoundedRectangleBorder(radius=5),
                            ),
                            on_click=lambda e: self.dlgmodal(e, modal=True),
                        ),
                        ft.TextButton(
                            'Ler QR Code',
                            style=ft.ButtonStyle(
                                bgcolor='#0E8BDB',
                                shape=ft.RoundedRectangleBorder(radius=5),
                            ),
                            on_click=lambda _: self.file_picker.pick_files(),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    height=200,
                ),
                bgcolor='#0A6199',
                height=300,
                width=250,
                alignment=ft.alignment.center,
            ),
        ]

    def files_result(self, event: ft.FilePickerResultEvent) -> None:
        """Pick file result."""
        self.conteudo = read_qr(event, event.files[0].path)
        self.dlgmodal(event, modal=False)

    def dlgmodal(self, event: ft.ControlEvent, *, modal: bool) -> None:
        """Generate a QR Code."""
        self.dlg_modal = (
            ft.AlertDialog(
                bgcolor='#0A6199',
                modal=True,
                title=ft.Text(
                    'Gerador de QR Code',
                    color='black',
                    weight=ft.FontWeight.BOLD,
                ),
                content=ft.Column(
                    controls=[
                        ft.TextField(
                            label='Escreva a mensagem do QR Code',
                            text_style=ft.TextStyle(
                                color='black',
                                weight=ft.FontWeight.W_500,
                            ),
                        ),
                    ],
                ),
                actions=[
                    ft.TextButton(
                        'Cancelar',
                        on_click=lambda e: e.page.close(self.dlg_modal),
                    ),
                    ft.TextButton(
                        'Gerar',
                        on_click=lambda e: gen_qr(
                            e,
                            self.dlg_modal.content.controls[0].value,
                            self.dlg_modal,
                        ),
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda e: e.page.add(
                    ft.Text('Modal dialog dismissed'),
                ),
            )
            if modal
            else ft.AlertDialog(
                title=ft.Text(
                    'Conteúdo do QR Code',
                    color='black',
                    weight=ft.FontWeight.BOLD,
                ),
                content=ft.Text(self.conteudo, color='black', size=20),
                bgcolor='#0A6199',
            )
        )
        event.page.open(self.dlg_modal)


def main_view(e: ft.ControlEvent) -> ft.Control:
    """Main view."""
    logging.debug(e)
    return Main(e, route='/')


def not_found_view(e: ft.ControlEvent) -> ft.Control:
    """Notfount view."""
    logging.debug(e)
    return ft.View(
        route='/notfound',
        controls=[
            ft.Column(
                controls=[
                    ft.Text(
                        value='Recurso não encontrado...',
                        color='red',
                        weight='bold',
                    ),
                ],
            ),
        ],
    )


if __name__ == '__main__':
    read_qr(
        ft.ControlEvent,
        Path(__file__).parents[2].joinpath('teste.png').as_posix(),
    )
