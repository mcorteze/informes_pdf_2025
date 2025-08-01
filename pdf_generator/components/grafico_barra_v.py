# ========================
# GRAFICO_BARRA_V.PY
# Gráfico de barras verticales de 1 a 20 elementos
# ========================

from reportlab.pdfgen.canvas import Canvas
from ..settings import COLORS, STYLES, PAGE_WIDTH, PAGE_HEIGHT

# 🎨 Paleta azul basada en la imagen proporcionada
PALETTE = [
    (0x03/255, 0x04/255, 0x5E/255),  # #03045E
    (0x02/255, 0x3E/255, 0x8A/255),  # #023E8A
    (0x00/255, 0x77/255, 0xB6/255),  # #0077B6
    (0x00/255, 0x96/255, 0xC7/255),  # #0096C7
    (0x00/255, 0xB4/255, 0xD8/255),  # #00B4D8
    (0x48/255, 0xCA/255, 0xE4/255),  # #48CAE4
    (0x90/255, 0xE0/255, 0xEF/255),  # #90E0EF
    (0xAD/255, 0xE8/255, 0xF4/255),  # #ADE8F4
    (0xCA/255, 0xF0/255, 0xF8/255),  # #CAF0F8
]

# 🎛 Parámetros configurables
MAX_BAR_WIDTH = 120
MIN_BAR_WIDTH = 6
MIN_SPACING = 6
MAX_SPACING = 40

def draw_vertical_bar_chart(
    canvas: Canvas,
    x: float,
    y: float,
    data: list[tuple[str, float]],
    max_value: float = 100.0,
    width: float = 400,
    height: float = 120,
    title: str = None,
    label_font: tuple = STYLES["barras_v_text"],
    value_font: tuple = STYLES["porcentaje_barras_vertical"],
    title_font: tuple = STYLES["barras_v_sub_title"],
    show_border: bool = False
):
    if not 1 <= len(data) <= 20:
        raise ValueError("El gráfico debe contener entre 1 y 20 datos.")

    n = len(data)

    # Cálculo dinámico de ancho y espaciado
    # Probar múltiples combinaciones para ajustarse al width total
    best_bar_width = MIN_BAR_WIDTH
    best_spacing = MIN_SPACING
    for bar_width in range(MAX_BAR_WIDTH, MIN_BAR_WIDTH - 1, -1):
        total_bars_width = bar_width * n
        remaining_space = width - total_bars_width
        if remaining_space < MIN_SPACING * (n - 1):
            continue
        spacing = min(remaining_space / (n - 1 if n > 1 else 1), MAX_SPACING)
        best_bar_width = bar_width
        best_spacing = spacing
        break

    bar_width = best_bar_width
    spacing = best_spacing

    total_chart_width = (bar_width * n) + (spacing * (n - 1))
    start_x = x + (width - total_chart_width) / 2  # centrado

    top_padding = 25
    bottom_padding = 34
    border_height = height + top_padding + bottom_padding

    if title:
        font_name, font_size = title_font
        canvas.setFont(font_name, font_size)
        canvas.setFillColor(COLORS["black"])
        title_y = y + height + top_padding + 5
        canvas.drawCentredString(x + width / 2, title_y, title.upper())

        # Texto explicativo justo debajo del título
        explanation = (
            "Facilita una comparación sencilla entre los objetivos y ayuda a identificar "
            "dónde se tienen fortalezas o aspectos que requieren mayor atención."
        )
        explanation_font = label_font  # puedes usar otro estilo si prefieres
        canvas.setFont(*explanation_font)
        canvas.setFillColor(COLORS.get("gray", (0.5, 0.5, 0.5)))
        line_height = explanation_font[1] + 8
        from reportlab.lib.utils import simpleSplit
        wrapped_lines = simpleSplit(explanation, explanation_font[0], explanation_font[1], width)

        for i, line in enumerate(wrapped_lines):
            canvas.drawString(x, title_y - (line_height * (i + 1)), line)
    
    if show_border:
        canvas.setStrokeColor(COLORS["black"])
        canvas.rect(x, y - bottom_padding, width, border_height, stroke=0, fill=0)

    for i, (label, value) in enumerate(data):
        x_bar = start_x + i * (bar_width + spacing)
        bar_height = (value / max_value) * height

        # Fondo gris claro
        canvas.setFillColor(COLORS["light_gray"])
        canvas.rect(x_bar, y, bar_width, height, stroke=0, fill=0)

        # Barra de color
        color = PALETTE[i % len(PALETTE)]
        canvas.setFillColorRGB(*color)
        canvas.rect(x_bar, y, bar_width, bar_height, stroke=0, fill=1)

        # Porcentaje
        canvas.setFont(*value_font)
        percent_text = f"{value:.0f}%"
        text_x = x_bar + bar_width / 2

        if value < 10:
            canvas.setFillColor(COLORS["black"])
            canvas.drawCentredString(text_x, y + bar_height + 6, percent_text)
        else:
            canvas.setFillColor(COLORS["white"])
            canvas.drawCentredString(text_x, y + bar_height / 2 - value_font[1] / 2 + 1, percent_text)

        # Etiqueta
        canvas.setFont(*label_font)
        canvas.setFillColor(COLORS["gray_text"])
        max_line_width = bar_width + 8
        lines = split_text(label, canvas, label_font[0], label_font[1], max_line_width)
        for j, line in enumerate(lines[:6]):
            canvas.drawCentredString(text_x, y - 14 - j * (label_font[1] + 1), line)

def split_text(text: str, canvas: Canvas, font_name: str, font_size: int, max_width: float) -> list[str]:
    canvas.setFont(font_name, font_size)
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = (current + " " + word).strip()
        if canvas.stringWidth(test, font_name, font_size) <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines
