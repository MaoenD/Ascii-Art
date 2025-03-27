from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

def export_ascii_to_txt(ascii_art, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        for line in ascii_art:
            f.write(line + "\n")

def export_ascii_to_terminal(ascii_art):
    for line in ascii_art:
        print(line)


def export_ascii_to_pdf(ascii_art, file_path, font_size=5, page_size=A4):
    """
    Export ASCII art dans un fichier PDF à l'aide de reportlab (supporte UTF-8).
    """
    c = canvas.Canvas(file_path, pagesize=page_size)
    width, height = page_size

    font_path = "C:/Windows/Fonts/consola.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("Consolas", font_path))
        c.setFont("Consolas", font_size)
    else:
        c.setFont("Courier", font_size)  # fallback

    line_height = font_size * 1.2
    y = height - 20

    for line in ascii_art:
        c.drawString(20, y, line)
        y -= line_height
        if y < 20:
            c.showPage()
            c.setFont("Consolas", font_size)
            y = height - 20

    c.save()
