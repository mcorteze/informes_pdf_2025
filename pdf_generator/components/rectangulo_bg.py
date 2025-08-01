# ========================
# RECTANGULO_BG.PY
# Componente visual de fondo para secciones
# ========================

from reportlab.pdfgen.canvas import Canvas
from ..settings import PAGE_WIDTH, COLORS

# 🎛 Altura modificable (en puntos)
altura_bg = 309  # Para ajustar la altura del rectángulo

def rectangulo_bg(canvas: Canvas, y: float, height: float = altura_bg):
    """
    Dibuja un rectángulo de fondo con color 'celeste_bg' a lo largo de toda la página.
    
    Parámetros:
    - canvas: objeto Canvas de ReportLab
    - y: coordenada vertical (posición superior del rectángulo)
    - height: alto del rectángulo (por defecto `altura_bg`)
    """
    color_fondo = COLORS["celeste_bg"]

    canvas.setFillColor(color_fondo)
    canvas.setStrokeColor(color_fondo)
    canvas.rect(0, y - height, PAGE_WIDTH, height, fill=1, stroke=0)
