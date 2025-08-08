import streamlit as st
import pandas as pd
import pytesseract
from pdf2image import convert_from_path
import re
import tempfile
import os

st.set_page_config(page_title="OCR Facturas", page_icon="📄", layout="wide")
st.title("📄 OCR de Facturas Eléctricas")

uploaded_file = st.file_uploader("Sube tu archivo PDF con facturas", type=["pdf"])

def extract_consumos_from_text(text):
    # Patrón para buscar consumos en kWh
    pattern = r'(\d+(?:[.,]\d+)?)\s*kWh'
    matches = re.findall(pattern, text)
    return [m.replace(",", ".") for m in matches]

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("📄 Convirtiendo PDF a imágenes...")
    images = convert_from_path(tmp_path)

    all_consumos = []
    factura_num = 1

    for img in images:
        text = pytesseract.image_to_string(img, lang="spa")
        consumos = extract_consumos_from_text(text)
        for c in consumos:
            all_consumos.append({"Factura": factura_num, "Consumo (kWh)": c})
        factura_num += 1

    df = pd.DataFrame(all_consumos)

    if not df.empty:
        st.success("✅ Datos extraídos con éxito")
        st.dataframe(df)

        # Botón para descargar
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Descargar CSV", csv, "consumos.csv", "text/csv")
    else:
        st.warning("No se encontraron consumos en el PDF.")

    # Limpieza
    os.remove(tmp_path)
