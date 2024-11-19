"""Pages."""

import logging

import flet as ft
import qrcode

from pathlib import Path

class Main(ft.View):
    """Main page."""
    def __init__(self, events: ft.ControlEvent, **kwargs: str):
        """Init it."""
        super().__init__()
        self.events = events
        self.route: str | None = kwargs.get('route')
        self.bgcolor='#074166'
        self.horizontal_alignment=ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.dlg_modal = ft.AlertDialog()
        self.controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.TextButton(
                            'Gerar QRCode',
                            style=ft.ButtonStyle(bgcolor='#0E8BDB', shape=ft.RoundedRectangleBorder(radius=5)),
                            on_click=self.dlgmodal,
                        ),
                        ft.TextButton(
                            'Ler QRCode',
                            style=ft.ButtonStyle(bgcolor='#0E8BDB', shape=ft.RoundedRectangleBorder(radius=5)),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    height=200,
                ),
                bgcolor='#0A6199',
                height=550,
                width=400,
                alignment = ft.alignment.center,
            ),
        ]

    def dlgmodal(self, event: ft.ControlEvent) -> None:
        """Generate a QRCode."""
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text('Gerador de QRCode'),
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.TextField(
                            label='Escreva a mensagem do QRCode',
                        ),
                        bgcolor='#0A6199',
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
                    on_click=lambda e: self.gen_qr(e, self.dlg_modal.content.controls[0].content.value),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: e.page.add(
                ft.Text('Modal dialog dismissed'),
            ),
        )
        event.page.open(self.dlg_modal)

    def gen_qr(self, event: ft.ControlEvent, msg: str):
        """Generate QRCode."""
        logging.debug(event)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(msg)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save(Path(__file__).parents[2].joinpath('teste.png').as_posix())




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
