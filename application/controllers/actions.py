"""Actions."""

import flet as ft
import qrcode
import logging
from pathlib import Path
import cv2

def gen_qr(event: ft.ControlEvent, msg: str, dlg: ft.Control) -> None:
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
    event.page.close(dlg)

def read_qr(event: ft.ControlEvent, file: str) -> str:
    """Read QRCode."""
    logging.debug(event)
    img = cv2.imread(file)
    detector = cv2.QRCodeDetector()
    conteudo, _, _ = detector.detectAndDecode(img)
    return conteudo
