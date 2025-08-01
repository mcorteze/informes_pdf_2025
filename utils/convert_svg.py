import cairosvg
import os

# 🔁 Corrige la ruta base y súbela un nivel desde /utils/
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_dir = os.path.join(base_dir, "assets")

# Archivos
svg_path = os.path.join(assets_dir, "header-logo.svg")
png_path = os.path.join(assets_dir, "header-logo.png")

# 🧪 Verifica existencia del archivo fuente
if not os.path.exists(svg_path):
    raise FileNotFoundError(f"No se encontró el archivo SVG en: {svg_path}")

# ✅ Convertir
cairosvg.svg2png(url=svg_path, write_to=png_path)
print(f"Convertido correctamente: {png_path}")
