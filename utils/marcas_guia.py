from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from pdf_generator.settings import PAGE_WIDTH, PAGE_HEIGHT  # ✅ Usa el tamaño definido centralmente

def draw_guia_margenes(canvas: Canvas, padding: int = 60):
    """
    Dibuja líneas guía alrededor de la hoja y líneas horizontales/verticales adicionales.
    ⚠️ IMPORTANTE: esta función debe ser llamada al FINAL del flujo de dibujo para que
    las líneas se superpongan sobre cualquier otro elemento del PDF.
    
    :param canvas: objeto canvas de ReportLab
    :param padding: margen desde los bordes (por defecto 60pt ≈ 2.1cm)
    """

    # 🔲 Líneas de margen (rojo punteado)
    canvas.setStrokeColor(colors.red)
    canvas.setLineWidth(0.5)
    canvas.setDash(2, 3)  # patrón de línea punteada: 2pt línea, 3pt espacio

    canvas.line(padding, PAGE_HEIGHT - padding, PAGE_WIDTH - padding, PAGE_HEIGHT - padding)  # Superior
    canvas.line(padding, padding, PAGE_WIDTH - padding, padding)                             # Inferior
    canvas.line(padding, padding, padding, PAGE_HEIGHT - padding)                            # Izquierda
    canvas.line(PAGE_WIDTH - padding, padding, PAGE_WIDTH - padding, PAGE_HEIGHT - padding)  # Derecha

    canvas.setDash([])  # 💡 Restablece el patrón a línea sólida
"""
    # ⬜ Líneas horizontales (gris)
    lineas_gray_y = [645, 495]
    canvas.setStrokeColor(colors.gray)
    for y in lineas_gray_y:
        canvas.line(0, y, PAGE_WIDTH, y)
    
    # 🟧 Línea horizontal adicional (naranja)
    lineas_orange_y = [620, 520]
    canvas.setStrokeColor(colors.orange)
    for y in lineas_orange_y:
        canvas.line(0, y, PAGE_WIDTH, y)

    # ⬜ Líneas verticales (gris)
    lineas_gris_x = [50, 180, 225, 545]
    canvas.setStrokeColor(colors.gray)
    for x in lineas_gris_x:
        canvas.line(x, 0, x, PAGE_HEIGHT)
"""