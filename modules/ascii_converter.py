from PIL import Image
from typing import List, Dict

def get_ascii_palettes() -> Dict[str, str]:
    """Retourne une sélection de palettes ASCII par nom."""
    return {
        "classic": "@%#*+=-:. ",
        "blocks": "█▓▒░ ",
        "light": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    }

def image_to_ascii(
    image: Image.Image,
    output_width: int,
    palette_name: str = "classic",
    color: bool = False
) -> List[str]:

    palettes = get_ascii_palettes()
    if palette_name not in palettes:
        raise ValueError(f"Palette '{palette_name}' non reconnue. Choix possibles : {list(palettes.keys())}")
    palette = palettes[palette_name]
    palette_len = len(palette)

    # Redimensionnement avec correction du ratio ASCII (~0.5)
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(output_width * aspect_ratio * 0.5)
    image_resized = image.resize((output_width, new_height))

    # Conversion en niveaux de gris
    grayscale_image = image_resized.convert("L")

    # Mapping pixels → caractères ASCII
    ascii_art = []
    for y in range(grayscale_image.height):
        line = ""
        for x in range(grayscale_image.width):
            pixel = grayscale_image.getpixel((x, y))
            char = palette[int(pixel / 255 * (palette_len - 1))]
            line += char
        ascii_art.append(line)

    return ascii_art