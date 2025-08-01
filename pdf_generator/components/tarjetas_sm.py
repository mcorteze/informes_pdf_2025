from reportlab.pdfgen.canvas import Canvas
from ..settings import COLORS

def draw_tarjetas_sm(
    canvas: Canvas,
    x: float,
    y: float,
    valores: dict,
    width: float = 130,
    height: float = 60,
    spacing: float = 18,
    scale: float = 1.0
):
    """
    Dibuja tarjetas compactas de resultados con ícono a la izquierda y número + texto centrado.
    """

    tarjetas = [
        {
            "clave": "correctas",
            "icono": "✔",
            "label": "Correctas",
            "color": COLORS.get("success", (0, 0.6, 0)),
        },
        {
            "clave": "incorrectas",
            "icono": "✖",
            "label": "Incorrectas",
            "color": COLORS.get("error", (1, 0, 0)),
        },
        {
            "clave": "omitidas",
            "icono": "–",
            "label": "Omitidas",
            "color": COLORS.get("gray", (0.5, 0.5, 0.5)),
            "is_circle": True
        }
    ]

    icon_font = ("Murecho-Black", int(20 * scale))
    number_font = ("Helvetica", int(18 * scale))
    label_font = ("Helvetica", int(11 * scale))

    padding = 8 * scale
    icon_box_size = 20 * scale

    # 🔧 Desplazamientos horizontales ajustables
    icon_x_offset = 20 * scale  # <--- Mueve el ícono horizontalmente
    text_x_offset = 70 * scale  # <--- Mueve el bloque número + label horizontalmente

    for i, tarjeta in enumerate(tarjetas):
        cx = x + i * (width + spacing)
        cy = y
        valor = str(valores.get(tarjeta["clave"], 0))
        color = tarjeta["color"]

        # 🔲 Fondo y borde
        canvas.setStrokeColor(color)
        canvas.setLineWidth(1)
        corner_radius = 6
        canvas.roundRect(cx, cy - height, width, height, radius=corner_radius, fill=0, stroke=1)

        center_y = cy - height / 2
        icon_x = cx + icon_x_offset
        text_block_x = cx + text_x_offset

        # 🖼 Ícono
        if tarjeta.get("is_circle"):
            radius = icon_box_size / 2
            icon_center = (icon_x + radius, center_y)
            canvas.setFillColor(COLORS.get("gray", (0.6, 0.6, 0.6)))
            canvas.setStrokeColor(COLORS.get("gray", (0.6, 0.6, 0.6)))
            canvas.circle(*icon_center, radius, stroke=0, fill=1)
            canvas.setFont(*icon_font)
            canvas.setFillColor(COLORS.get("white"))
            canvas.drawCentredString(icon_center[0], icon_center[1] - icon_font[1] / 3, "–")
        else:
            canvas.setFont(*icon_font)
            canvas.setFillColor(color)
            canvas.drawString(icon_x, center_y - icon_font[1] / 2 + 2, tarjeta["icono"])

        # 🎯 Ajuste vertical
        group_height = number_font[1] + label_font[1] + 3
        group_top = center_y + group_height / 2

        # 🧮 Calcular anchos para centrar respecto al texto más largo
        canvas.setFont(*number_font)
        num_width = canvas.stringWidth(valor, *number_font)
        canvas.setFont(*label_font)
        label_width = canvas.stringWidth(tarjeta["label"], *label_font)
        max_width = max(num_width, label_width)

        num_x = text_block_x + (max_width - num_width) / 2
        label_x = text_block_x + (max_width - label_width) / 2

        # 🔢 Número
        canvas.setFont(*number_font)
        canvas.setFillColor(color)
        canvas.drawString(num_x, group_top - number_font[1], valor)

        # 🔤 Etiqueta
        canvas.setFont(*label_font)
        canvas.setFillColor(color)
        canvas.drawString(label_x, group_top - number_font[1] - label_font[1] - 3, tarjeta["label"])
