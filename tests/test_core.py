import os
import sys

# 👇 Esto debe ir antes de las importaciones del paquete
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf_generator.core import generate_sample_pdf
from pdf_generator.settings import OUTPUT_DIR

def test_generate_sample_pdf():
    filepath = generate_sample_pdf("test_output.pdf")
    assert os.path.exists(filepath)
    assert filepath.startswith(OUTPUT_DIR)
