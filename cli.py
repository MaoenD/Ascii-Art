import os
from pathlib import Path
from modules.image_loader import load_image, parse_target_size, resize_image
from modules.ascii_converter import image_to_ascii, get_ascii_palettes
from modules.qr_generator import generate_qr_ascii
from modules.ascii_merger import merge_ascii_with_qr
from modules.ascii_exporter import export_ascii_to_txt, export_ascii_to_terminal, export_ascii_to_pdf

def prompt_input(prompt, default=None, cast=str):
    value = input(f"{prompt} " + (f"[{default}] " if default else ""))
    if not value.strip() and default is not None:
        return default
    try:
        return cast(value.strip())
    except:
        print("Entrée invalide. Réessayez.")
        return prompt_input(prompt, default, cast)

def cli_main():
    print("🎨 ASCII Art QR Generator 🔲")
    print("Bienvenue ! Suivez les étapes pour créer votre œuvre ASCII personnalisée.\n")

    # Étape 1 : Image
    image_path = prompt_input("1. Entrez le chemin de l'image à convertir (ex: ./image.jpg) :")
    image = load_image(image_path)

    # Étape 2 : Format cible
    format_input = prompt_input("2. Entrez le format de sortie (ex: A4, A3 ou dimensions comme 1920x1080 ou 21x29.7) :", "A4")
    if "x" in format_input:
        parts = format_input.split("x")
        width, height = float(parts[0]), float(parts[1])
        unit = prompt_input("   Unité de mesure (px, cm ou mm) :", "cm")
        target_size = parse_target_size((width, height), unit=unit)
    else:
        target_size = parse_target_size(format_input)

    # Étape 3 : Proportions
    keep_ratio = prompt_input("3. Voulez-vous conserver les proportions d'origine ? (oui/non) :", "oui").lower() in ["oui", "o", "yes", "y"]
    image_resized = resize_image(image, target_size, keep_aspect_ratio=keep_ratio)

    # Étape 4 : Palette ASCII
    palettes = get_ascii_palettes()
    print("4. Choisissez un style de rendu (palette ASCII) :")
    for i, name in enumerate(palettes.keys(), start=1):
        print(f"  [{i}] {name}")
    palette_index = int(prompt_input("Votre choix (numéro) :", "1"))
    palette_name = list(palettes.keys())[palette_index - 1]

    # Étape 5 : Taille de sortie ASCII
    output_width = int(prompt_input("5. Largeur souhaitée de l'image ASCII (en caractères, ex: 150) :", 150))
    ascii_img = image_to_ascii(image_resized, output_width=output_width, palette_name=palette_name)

    # Étape 6 : Ajouter un QR code ?
    use_qr = prompt_input("6. Souhaitez-vous ajouter un QR code intégré à l'image ? (oui/non) :", "oui").lower() in ["oui", "o", "yes", "y"]

    if use_qr:
        qr_data = prompt_input("7. Entrez le texte ou l'URL à encoder dans le QR code :")
        qr_position = prompt_input("8. Position du QR dans l'image (top-left, bottom-right, center ou ligne,colonne) :", "bottom-right")
        if "," in qr_position:
            row, col = map(int, qr_position.split(","))
            qr_position = (row, col)
        box_size = int(prompt_input("9. Taille du QR code (valeur entière, ex: 2 pour 2x2) :", 2))
        qr_ascii = generate_qr_ascii(qr_data, box_size=box_size)
        ascii_img = merge_ascii_with_qr(ascii_img, qr_ascii, qr_position)

    # Étape finale : Export
    print("10. Choisissez un format de sortie :\n   [1] Affichage dans le terminal\n   [2] Fichier texte (.txt)\n   [3] Document PDF (.pdf)")
    export_choice = prompt_input("Votre choix :", "3")

    if export_choice == "1":
        export_ascii_to_terminal(ascii_img)
    elif export_choice == "2":
        txt_name = prompt_input("Nom du fichier texte de sortie :", "ascii_output.txt")
        export_ascii_to_txt(ascii_img, txt_name)
        print(f"✅ Exporté dans {txt_name}")
    elif export_choice == "3":
        pdf_name = prompt_input("Nom du fichier PDF de sortie :", "ascii_output.pdf")
        export_ascii_to_pdf(ascii_img, pdf_name)
        print(f"✅ Exporté dans {pdf_name}")

    print("\n🎉 Votre œuvre ASCII est prête. Merci d’avoir utilisé ASCII Art QR Generator !")

if __name__ == "__main__":
    cli_main()
