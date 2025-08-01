import os
from pdf_generator.core import generate_sample_pdf

if __name__ == "__main__":
    path = generate_sample_pdf()
    print(f"PDF generado exitosamente en: {path}")
    
    """
    # 🖥️ Abre el archivo generado en el visor predeterminado
    try:
        os.startfile(path)  # ✅ Solo funciona en Windows
    except AttributeError:
        print("Apertura automática no soportada en este sistema operativo.")
    """
