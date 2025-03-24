"""Actions."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

import cv2
import flet as ft
import qrcode
from flet_toast import flet_toast
from pytz import timezone
from pyzbar.pyzbar import decode

qrcodes: list = []

colors = [
    'aliceblue',
    'antiquewhite',
    'aqua',
    'aquamarine',
    'azure',
    'beige',
    'bisque',
    'black',
    'blanchedalmond',
    'blue',
    'blueviolet',
    'brown',
    'burlywood',
    'cadetblue',
    'chartreuse',
    'chocolate',
    'coral',
    'cornflowerblue',
    'cornsilk',
    'crimson',
    'cyan',
    'darkblue',
    'darkcyan',
    'darkgoldenrod',
    'darkgray',
    'darkgrey',
    'darkgreen',
    'darkkhaki',
    'darkmagenta',
    'darkolivegreen',
    'darkorange',
    'darkorchid',
    'darkred',
    'darksalmon',
    'darkseagreen',
    'darkslateblue',
    'darkslategray',
    'darkslategrey',
    'darkturquoise',
    'darkviolet',
    'deeppink',
    'deepskyblue',
    'dimgray',
    'dimgrey',
    'dodgerblue',
    'firebrick',
    'floralwhite',
    'forestgreen',
    'fuchsia',
    'gainsboro',
    'ghostwhite',
    'gold',
    'goldenrod',
    'gray',
    'grey',
    'green',
    'greenyellow',
    'honeydew',
    'hotpink',
    'indianred',
    'indigo',
    'ivory',
    'khaki',
    'lavender',
    'lavenderblush',
    'lawngreen',
    'lemonchiffon',
    'lightblue',
    'lightcoral',
    'lightcyan',
    'lightgoldenrodyellow',
    'lightgray',
    'lightgrey',
    'lightgreen',
    'lightpink',
    'lightsalmon',
    'lightseagreen',
    'lightskyblue',
    'lightslategray',
    'lightslategrey',
    'lightsteelblue',
    'lightyellow',
    'lime',
    'limegreen',
    'linen',
    'magenta',
    'maroon',
    'mediumaquamarine',
    'mediumblue',
    'mediumorchid',
    'mediumpurple',
    'mediumseagreen',
    'mediumslateblue',
    'mediumspringgreen',
    'mediumturquoise',
    'mediumvioletred',
    'midnightblue',
    'mintcream',
    'mistyrose',
    'moccasin',
    'navajowhite',
    'navy',
    'oldlace',
    'olive',
    'olivedrab',
    'orange',
    'orangered',
    'orchid',
    'palegoldenrod',
    'palegreen',
    'paleturquoise',
    'palevioletred',
    'papayawhip',
    'peachpuff',
    'peru',
    'pink',
    'plum',
    'powderblue',
    'purple',
    'red',
    'rosybrown',
    'royalblue',
    'saddlebrown',
    'salmon',
    'sandybrown',
    'seagreen',
    'seashell',
    'sienna',
    'silver',
    'skyblue',
    'slateblue',
    'slategray',
    'slategrey',
    'snow',
    'springgreen',
    'steelblue',
    'tan',
    'teal',
    'thistle',
    'tomato',
    'turquoise',
    'violet',
    'wheat',
    'white',
    'whitesmoke',
    'yellow',
    'yellowgreen',
]


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
        fill_color=qrcolor,
        back_color=bkgcolor,
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
            ]
            if bkgcolor == 'Branco' and qrcolor == 'Preto'
            else [
                ft.Image(qrcodes[-1].as_posix()),
                ft.Text(
                    'Os QR Codes com cores alteradas estão'
                    ' sujeitos à dificuldade ou até mesmo à'
                    ' ilegibilidade da mensagem',
                    color='#76CEF2',
                    weight=ft.FontWeight.BOLD,
                    size=20,
                    width=350,
                ),
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
    now = datetime.now(tz=timezone('America/Sao_Paulo'))
    img.save(
        Path.home()
        .joinpath('Downloads', f'QR_{now.strftime("%Y%m%d%H%M%S")}.png')
        .as_posix(),
    )
    event.page.close(dlg)
    flet_toast.sucess(event.page, 'Download bem sucedido', 'top_right')


def read_qr(event: ft.ControlEvent, file: str) -> str:
    """Read QRCode."""
    logging.debug(event)
    img = cv2.imread(file)
    detector = cv2.QRCodeDetector()
    conteudo, _, _ = detector.detectAndDecode(img)
    return conteudo


def scan_qr(event: ft.ControlEvent) -> str:
    """Scan QRCode."""
    logging.debug(event)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        flet_toast.error(event.page, 'Erro ao abrir a câmera', 'top_right')
        sys.exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            flet_toast.error(event.page, 'Não foi possível ler o QR code', 'top_right')
            break

        cv2.imshow('Scanner de QR Code', frame)

        qr_codes = decode(frame)
        if qr_codes:
            break

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return qr_codes[0].data.decode('utf-8')
