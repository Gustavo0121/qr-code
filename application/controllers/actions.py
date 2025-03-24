"""Actions."""

import logging
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

# colors = {
#     'Azul': 'blue',
#     'Verde': 'green',
#     'Amarelo': 'yellow',
#     'Roxo': 'purple',
#     'Rosa': 'pink',
#     'Vermelho': 'red',
#     'Laranja': 'orange',
#     'Marrom': 'brown',
#     'Cinza': 'gray',
#     'Branco': 'white',
#     'Preto': 'black',
# }

colors = {
    'teste0': 'aliceblue',
    'teste1': 'antiquewhite',
    'teste2': 'aqua',
    'teste3': 'aquamarine',
    'teste4': 'azure',
    'teste5': 'beige',
    'teste6': 'bisque',
    'teste7': 'black',
    'teste8': 'blanchedalmond',
    'teste9': 'blue',
    'teste10': 'blueviolet',
    'teste11': 'brown',
    'teste12': 'burlywood',
    'teste13': 'cadetblue',
    'teste14': 'chartreuse',
    'teste15': 'chocolate',
    'teste16': 'coral',
    'teste17': 'cornflowerblue',
    'teste18': 'cornsilk',
    'teste19': 'crimson',
    'teste20': 'cyan',
    'teste21': 'darkblue',
    'teste22': 'darkcyan',
    'teste23': 'darkgoldenrod',
    'teste24': 'darkgray',
    'teste25': 'darkgrey',
    'teste26': 'darkgreen',
    'teste27': 'darkkhaki',
    'teste28': 'darkmagenta',
    'teste29': 'darkolivegreen',
    'teste30': 'darkorange',
    'teste31': 'darkorchid',
    'teste32': 'darkred',
    'teste33': 'darksalmon',
    'teste34': 'darkseagreen',
    'teste35': 'darkslateblue',
    'teste36': 'darkslategray',
    'teste37': 'darkslategrey',
    'teste38': 'darkturquoise',
    'teste39': 'darkviolet',
    'teste40': 'deeppink',
    'teste41': 'deepskyblue',
    'teste42': 'dimgray',
    'teste43': 'dimgrey',
    'teste44': 'dodgerblue',
    'teste45': 'firebrick',
    'teste46': 'floralwhite',
    'teste47': 'forestgreen',
    'teste48': 'fuchsia',
    'teste49': 'gainsboro',
    'teste50': 'ghostwhite',
    'teste51': 'gold',
    'teste52': 'goldenrod',
    'teste53': 'gray',
    'teste54': 'grey',
    'teste55': 'green',
    'teste56': 'greenyellow',
    'teste57': 'honeydew',
    'teste58': 'hotpink',
    'teste59': 'indianred',
    'teste60': 'indigo',
    'teste61': 'ivory',
    'teste62': 'khaki',
    'teste63': 'lavender',
    'teste64': 'lavenderblush',
    'teste65': 'lawngreen',
    'teste66': 'lemonchiffon',
    'teste67': 'lightblue',
    'teste68': 'lightcoral',
    'teste69': 'lightcyan',
    'teste70': 'lightgoldenrodyellow',
    'teste71': 'lightgray',
    'teste72': 'lightgrey',
    'teste73': 'lightgreen',
    'teste74': 'lightpink',
    'teste75': 'lightsalmon',
    'teste76': 'lightseagreen',
    'teste77': 'lightskyblue',
    'teste78': 'lightslategray',
    'teste79': 'lightslategrey',
    'teste80': 'lightsteelblue',
    'teste81': 'lightyellow',
    'teste82': 'lime',
    'teste83': 'limegreen',
    'teste84': 'linen',
    'teste85': 'magenta',
    'teste86': 'maroon',
    'teste87': 'mediumaquamarine',
    'teste88': 'mediumblue',
    'teste89': 'mediumorchid',
    'teste90': 'mediumpurple',
    'teste91': 'mediumseagreen',
    'teste92': 'mediumslateblue',
    'teste93': 'mediumspringgreen',
    'teste94': 'mediumturquoise',
    'teste95': 'mediumvioletred',
    'teste96': 'midnightblue',
    'teste97': 'mintcream',
    'teste98': 'mistyrose',
    'teste99': 'moccasin',
    'teste100': 'navajowhite',
    'teste101': 'navy',
    'teste102': 'oldlace',
    'teste103': 'olive',
    'teste104': 'olivedrab',
    'teste105': 'orange',
    'teste106': 'orangered',
    'teste107': 'orchid',
    'teste108': 'palegoldenrod',
    'teste109': 'palegreen',
    'teste110': 'paleturquoise',
    'teste111': 'palevioletred',
    'teste112': 'papayawhip',
    'teste113': 'peachpuff',
    'teste114': 'peru',
    'teste115': 'pink',
    'teste116': 'plum',
    'teste117': 'powderblue',
    'teste118': 'purple',
    'teste119': 'red',
    'teste120': 'rosybrown',
    'teste121': 'royalblue',
    'teste122': 'saddlebrown',
    'teste123': 'salmon',
    'teste124': 'sandybrown',
    'teste125': 'seagreen',
    'teste126': 'seashell',
    'teste127': 'sienna',
    'teste128': 'silver',
    'teste129': 'skyblue',
    'teste130': 'slateblue',
    'teste131': 'slategray',
    'teste132': 'slategrey',
    'teste133': 'snow',
    'teste134': 'springgreen',
    'teste135': 'steelblue',
    'teste136': 'tan',
    'teste137': 'teal',
    'teste138': 'thistle',
    'teste139': 'tomato',
    'teste140': 'turquoise',
    'teste141': 'violet',
    'teste142': 'wheat',
    'teste143': 'white',
    'teste144': 'whitesmoke',
    'teste145': 'yellow',
    'teste146': 'yellowgreen',
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
        print("Erro ao abrir a webcam")
        exit()

    print("Aguardando QR code... Pressione 'q' para sair")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Não foi possível receber o frame")
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