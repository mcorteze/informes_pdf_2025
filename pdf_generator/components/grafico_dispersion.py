from collections import defaultdict
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import simpleSplit
from ..settings import COLORS, STYLES

def grafico_dispersion(
    canvas: Canvas,
    x: float,
    y: float,
    notas: list[float],
    nota_alumno: float = None,
    width: float = 500,
    height: float = 60,
    title: str = "Distribución de Notas",
    point_radius: float = 4.5,
    min_score: float = 1.0,
    max_score: float = 7.0,
    font: tuple = STYLES.get("ejes_text", ("Helvetica", 9))
):
    """
    Gráfico de dispersión con título, texto explicativo y leyenda.
    """

    line_height = font[1] + 2
    current_y = y + height + 42  # espacio justo encima del gráfico

    # 🏷 Título
    canvas.setFont(*font)
    canvas.setFillColor(COLORS["black"])
    canvas.drawCentredString(x + width / 2, current_y + 10, title.upper())

    # 📝 Texto explicativo
    explanation = (
        "Ofrece una visión general de cómo se distribuyen las calificaciones en el curso. "
        "Observarás diferentes puntos que representan las notas de tus compañeros. "
        "Aunque recuerda que cada estudiante tiene su propio progreso y trayectoria."
    )
    canvas.setFont(*font)
    canvas.setFillColor(COLORS.get("gray", (0.5, 0.5, 0.5)))
    wrapped_lines = simpleSplit(explanation, font[0], font[1], 420)
    for line in wrapped_lines:
        current_y -= line_height
        canvas.drawString(x, current_y + 5, line)

    # 🧭 Leyenda de puntos (justo encima del gráfico)
    current_y -= (line_height + 4)
    leyenda_y = current_y
    spacing = 110

    # Punto rojo (Tu resultado)
    canvas.setFillColorRGB(0.925, 0.6, 0.6)
    canvas.setStrokeColorRGB(220 / 255, 38 / 255, 38 / 255)
    canvas.circle(x + 10, leyenda_y, point_radius, fill=1, stroke=1)
    canvas.setFillColor(COLORS["black"])
    canvas.drawString(x + 20, leyenda_y - 3, "Tu resultado")

    # Punto celeste (Otros resultados)
    canvas.setFillColorRGB(0.735, 0.933, 0.919)
    canvas.setStrokeColorRGB(28 / 255, 218 / 255, 191 / 255)
    canvas.circle(x + spacing, leyenda_y, point_radius, fill=1, stroke=1)
    canvas.setFillColor(COLORS["black"])
    canvas.drawString(x + spacing + 10, leyenda_y - 3, "Otros resultados")

    # 📊 GRÁFICO DE DISPERSIÓN
    center_y = y + height / 2
    eje_y = y

    # Contorno del gráfico
    canvas.setStrokeColor(COLORS.get("gray", (0.7, 0.7, 0.7)))
    canvas.setLineWidth(0.5)
    canvas.rect(x, y, width, height, stroke=0, fill=0)

    # Eje horizontal
    canvas.setStrokeColor(COLORS["gray_text"])
    canvas.line(x, eje_y, x + width, eje_y)

    # Escala
    canvas.setFont(*font)
    for nota in range(int(min_score), int(max_score) + 1):
        xpos = x + ((nota - min_score) / (max_score - min_score)) * width
        canvas.setStrokeColor(COLORS["gray_text"])
        canvas.line(xpos, eje_y, xpos, eje_y + 4)
        canvas.setFillColor(COLORS["gray_text"])
        canvas.drawCentredString(xpos, eje_y - 10, f"{nota}")

    # Agrupar puntos (excepto alumno)
    bins = defaultdict(list)
    for score in notas:
        if nota_alumno is not None and abs(score - nota_alumno) < 0.05:
            continue
        key = round(score, 1)
        bins[key].append(score)

    max_offset = (height / 2) - point_radius - 2

    for key, valores in bins.items():
        xpos = x + ((key - min_score) / (max_score - min_score)) * width
        n = len(valores)
        if n == 1:
            offsets_y = [0]
        else:
            step = point_radius * 2 + 2
            span = (n - 1) * step / 2
            if span > max_offset:
                step = (2 * max_offset) / max(n - 1, 1)
            offsets_y = [((i - (n - 1) / 2) * step) for i in range(n)]

        for offset_y in offsets_y:
            cy = center_y + offset_y
            canvas.setFillColorRGB(0.735, 0.933, 0.919)
            canvas.setStrokeColorRGB(28 / 255, 218 / 255, 191 / 255)
            canvas.setLineWidth(0.6)
            canvas.circle(xpos, cy, point_radius, fill=1, stroke=1)

    # Punto del alumno
    if nota_alumno is not None:
        xpos = x + ((nota_alumno - min_score) / (max_score - min_score)) * width
        canvas.setFillColorRGB(0.925, 0.6, 0.6)
        canvas.setStrokeColorRGB(220 / 255, 38 / 255, 38 / 255)
        canvas.setLineWidth(0.9)
        canvas.circle(xpos, center_y, point_radius + 0.5, fill=1, stroke=1)
