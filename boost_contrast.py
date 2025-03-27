from PIL import Image, ImageEnhance
import sys
import os

def enhance_contrast(image_path: str, output_path: str = None, factor: float = 1.5):
    try:
        image = Image.open(image_path)
        enhancer = ImageEnhance.Contrast(image)
        enhanced = enhancer.enhance(factor)

        if not output_path:
            base, ext = os.path.splitext(image_path)
            output_path = f"{base}_contrast{ext}"

        enhanced.save(output_path)
        print(f"✅ Contraste amélioré et enregistré dans : {output_path}")
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Utilisation : python boost_contrast.py <image_path> [facteur]")
    else:
        path = sys.argv[1]
        factor = float(sys.argv[2]) if len(sys.argv) > 2 else 1.5
        enhance_contrast(path, factor=factor)
