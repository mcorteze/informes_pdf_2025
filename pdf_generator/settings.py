# ⚙️ El panel de control: define constantes y estilos usados en todo el sistema
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color
import os

# Tamaño de hoja: personalizado 794x1123 puntos
PAGE_WIDTH = 794
PAGE_HEIGHT = 1123
PAGE_SIZE = (PAGE_WIDTH, PAGE_HEIGHT)


# Rutas base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# Registro de fuentes personalizadas
FONT_VARIANTS = {
    "MyriadPro-Light": "MyriadPro-Light.ttf",
    "MyriadPro-Cond": "MYRIADPRO-COND.ttf",
    "MyriadPro-BoldCond": "MYRIADPRO-BOLDCOND.ttf",
    "NotoSansJapaneseSemiBold": "NotoSansJP-SemiBold.ttf",  # Fuente exclusiva para cifras
    "Murecho-Black": "Murecho-Black.ttf",  # Fuente para
}

for font_name, font_file in FONT_VARIANTS.items():
    font_path = os.path.join(FONTS_DIR, font_file)
    try:
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont(font_name, font_path))
        else:
            print(f"⚠️ No se encontró la fuente: {font_file}")
    except Exception as e:
        print(f"❌ Error registrando {font_name}: {e}")

# 🎨 Paleta de colores institucionales
COLORS = {
    "C": Color(0/255, 117/255, 255/255),
    "duoc_darkblue": Color(0/255, 60/255, 113/255),
    "neutral_gray": Color(70/255, 70/255, 70/255),
    "light_gray": Color(220/255, 220/255, 220/255),
    
    
    "gray_text": Color(0.3, 0.3, 0.3),
    "celeste_bg": Color(230/250, 240/250, 249/250),
    "azul_cristal": Color(61/250, 63/250, 101/250), # Hex: #3d3f65
     
      # Hex: #e6f0f9
    # ======== PALETA ===========
    "black": Color(35/255, 31/255, 32/255), # Hex: #231f20
    "white": Color(255/255, 255/255, 255/255), # Hex: #FFFFFF

    "accent_neutral": Color(61/255, 63/255, 101/255),
    "title_primary": Color(13/255, 59/255, 127/255),
    "subtitle_secondary": Color(7/255, 35/255, 76/255),

    # Colores institucionales Duoc UC
    "duoc_yellow": Color(255/255, 199/255, 44/255),          # Hex: #FFC72C
    "duoc_darkblue_pantone": Color(0/255, 40/255, 85/255),   # Hex: #002855
    "duoc_midblue_pantone": Color(122/255, 137/255, 148/255),# Hex: #7A8994
    "duoc_darkblue_cmyk": Color(0/255, 51/255, 102/255),     # Hex: #003366
    "duoc_midblue_cmyk": Color(102/255, 128/255, 153/255),   # Hex: #668099

    # Sistema cromático complementario (pares definidos juntos)

    "complementary_purple": Color(149/255, 33/255, 178/255),     # #9521B2
    "complementary_orange": Color(247/255, 139/255, 48/255),     # #F78B30

    "complementary_lime": Color(189/255, 198/255, 1/255),        # #BDC601
    "complementary_darkgray": Color(51/255, 51/255, 51/255),     # #333333

    "complementary_green": Color(0/255, 133/255, 88/255),        # #008558
    "complementary_lightgreen": Color(102/255, 176/255, 50/255), # #66B032

    "complementary_hotpink": Color(191/255, 2/255, 73/255),      # #BF0249
    "complementary_cyan": Color(60/255, 188/255, 193/255),       # #3CBCC1

    "complementary_gray": Color(147/255, 147/255, 147/255),      # #939393
    "complementary_fuchsia": Color(191/255, 2/255, 73/255),      # #BF0249 

    "complementary_teal": Color(60/255, 188/255, 193/255),       # #3CBCC1
    "complementary_violet": Color(149/255, 33/255, 178/255),     # #9521B2

    "complementary_soft_orange": Color(247/255, 139/255, 48/255),# #F78B30  
    "complementary_wine": Color(160/255, 20/255, 99/255),        # #A01463

    "complementary_navy": Color(27/255, 39/255, 125/255),        # #1B277D
    "complementary_bright_blue": Color(0/255, 176/255, 240/255), # #00B0F0

    "complementary_sky_blue": Color(0/255, 163/255, 224/255),    # #00A3E0
    "complementary_deep_indigo": Color(28/255, 38/255, 112/255), # #1C2670

  

    # Colores sistema gráfico (social media y web)
    "web_black": Color(26/255, 26/255, 26/255),             # #1A1A1A
    "web_white": Color(1, 1, 1),                            # #FFFFFF
    "web_darkgray": Color(102/255, 102/255, 102/255),       # #666666
    "web_pure_black": Color(0, 0, 0),                       # #000000
    "web_orange": Color(241/255, 182/255, 52/255),          # #F1B634

    "web_blue": Color(19/255, 44/255, 170/255),             # #132CAA
    "web_green": Color(43/255, 145/255, 65/255),            # #2B9141
    "web_aqua": Color(55/255, 167/255, 198/255),            # #37A7C6
    "web_cyan": Color(60/255, 188/255, 193/255),            # #3CB8C1
    "web_purple": Color(149/255, 33/255, 178/255),          # #9521B2
    "web_magenta": Color(191/255, 2/255, 73/255),           # #BF0249
    "web_soft_orange": Color(247/255, 139/255, 48/255),     # #F78B30
    "web_lime": Color(189/255, 198/255, 1/255),             # #BDC601
    "web_gray": Color(147/255, 147/255, 147/255),           # #939393

}


# 🎯 Estilos tipográficos mapeados por uso
STYLES = {

    # ========= SECCION RESUMEN =========
    # Título header
    "section_header":        ("MyriadPro-Cond", 22),
    # Titulo prueba  
    "main_title":            ("MyriadPro-Cond", 20),   
    # Titulo asignatura
    "sub_title":             ("MyriadPro-Cond", 18),

    # Secciones internas --
    "section_subtitle":      ("MyriadPro-BoldCond", 10), 
    "panel_title":           ("MyriadPro-BoldCond", 9),

    # Identificadores: label
    "label":                 ("MyriadPro-BoldCond", 12),
    # Indentificadores: valor   
    "label_value":           ("MyriadPro-Cond", 13),

    # Nota
    "highlight_number":      ("MyriadPro-BoldCond", 46),
    # Desempeño  
    "highlight_label":       ("MyriadPro-Cond", 14),      

    # Párrafo motivacional
    "paragraph":             ("MyriadPro-Cond", 12),

    # Logros por aprendizaje
    "percentage_label":      ("MyriadPro-BoldCond", 16), 
    "learning_result_desc":  ("MyriadPro-Cond", 8),

    # Gráfico de distribución
    "chart_label":           ("MyriadPro-BoldCond", 12),
    "chart_number":          ("MyriadPro-BoldCond", 12),

    # Footer
    "footer_icon":           ("Helvetica", 9),
    "footer_text":           ("MyriadPro-Cond", 8),

    # Valores numéricos tabulados
    "nota_value":         ("NotoSansJapaneseSemiBold", 42),

    # Divider
    "divider_text":            ("MyriadPro-Cond", 16),

    # Porcentaje grafico barras vertical
    "porcentaje_barras_vertical":         ("NotoSansJapaneseSemiBold", 12),

    # Párrafos indicador de logro
    "barras_v_text":             ("MyriadPro-Cond", 12),

    # Titulo barra vertical
    "barras_v_title":             ("MyriadPro-Cond", 18),
    # Titulo barra vertical
    "barras_v_subtitle":             ("MyriadPro-Cond", 16),

    # eje x grafico dispersion
    "ejes_text": ("Helvetica", 9),

    # Tabla basica: titulo
    "table_b_title":             ("MyriadPro-Cond", 18),
    # Tabla basica: subtitulo
    "table_b_subtitle":             ("MyriadPro-Cond", 16),
    # Tabla basica: header
    "table_b_header":             ("MyriadPro-Cond", 14),
    # Tabla basica: celdas
    "table_b_cell":             ("MyriadPro-Light", 12),



}
