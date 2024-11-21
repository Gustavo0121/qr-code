"""Actions."""

import flet as ft
import qrcode
import logging
import cv2
from pathlib import Path
from tempfile import NamedTemporaryFile
# from application import qrcodes

qrcodes: list = []

def gen_qr(event: ft.ControlEvent, msg: str, dlg: ft.Control) -> None:
    """Generate QRCode."""
    logging.debug(event)
    qrcodes.append(Path(NamedTemporaryFile(suffix='.png').name))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(msg)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(qrcodes[-1].as_posix())
    print(qrcodes)
    dlg_qr: ft.AlertDialog = ft.AlertDialog(
        title=ft.Text('QRCode gerado'),
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
            ],
        ),
    )
    event.page.open(dlg_qr)
    event.page.close(dlg)

def download(event: ft.ControlEvent, img: qrcode.image.pure.PyPNGImage, dlg: ft.Control) -> None:
    """Download image."""
    logging.debug(event)
    img.save(Path.home().joinpath('Downloads', 'teste.png').as_posix())
    event.page.close(dlg)


def read_qr(event: ft.ControlEvent, file: str) -> str:
    """Read QRCode."""
    logging.debug(event)
    img = cv2.imread(file)
    detector = cv2.QRCodeDetector()
    conteudo, _, _ = detector.detectAndDecode(img)
    return conteudo

if __name__ == '__main__':
    print(Path(NamedTemporaryFile(suffix='.png').name))
