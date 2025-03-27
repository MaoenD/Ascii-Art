from PIL import Image
from typing import Tuple, Union

STANDARD_FORMATS_CM = {
    "A5": (14.8, 21.0),
    "A4": (21.0, 29.7),
    "A3": (29.7, 42.0),
}

def load_image(path: str) -> Image.Image:
    return Image.open(path)

def cm_to_px(cm: float, dpi: int) -> int:
    return int(cm * dpi / 2.54)

def parse_target_size(
    size_input: Union[str, Tuple[float, float]],
    unit: str = 'px',
    dpi: int = 300
) -> Tuple[int, int]:

    if isinstance(size_input, str):
        if size_input.upper() in STANDARD_FORMATS_CM:
            width_cm, height_cm = STANDARD_FORMATS_CM[size_input.upper()]
            return cm_to_px(width_cm, dpi), cm_to_px(height_cm, dpi)
        else:
            raise ValueError(f"Format I: {size_input}")
    
    elif isinstance(size_input, tuple) and len(size_input) == 2:
        width, height = size_input
        if unit == 'cm':
            return cm_to_px(width, dpi), cm_to_px(height, dpi)
        elif unit == 'mm':
            return cm_to_px(width / 10, dpi), cm_to_px(height / 10, dpi)
        elif unit == 'px':
            return int(width), int(height)
        else:
            raise ValueError(f"Unité I : {unit}")
    else:
        raise TypeError("taille invalide.")

def resize_image(
    image: Image.Image,
    target_size: Tuple[int, int],
    keep_aspect_ratio: bool = True
) -> Image.Image:

    from PIL import Image as PILImage
    if not keep_aspect_ratio:
        return image.resize(target_size, PILImage.Resampling.LANCZOS)

    original_width, original_height = image.size
    target_width, target_height = target_size

    ratio = min(target_width / original_width, target_height / original_height)
    new_width = int(original_width * ratio)
    new_height = int(original_height * ratio)

    return image.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
