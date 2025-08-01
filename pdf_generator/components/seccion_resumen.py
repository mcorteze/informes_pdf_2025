# ========================
# IMPORTACIONES Y CONSTANTES
# ========================
from reportlab.pdfgen.canvas import Canvas
from reportlab.graphics.shapes import Drawing, Circle, String
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from ..settings import COLORS, STYLES, PAGE_WIDTH, PAGE_HEIGHT
from .grafico_resumen import draw_comparative_bars

CHECK_ICON_RADIUS = 6
CHECK_ICON_OFFSET_X = 0
CHECK_ICON_CENTER_Y_OFFSET = 0


# ========================
# FUNCIONES AUXILIARES
# ========================

## 🔤 Ajuste de texto largo en múltiples líneas
def wrap_text(text, canvas, font_name, font_size, max_width):
    canvas.setFont(font_name, font_size)
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if canvas.stringWidth(test_line, font_name, font_size) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    return lines


# ========================
# COMPONENTES GRÁFICOS
# ========================

## ✔️ Ícono de check dentro de un círculo
def draw_check_icon(canvas: Canvas, x: float, y: float):
    canvas.setStrokeColor(COLORS["duoc_darkblue_cmyk"])
    canvas.setFillColor(COLORS["duoc_darkblue_cmyk"])
    canvas.circle(x, y, CHECK_ICON_RADIUS, stroke=1, fill=1)
    canvas.setFillColor(COLORS["white"])
    canvas.setFont("Murecho-Black", 8)
    canvas.drawCentredString(x, y - 3, "✔")


## 🏷️ Bloque de etiqueta + valor (ya no usado directamente, reemplazado por draw_check_group)
def draw_label_value(canvas: Canvas, x: float, y: float, label: str, value: str, max_width: int = 150):
    font_lbl, size_lbl = STYLES["label"]
    font_val, size_val = STYLES["label_value"]
    y_lbl = y
    y_val = y - 10

    draw_check_icon(canvas, x + CHECK_ICON_OFFSET_X, y_lbl + CHECK_ICON_CENTER_Y_OFFSET)

    canvas.setFont(font_lbl, size_lbl)
    canvas.setFillColor(COLORS["duoc_midblue_cmyk"])
    canvas.drawString(x + 12, y_lbl, label)

    lines = wrap_text(value, canvas, font_val, size_val, max_width)
    canvas.setFont(font_val, size_val)
    canvas.setFillColor(COLORS["black"])
    for i, line in enumerate(lines):
        canvas.drawString(x + 12, y_val - (i * (size_val + 2)), line)


## 📦 Grupo completo: check + etiqueta + valor
def draw_check_group(canvas: Canvas, x: float, y: float, label: str, value: str, max_width: int = 150):
    draw_check_icon(canvas, x + CHECK_ICON_OFFSET_X, y + CHECK_ICON_CENTER_Y_OFFSET)

    font_lbl, size_lbl = STYLES["label"]
    font_val, size_val = STYLES["label_value"]

    y_lbl = y
    y_val = y - 14

    canvas.setFont(font_lbl, size_lbl)
    canvas.setFillColor(COLORS["duoc_midblue_cmyk"])
    canvas.drawString(x + 12, y_lbl, label)

    lines = wrap_text(value, canvas, font_val, size_val, max_width)
    canvas.setFont(font_val, size_val)
    canvas.setFillColor(COLORS["black"])
    for i, line in enumerate(lines):
        canvas.drawString(x + 12, y_val - i * (size_val + 2), line)


## 🧾 Grupo completo: etiqueta de nota + valor + estado
def draw_nota_group(canvas: Canvas, x: float, y: float, nota_label: str, nota_valor: str, estado: str):
    canvas.setFont(*STYLES["highlight_label"])
    canvas.setFillColor(COLORS["black"])
    canvas.drawString(x + 8, y, nota_label)

    canvas.setFont(*STYLES["nota_value"])
    canvas.setFillColor(COLORS["duoc_darkblue_cmyk"])
    canvas.drawString(x + 8, y - 39, str(nota_valor))

    canvas.setFont(*STYLES["highlight_label"])
    canvas.setFillColor(COLORS["black"])
    canvas.drawString(x + 8, y - 60, estado)


## 💬 Texto motivacional justificado en un frame
def draw_motivational_text(canvas: Canvas, x: float, y: float, mensaje: str, max_width: int = 280, max_height: int = 100):
    font_name, font_size = STYLES["paragraph"]

    style = ParagraphStyle(
        name="Justify",
        fontName=font_name,
        fontSize=font_size,
        leading=font_size + 2,
        textColor=COLORS["duoc_midblue_cmyk"],
        alignment=TA_JUSTIFY
    )

    paragraph = Paragraph(mensaje, style)
    frame = Frame(300, 741, max_width, max_height, showBoundary=0)
    frame.addFromList([paragraph], canvas)


# ========================
# COMPONENTE PRINCIPAL DE SECCIÓN
# ========================

## 🧩 Dibuja el resumen completo de la sección
def draw_seccion_resumen(canvas: Canvas, x: float, y: float, datos: dict):
    LEFT_X = x
    RIGHT_X = x + 240

    # 🟦 Título principal
    if "main_title" in datos:
        canvas.setFont(*STYLES["main_title"])
        canvas.setFillColor(COLORS["duoc_darkblue_pantone"])
        canvas.drawCentredString(PAGE_WIDTH / 2, 965, datos["main_title"])

    # 🟪 Subtítulo
    if "sub_title" in datos:
        canvas.setFont(*STYLES["sub_title"])
        canvas.setFillColor(COLORS["duoc_midblue_pantone"])
        canvas.drawCentredString(PAGE_WIDTH / 2, 945, datos["sub_title"])

    # 🧷 Bloques laterales con check (sede, sección, profesor)
    draw_check_group(canvas, 70, 894, "Sede", datos["sede"])
    draw_check_group(canvas, 70, 857, "Sección", datos["seccion"])
    draw_check_group(canvas, 70, 820, "Profesor", datos["profesor"], max_width=180)

    # 🧾 Grupo de nota + estado
    if "nota_label" in datos:
        draw_nota_group(
            canvas,
            x=306,
            y=910,
            nota_label=datos["nota_label"],
            nota_valor=datos["nota"],
            estado=datos["estado"]
        )

    # 📊 Gráfico comparativo de barras
    draw_comparative_bars(
        canvas,
        x=482,
        y=897,
        prom_sec=float(datos["promedio_seccion"]),
        prom_alu=float(datos["promedio_alumno"]),
        show_border=False,
    )

    # 💬 Texto motivacional al pie
    draw_motivational_text(canvas, 223, 566, datos["mensaje"], max_width=410)
