from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import simpleSplit
from ..settings import COLORS, STYLES

def draw_tabla_basica(
    canvas: Canvas,
    x: float,
    y: float,
    data: dict,
    col_widths: list[float],
    alignments: list[str],
    scale: float = 1.0,
):
    titulo = data.get("titulo", "")
    subtitulo = data.get("subtitulo", "")
    headers = data["titulos"]
    rows = data["valores"]

    assert len(headers) == len(col_widths) == len(alignments), "Headers, col_widths y alignments deben tener igual longitud"

    # Escalar fuentes desde STYLES
    font_title = _scaled_font(STYLES["table_b_title"], scale)
    font_sub = _scaled_font(STYLES["table_b_subtitle"], scale)
    font_header = _scaled_font(STYLES["table_b_header"], scale)
    font_cell = _scaled_font(STYLES["table_b_cell"], scale)

    current_y = y
    total_width = sum(col_widths)
    padding_y = 6 * scale
    padding_x = 5  # ← Padding horizontal fijo de 3 pt (equivale a ~pixel)

    # 🟦 Título
    if titulo:
        canvas.setFont(*font_title)
        canvas.setFillColor(COLORS["black"])
        canvas.drawCentredString(x + total_width / 2, current_y, titulo.upper())
        current_y -= 18 * scale

    # 🟪 Subtítulo
    if subtitulo:
        canvas.setFont(*font_sub)
        canvas.setFillColor(COLORS.get("gray", (0.4, 0.4, 0.4)))
        canvas.drawCentredString(x + total_width / 2, current_y, subtitulo)
        current_y -= 14 * scale

    # 🟥 Encabezado centrado
    canvas.setFont(*font_header)
    header_lines = []
    max_header_height = 0

    for i, header in enumerate(headers):
        col_x = x + sum(col_widths[:i])
        col_w = col_widths[i]
        lines = simpleSplit(str(header), font_header[0], font_header[1], col_w - 2 * padding_x)
        header_lines.append(lines)
        max_header_height = max(max_header_height, len(lines) * (font_header[1] + 1))

    row_height = max_header_height + padding_y

    for i, lines in enumerate(header_lines):
        col_x = x + sum(col_widths[:i])
        col_w = col_widths[i]

        # Fondo
        canvas.setFillColor(COLORS["duoc_darkblue_cmyk"])
        canvas.rect(col_x, current_y - row_height, col_w, row_height, fill=1, stroke=0)

        # Texto
        canvas.setFillColor(COLORS["white"])
        start_y = current_y - (row_height - len(lines) * (font_header[1] + 1)) / 2 - font_header[1]
        for j, line in enumerate(lines):
            y_line = start_y - j * (font_header[1] + 1)
            _draw_text(canvas, line, font_header, col_x, col_w, y_line, align="center", padding_x=padding_x)

        # Borde
        canvas.setStrokeColor(COLORS["black"])
        canvas.rect(col_x, current_y - row_height, col_w, row_height, fill=0, stroke=1)

    current_y -= row_height

    # 🟩 Filas
    canvas.setFont(*font_cell)
    for row in rows:
        cell_lines = []
        row_heights = []

        for i, cell in enumerate(row):
            col_w = col_widths[i]
            lines = simpleSplit(str(cell), font_cell[0], font_cell[1], col_w - 2 * padding_x)
            cell_lines.append(lines)
            row_heights.append(len(lines) * (font_cell[1] + 1))

        row_height = max(row_heights) + padding_y

        for i, lines in enumerate(cell_lines):
            col_x = x + sum(col_widths[:i])
            col_w = col_widths[i]

            # Texto
            canvas.setFillColor(COLORS["black"])
            start_y = current_y - (row_height - len(lines) * (font_cell[1] + 1)) / 2 - font_cell[1]
            for j, line in enumerate(lines):
                y_line = start_y - j * (font_cell[1] + 1)
                _draw_text(canvas, line, font_cell, col_x, col_w, y_line, align=alignments[i], padding_x=padding_x)

            # Borde
            canvas.setStrokeColor(COLORS["black"])
            canvas.rect(col_x, current_y - row_height, col_w, row_height, fill=0, stroke=1)

        current_y -= row_height


def _draw_text(canvas, text: str, font: tuple, x: float, width: float, y: float, align: str, padding_x: float = 3):
    canvas.setFont(*font)
    if align == "left":
        canvas.drawString(x + padding_x, y, text)
    else:  # center
        canvas.drawCentredString(x + width / 2, y, text)


def _scaled_font(font: tuple, scale: float) -> tuple:
    name, size = font
    return (name, int(size * scale))
