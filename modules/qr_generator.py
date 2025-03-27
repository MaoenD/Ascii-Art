import qrcode
from typing import List

def generate_qr_ascii(data: str, box_size: int = 2) -> List[str]:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=1,
        border=1 
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert("1")

    ascii_lines = []
    for y in range(qr_img.size[1]):
        line = ""
        for x in range(qr_img.size[0]):
            pixel = qr_img.getpixel((x, y))
            char = "█" if pixel == 0 else " "
            line += char * box_size
        for _ in range(box_size):
            ascii_lines.append(line)

    return ascii_lines
