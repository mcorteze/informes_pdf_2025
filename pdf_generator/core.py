import os
from reportlab.pdfgen.canvas import Canvas
from .settings import OUTPUT_DIR, PAGE_SIZE, PAGE_WIDTH  
from .layout import draw_header, draw_footer
from .components.seccion_resumen import draw_seccion_resumen
from .components.divider import draw_divider  
from .components.grafico_barra_v import draw_vertical_bar_chart
from .components.grafico_dispersion import grafico_dispersion
from .components.grafico_boxplot import grafico_boxplot
from .components.rectangulo_bg import rectangulo_bg

def generate_sample_pdf(filename: str = "ejemplo.pdf"):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)

    canvas = Canvas(filepath, pagesize=PAGE_SIZE)

    draw_header(canvas, "Informe de Ejemplo")
    draw_footer(canvas, "SUDCRA.")

    # 📊 Bloque de resumen
    draw_seccion_resumen(canvas, x=60, y=630, datos={
        "main_title": "PRUEBA 1",
        "sub_title": "NIVELACIÓN MATEMÁTICA",
        "nota_label": "Nota",
        "sede": "VALPARAÍSO",
        "seccion": "MAT1111-004D",
        "profesor": "FRANCIS GLORIA FUENTES CHACANA",
        "nota": "3,6",
        "estado": "Aún no competente",
        "promedio_seccion": 4.9,
        "promedio_alumno": 3.6,
        "mensaje": (
            "Estimado estudiante, ¡No te desanimes por no haber alcanzado el porcentaje mínimo para aprobar\n"
            "la primera prueba de Nivelación Matemática! Cada desafío es una oportunidad para crecer y\n"
            "aprender. Te animo a que aproveches los recursos disponibles y busques apoyo si lo necesitas.\n"
            "¡Tu esfuerzo y dedicación te llevarán lejos!"
        )
    })

    rectangulo_bg(canvas, y=709)

    # ➖ Divider intermedio
    draw_divider(canvas, y=750, text="Aprendizaje")

    # 📈 Gráfico de barras verticales con porcentajes
    width = 550
    draw_vertical_bar_chart(
        canvas,
        x=(PAGE_WIDTH - width) / 2,
        y=500,  # posición vertical base
        data = [
        (
            "Interpretar y construir expresiones algebraicas a partir de\n"
            "situaciones reales o representaciones gráficas, identificando\n"
            "las variables y relaciones relevantes", 32
        ),
        (
            "Analizar y representar patrones de crecimiento aritmético y\n"
            "geométrico, reconociendo regularidades y su expresión simbólica", 55
        ),
        (
            "Evaluar la validez de procedimientos matemáticos utilizados\n"
            "en la resolución de problemas, argumentando con claridad sobre\n"
            "posibles errores o alternativas más eficientes", 67
        ),
        (
            "Relacionar distintos tipos de representaciones (gráfica,\n"
            "simbólica, tabular y verbal) en el estudio de relaciones lineales\n"
            "y no lineales", 21
        ),
        ],
        max_value=100.0,
        height=150,
        width = 550,
        title="Logro promedio por Aprendizajee",
        show_border=True
    )
    """
    # ➖ Divider provisorio
    draw_divider(canvas, y=400, text="DIVIDER PROVISORIO")
    """
    # ➕ Gráfico de dispersión horizontal de notas simuladas
    notas = [2.6, 2.3, 2.6, 3.3, 3.4, 2.5, 4.1, 2.9, 3.5, 3.4, 2.1, 1.8, 3.9, 1.4, 2.4, 4.7, 2.2, 2.0, 2.5, 2.8, 2.5, 2.6, 3.6, 3.0, 2.9, 2.4, 3.3, 3.2, 6.5, 2.7, 2.8, 2.8, 3.9, 4.2, 3.7, 2.8, 7.0, 7.0, 7.0]

    nota_alumno = 3.3

    grafico_dispersion(
        canvas,
        x=60,
        y=180,
        notas=notas,
        nota_alumno=nota_alumno,
        width=400,
        height=100,
        title="DISTRIBUCIÓN DE CALIFICACIONES"
    )

    grafico_boxplot(
        canvas,
        x=60,
        y=180,
        notas=notas,
        nota_alumno=nota_alumno,
        width=400,
        height=100,
        title=""
    )

    canvas.save()
    return filepath
