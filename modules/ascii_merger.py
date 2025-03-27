from typing import List, Union, Tuple

def merge_ascii_with_qr(
    ascii_image: List[str],
    qr_ascii: List[str],
    position: Union[str, Tuple[int, int]],
    padding: int = 1
) -> List[str]:

    img_height = len(ascii_image)
    img_width = max(len(line) for line in ascii_image)
    qr_height = len(qr_ascii)
    qr_width = max(len(line) for line in qr_ascii)

    # Calcul de la position d'insertion
    if isinstance(position, str):
        position = position.lower()
        if position == "top-left":
            row, col = padding, padding
        elif position == "top-right":
            row, col = padding, img_width - qr_width - padding
        elif position == "bottom-left":
            row, col = img_height - qr_height - padding, padding
        elif position == "bottom-right":
            row, col = img_height - qr_height - padding, img_width - qr_width - padding
        elif position == "center":
            row, col = (img_height - qr_height) // 2, (img_width - qr_width) // 2
        else:
            raise ValueError(f"Position symbolique inconnue : {position}")
    elif isinstance(position, tuple) and len(position) == 2:
        row, col = position
    else:
        raise ValueError("Position invalide")

    # Vérification de l'espace
    if row < 0 or col < 0 or row + qr_height > img_height or col + qr_width > img_width:
        raise ValueError("QR code dépasse les limites de l'image ASCII")

    # Fusion des deux ASCII
    merged_image = ascii_image.copy()
    merged_image = [line.ljust(img_width) for line in merged_image]  # Padding droite

    for i in range(qr_height):
        line_index = row + i
        original_line = merged_image[line_index]
        qr_line = qr_ascii[i]
        new_line = (
            original_line[:col] +
            qr_line +
            original_line[col + len(qr_line):]
        )
        merged_image[line_index] = new_line

    return merged_image
