# ========================
# GRAFICO_BARRA_V.PY
# Gráfico de barras verticales de 1 a 20 elementos con factor de escala
# ========================

from reportlab.pdfgen.canvas import Canvas
from ..settings import COLORS, STYLES, PAGE_WIDTH, PAGE_HEIGHT

# 🎨 Paleta azul
PALETTE = [
    (0x03 / 255, 0x04 / 255, 0x5E / 255),  # #03045E
    (0x02 / 255, 0x3E / 255, 0x8A / 255),  # #023E8A
    (0x00 / 255, 0x77 / 255, 0xB6 / 255),  # #0077B6
    (0x00 / 255, 0x96 / 255, 0xC7 / 255),  # #0096C7
    (0x00 / 255, 0xB4 / 255, 0xD8 / 255),  # #00B4D8
    (0x48 / 255, 0xCA / 255, 0xE4 / 255),  # #48CAE4
    (0x90 / 255, 0xE0 / 255, 0xEF / 255),  # #90E0EF
    (0xAD / 255, 0xE8 / 255, 0xF4 / 255),  # #ADE8F4
    (0xCA / 255, 0xF0 / 255, 0xF8 / 255),  # #CAF0F8
]

# 📐 Parámetros base
MAX_BAR_WIDTH = 120
MIN_BAR_WIDTH = 6
MIN_SPACING = 6
MAX_SPACING = 40


def smart_scale_font(font: tuple, scale: float, min_size: int, base_scale: float = 1.0) -> tuple:
    name, base_size = font
    adjusted_scale = 0.75 + 0.5 * scale if scale < 1 else 1 + 0.5 * (scale - 1)
    scaled_size = max(int(base_size * adjusted_scale), min_size)
    return (name, scaled_size)


def draw_vertical_bar_chart(
    canvas: Canvas,
    x: float,
    y: float,
    data: list[tuple[str, float]],
    max_value: float = 100.0,
    height: float = 120,
    scale: float = 1.0,
    width: float = None,  # ← Nuevo parámetro
    title: str = None,
    label_font: tuple = STYLES["barras_v_text"],
    value_font: tuple = STYLES["porcentaje_barras_vertical"],
    title_font: tuple = STYLES["barras_v_title"],
    subtitle_font: tuple = STYLES["barras_v_subtitle"],
    show_border: bool = False
):
    if not 1 <= len(data) <= 20:
        raise ValueError("El gráfico debe contener entre 1 y 20 datos.")

    n = len(data)
    scaled_height = height * scale
    top_padding = 25 * scale
    bottom_padding = 34 * scale

    # Escalar fuentes
    label_font = smart_scale_font(label_font, scale, min_size=7)
    value_font = smart_scale_font(value_font, scale, min_size=8)
    title_font = smart_scale_font(title_font, scale, min_size=10)
    subtitle_font = smart_scale_font(subtitle_font, scale, min_size=8)

    scaled_min_spacing = int(MIN_SPACING * scale)
    scaled_max_spacing = int(MAX_SPACING * scale)

    # Determinar bar_width y spacing
    if width is not None:
        total_spacing = scaled_min_spacing * (n - 1)
        available_width = max(width - total_spacing, 1)
        bar_width = available_width / n
        spacing = scaled_min_spacing
    else:
        best_bar_width = MIN_BAR_WIDTH
        best_spacing = scaled_min_spacing
        width_found = None

        for bar_width in range(MAX_BAR_WIDTH, MIN_BAR_WIDTH - 1, -1):
            for spacing in range(scaled_max_spacing, scaled_min_spacing - 1, -1):
                test_width = ((bar_width * scale) * n) + ((spacing * scale) * (n - 1))
                if test_width <= PAGE_WIDTH * 0.9:
                    best_bar_width = bar_width
                    best_spacing = spacing
                    width_found = test_width
                    break
            if width_found:
                break

        if width_found is None:
            bar_width = MIN_BAR_WIDTH * scale
            spacing = scaled_min_spacing * scale
            width = (bar_width * n) + (spacing * (n - 1))
        else:
            bar_width = best_bar_width * scale
            spacing = best_spacing * scale
            width = width_found

    start_x = x + (width - ((bar_width * n) + (spacing * (n - 1)))) / 2
    border_height = scaled_height + top_padding + bottom_padding

    if title:
        font_name, font_size = title_font
        canvas.setFont(font_name, font_size)
        canvas.setFillColor(COLORS["black"])
        title_y = y + scaled_height + top_padding + 5 * scale
        canvas.drawCentredString(x + width / 2, title_y, title.upper())

        explanation = (
            "Facilita una comparación sencilla entre los objetivos y ayuda a identificar "
            "dónde se tienen fortalezas o aspectos que requieren mayor atención."
        )
        canvas.setFont(*subtitle_font)
        canvas.setFillColor(COLORS.get("gray", (0.5, 0.5, 0.5)))
        from reportlab.lib.utils import simpleSplit
        scaled_text_width = width * 0.95
        wrapped_lines = simpleSplit(explanation, subtitle_font[0], subtitle_font[1], scaled_text_width)
        line_height = max(subtitle_font[1] * 1.2, 10)

        for i, line in enumerate(wrapped_lines):
            canvas.drawCentredString(x + width / 2, title_y - (line_height * (i + 1)), line)

    if show_border:
        canvas.setStrokeColor(COLORS["black"])
        canvas.rect(x, y - bottom_padding, width, border_height, stroke=0, fill=0)

    for i, (label, value) in enumerate(data):
        x_bar = start_x + i * (bar_width + spacing)
        bar_height = (value / max_value) * scaled_height

        # Fondo gris claro
        canvas.setFillColor(COLORS["light_gray"])
        canvas.rect(x_bar, y, bar_width, scaled_height, stroke=0, fill=0)

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
            canvas.drawCentredString(text_x, y + bar_height + 6 * scale, percent_text)
        else:
            canvas.setFillColor(COLORS["white"])
            canvas.drawCentredString(
                text_x,
                y + bar_height / 2 - value_font[1] / 2 + 1 * scale,
                percent_text
            )

        # Etiqueta
        canvas.setFont(*label_font)
        canvas.setFillColor(COLORS["gray_text"])
        max_line_width = bar_width + 8 * scale
        lines = split_text(label, canvas, label_font[0], label_font[1], max_line_width)

        for j, line in enumerate(lines[:6]):
            canvas.drawCentredString(
                text_x,
                y - 14 * scale - j * (label_font[1] + 1 * scale),
                line
            )


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
