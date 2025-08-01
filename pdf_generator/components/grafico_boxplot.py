from reportlab.pdfgen.canvas import Canvas
from ..settings import COLORS, STYLES

def grafico_boxplot(
    canvas: Canvas,
    x: float,
    y: float,
    notas: list[float],
    nota_alumno: float = None,
    width: float = 400,
    height: float = 100,
    title: str = "Box Plot Notas",
    min_score: float = 1.0,
    max_score: float = 7.0,
    font: tuple = STYLES.get("ejes_text", ("Helvetica", 9)),
    thickness_ratio: float = 0.42
):
    """
    Dibuja un gráfico de box plot horizontal con leyenda inferior.
    """
    from statistics import mean, quantiles

    all_notas = notas.copy()
    if nota_alumno is not None:
        all_notas.append(nota_alumno)
    all_notas.sort()

    if len(all_notas) < 4:
        return

    q1, q2, q3 = quantiles(all_notas, n=4)
    iqr = q3 - q1
    lower_fence = max(min_score, q1 - 1.5 * iqr)
    upper_fence = min(max_score, q3 + 1.5 * iqr)

    min_val = min([n for n in all_notas if n >= lower_fence])
    max_val = max([n for n in all_notas if n <= upper_fence])
    outliers = sorted(set(n for n in all_notas if n < lower_fence or n > upper_fence))
    media = mean(all_notas)

    center_y = y + height / 2
    box_half = (height * thickness_ratio) / 2
    whisker_half = box_half * 0.5

    scale = lambda val: x + ((val - min_score) / (max_score - min_score)) * width

    boxplot_color = COLORS["black"]

    # 🏷 Título
    canvas.setFont(*font)
    canvas.setFillColor(COLORS["black"])
    canvas.drawCentredString(x + width / 2, y + height + 16, title.upper())

    # 📦 Caja
    canvas.setStrokeColor(boxplot_color)
    canvas.setLineWidth(1)
    canvas.rect(scale(q1), center_y - box_half, scale(q3) - scale(q1), box_half * 2, fill=0, stroke=1)

    # ➖ Mediana (gris)
    canvas.setStrokeColor(COLORS.get("gray", (0.5, 0.5, 0.5)))
    canvas.setLineWidth(1.2)
    canvas.line(scale(q2), center_y - box_half, scale(q2), center_y + box_half)

    # 📉 Media (línea punteada gris)
    canvas.setDash([2, 2], 0)
    canvas.setLineWidth(1)
    canvas.line(scale(media), center_y - box_half, scale(media), center_y + box_half)
    canvas.setDash([], 0)

    # 📈 Bigotes
    canvas.setStrokeColor(boxplot_color)
    canvas.setLineWidth(0.8)
    canvas.line(scale(min_val), center_y, scale(q1), center_y)
    canvas.line(scale(q3), center_y, scale(max_val), center_y)
    canvas.line(scale(min_val), center_y - whisker_half, scale(min_val), center_y + whisker_half)
    canvas.line(scale(max_val), center_y - whisker_half, scale(max_val), center_y + whisker_half)

    # ✳ Outliers únicos
    canvas.setFont(*font)
    canvas.setFillColor(COLORS["black"])
    for n in outliers:
        canvas.drawCentredString(scale(n), center_y - 5, "*")

    # 📦 Contorno general
    canvas.setStrokeColor(COLORS.get("gray", COLORS.get("gray_text", (0.7, 0.7, 0.7))))
    canvas.setLineWidth(0.5)
    canvas.rect(x, y, width, height, stroke=0, fill=0)

    # 🧾 Leyenda inferior
    leyenda_y = y - 18
    leyenda_font = (font[0], max(font[1] - 1, 6))
    canvas.setFont(*leyenda_font)
    canvas.setFillColor(COLORS.get("gray", (0.5, 0.5, 0.5)))

    texto_leyenda = "— mediana    --- media (promedio)    * valor outlier: dato inusualmente lejano al centro"
    canvas.drawCentredString(x + width / 2, leyenda_y, texto_leyenda)
