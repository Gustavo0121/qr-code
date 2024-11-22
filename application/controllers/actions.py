"""Actions."""

import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
from datetime import datetime

import cv2
import flet as ft
from flet_toast import flet_toast
import qrcode

qrcodes: list = []

colors = {
    'Azul': 'blue',
    'Verde': 'green',
    'Amarelo': 'yellow',
    'Roxo': 'purple',
    'Rosa': 'pink',
    'Vermelho': 'red',
    'Laranja': 'orange',
    'Marrom': 'brown',
    'Cinza': 'gray',
    'Branco': 'white',
    'Preto': 'black',
}


def gen_qr(
    event: ft.ControlEvent,
    msg: str,
    dlg: ft.Control,
    bkgcolor: str,
    qrcolor: str,
) -> None:
    """Generate QR Code."""
    logging.debug(event)
    qrcodes.append(Path(NamedTemporaryFile(suffix='.png').name))  # noqa: SIM115
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(msg)
    qr.make(fit=True)
    img = qr.make_image(
        fill_color=colors[qrcolor],
        back_color=colors[bkgcolor],
    )
    img.save(qrcodes[-1].as_posix())
    dlg_qr: ft.AlertDialog = ft.AlertDialog(
        title=ft.Text('QR Code gerado', weight=ft.FontWeight.BOLD),
        bgcolor='#074166',
        content=ft.Column(
            controls=[
                ft.Image(qrcodes[-1].as_posix()),
                ft.Row(
                    controls=[
                        ft.TextButton(
                            'Close',
                            on_click=lambda e: e.page.close(dlg_qr),
                        ),
                        ft.TextButton(
                            'Download',
                            on_click=lambda e: download(e, img, dlg_qr),
                        ),
                    ],
                ),
            ] if bkgcolor == 'Branco' and qrcolor == 'Preto' else[
                ft.Image(qrcodes[-1].as_posix()),
                ft.Text('Os QR Codes com cores alteradas estão sujeitos à dificuldade ou até mesmo à ilegibilidade da mensagem', color='#76CEF2', weight=ft.FontWeight.BOLD, size=20, width=350),
                ft.Row(
                    controls=[
                        ft.TextButton(
                            'Close',
                            on_click=lambda e: e.page.close(dlg_qr),
                        ),
                        ft.TextButton(
                            'Download',
                            on_click=lambda e: download(e, img, dlg_qr),
                        ),
                    ],
                ),
            ],
        ),
    )
    event.page.open(dlg_qr)
    event.page.close(dlg)


def download(
    event: ft.ControlEvent,
    img: qrcode.image.pure.PyPNGImage,
    dlg: ft.Control,
) -> None:
    """Download image."""
    logging.debug(event)
    now = datetime.now()
    img.save(Path.home().joinpath('Downloads', f'QR_{now.strftime("%Y%m%d%H%M%S")}.png').as_posix())
    event.page.close(dlg)
    flet_toast.sucess(event.page, 'Download bem sucedido', 'top_right')


def read_qr(event: ft.ControlEvent, file: str) -> str:
    """Read QRCode."""
    logging.debug(event)
    img = cv2.imread(file)
    detector = cv2.QRCodeDetector()
    conteudo, _, _ = detector.detectAndDecode(img)
    return conteudo
