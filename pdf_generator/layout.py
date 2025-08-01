# 🎨 El diseñador: funciones para dibujar encabezado, pie, logos, etc.
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import black, Color
from .settings import PAGE_WIDTH, PAGE_HEIGHT, STYLES, ASSETS_DIR, COLORS
from utils.marcas_guia import draw_guia_margenes
import os

def draw_header(canvas: Canvas, title: str):
    draw_guia_margenes(canvas, padding=60)

    # 🧭 Altura y posición del header
    header_height = 132
    header_y = PAGE_HEIGHT - header_height

    # 🖼 Imagen de fondo
    header_img_path = os.path.join(ASSETS_DIR, "header.png")
    canvas.drawImage(
        header_img_path,
        x=0,
        y=header_y,
        width=PAGE_WIDTH,
        height=header_height,
        preserveAspectRatio=True,
        mask='auto'
    )

    # 🟦 Capa oscura semitransparente sobre el fondo
    overlay_color = Color(21/255, 31/255, 61/255, alpha=0.7)
    canvas.setFillColor(overlay_color)
    canvas.rect(0, header_y, PAGE_WIDTH, header_height, fill=1, stroke=0)

    # 🧷 Logo centrado
    logo_path = os.path.join(ASSETS_DIR, "header-logo.png")
    logo_width = 270
    logo_height = 65
    logo_x = (PAGE_WIDTH - logo_width) / 2 + 10
    logo_y = header_y + (header_height - logo_height) / 2 + 10

    canvas.drawImage(
        logo_path,
        x=logo_x,
        y=logo_y,
        width=logo_width,
        height=logo_height,
        preserveAspectRatio=True,
        mask='auto'
    )

    # 📝 Subtítulo centrado (ejemplo)
    subtitle = "RETROALIMENTACIÓN DE RESULTADOS"
    font_name, font_size = STYLES["section_header"]
    canvas.setFont(font_name, font_size)
    canvas.setFillColor(COLORS["white"])

    text_width = canvas.stringWidth(subtitle, font_name, font_size)
    text_x = (PAGE_WIDTH - text_width) / 2
    text_y = header_y + 12  # cerca del borde inferior del header

    canvas.drawString(text_x, text_y, subtitle)


def draw_footer(canvas: Canvas, text: str):
    footer_height = 84
    footer_y = 0  # base de la página

    # Puedes usar esta zona como área visual si agregas fondo o marcas
    # Ejemplo: futura franja o imagen si lo necesitas

    # 📝 Texto en esquina inferior izquierda
    canvas.setFont(*STYLES["paragraph"])
    canvas.setFillColor(black)
    canvas.drawString(72, footer_y + 30, text)
