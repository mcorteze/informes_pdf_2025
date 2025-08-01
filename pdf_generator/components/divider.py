# ========================
# DIVIDER.PY
# Componente visual para separador con texto centrado
# ========================

from reportlab.pdfgen.canvas import Canvas
from ..settings import PAGE_WIDTH, PAGE_HEIGHT, STYLES, ASSETS_DIR, COLORS

## 📏 Divider con texto centrado
def draw_divider(canvas: Canvas, y: float, text: str, height: float = 41):
    """
    Dibuja un divider horizontal con fondo oscuro y texto centrado en blanco.
    
    Parámetros:
    - canvas: objeto Canvas de ReportLab
    - y: coordenada vertical (posición superior del rectángulo)
    - text: texto que se mostrará centrado en el divider
    - height: alto del rectángulo (por defecto 41)
    """

    background_color = COLORS["azul_cristal"]
    text_color = COLORS["white"]

    # 🎨 Rectángulo de fondo
    canvas.setFillColor(background_color)
    canvas.setStrokeColor(background_color)
    canvas.rect(0, y - height, PAGE_WIDTH, height, fill=1, stroke=0)

    # 📝 Texto centrado
    font_name, font_size = STYLES["divider_text"]
    canvas.setFont(font_name, font_size)
    canvas.setFillColor(text_color)

    # 📐 Corrección precisa de alineación vertical
    text_y = y - (height / 2) - (font_size * 0.35)
    canvas.drawCentredString(PAGE_WIDTH / 2, text_y, text.upper())
