"""Pages."""

import logging

import flet as ft

def main_view(e: ft.ControlEvent) -> ft.Control:
    """Main view."""
    logging.debug(e)
    return ft.View(
        route='/',
        bgcolor='#074166',
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment = ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.TextButton(
                            'Gerar QRCode',
                            style=ft.ButtonStyle(bgcolor='#0E8BDB', shape=ft.RoundedRectangleBorder(radius=5)),
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
        ],
    )

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
