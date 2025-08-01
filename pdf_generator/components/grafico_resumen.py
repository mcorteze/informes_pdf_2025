# ===========================
# COMPARATIVE_BARS.PY
# Gráfico comparativo de barras: Promedio Sección vs Alumno
# ===========================

from reportlab.pdfgen.canvas import Canvas
from ..settings import COLORS, STYLES, PAGE_WIDTH

# 🎛️ Parámetros configurables (solo definidos al inicio del módulo)
BAR_HEIGHT = 18         # Grosor de cada barra
BAR_GAP = 2             # Separación vertical entre las barras
BAR_WIDTH_MAX = 140     # Ancho máximo de la barra horizontal
LABEL_OFFSET = 64       # Desplazamiento a la izquierda para etiquetas

# 🔤 Tipografías importadas
LABEL_FONT = STYLES["chart_label"]         # Ej: ("MyriadPro-Cond", 8)
VALUE_FONT = STYLES["chart_number"]        # Ej: ("MyriadPro-BoldCond", 9)

# 🎨 Colores definidos por separado
COLOR_PROM_SEC = COLORS["complementary_navy"]
COLOR_PROM_ALU = COLORS["complementary_bright_blue"]

def draw_comparative_bars(
    canvas: Canvas,
    x: float,
    y: float,
    prom_sec: float,
    prom_alu: float,
    show_border: bool = False
):
    """
    Dibuja barras comparativas del promedio de sección vs alumno (escala sobre 7.0).
    """

    # 🧮 Cálculo de anchos proporcionales
    ancho_sec = max(BAR_WIDTH_MAX * prom_sec / 7.0, 1)
    ancho_alu = max(BAR_WIDTH_MAX * prom_alu / 7.0, 1)

    # 📏 Coordenadas verticales
    y_sec = y
    y_alu = y - (BAR_HEIGHT + BAR_GAP)

    # 🏷️ Etiquetas a la izquierda
    canvas.setFont(*LABEL_FONT)
    canvas.setFillColor(COLORS["gray_text"])
    canvas.drawRightString(x + LABEL_OFFSET, y_sec + 1, "Prom. Sección")
    canvas.drawRightString(x + LABEL_OFFSET, y_alu + 1, "Alumno")

    # 🎨 Barras de fondo
    x_bar = x + LABEL_OFFSET + 8
    canvas.setFillColor(COLORS["light_gray"])
    canvas.rect(x_bar, y_sec, BAR_WIDTH_MAX, BAR_HEIGHT, stroke=0, fill=1)
    canvas.rect(x_bar, y_alu, BAR_WIDTH_MAX, BAR_HEIGHT, stroke=0, fill=1)

    # 🎨 Barras reales
    canvas.setFillColor(COLOR_PROM_SEC)
    canvas.rect(x_bar, y_sec, ancho_sec, BAR_HEIGHT, stroke=0, fill=1)

    canvas.setFillColor(COLOR_PROM_ALU)
    canvas.rect(x_bar, y_alu, ancho_alu, BAR_HEIGHT, stroke=0, fill=1)

    # 🔢 Números dentro de la barra
    canvas.setFont(*VALUE_FONT)
    canvas.setFillColor(COLORS["white"])
    canvas.drawRightString(x_bar + ancho_sec - 4, y_sec + BAR_HEIGHT / 2 - VALUE_FONT[1] / 2 + 1, f"{prom_sec:.1f}")
    canvas.drawRightString(x_bar + ancho_alu - 4, y_alu + BAR_HEIGHT / 2 - VALUE_FONT[1] / 2 + 1, f"{prom_alu:.1f}")

    # 🖼️ Borde opcional
    if show_border:
        canvas.setStrokeColor(COLORS["gray_text"])
        border_height = 2 * BAR_HEIGHT + BAR_GAP + 10
        canvas.rect(x, y_alu - 4, BAR_WIDTH_MAX + LABEL_OFFSET + 16, border_height, stroke=1, fill=0)
