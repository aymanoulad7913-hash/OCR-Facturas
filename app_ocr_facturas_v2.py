import os, re, tempfile
from io import BytesIO
import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
from PIL import Image

try:
    import pytesseract
except Exception:
    pytesseract = None  # en cloud debería estar

st.set_page_config(page_title="OCR Facturas", page_icon="📄", layout="wide")
st.title("📄 OCR de Facturas (sin Poppler)")

uploaded_file = st.file_uploader("Sube tu PDF", type=["pdf"])
dpi = st.slider("DPI (para páginas escaneadas)", 150, 600, 300, 50)
langs = st.text_input("Idiomas Tesseract", value="spa+eng")

def normnum(s: str):
    s = s.strip().replace("\u00A0"," ").replace(" ","")
    if "," in s and "." in s: s = s.replace(".","").replace(",",".")
    elif "," in s: s = s.replace(",",".")
    try: return float(s)
    except: return None

def extract_consumos(text: str):
    # ejemplo simple para kWh; amplía si quieres otros
    pat = re.compile(r"(\d[\d\.\,\s]*\d|\d)\s*kwh\b", re.IGNORECASE)
    vals = [normnum(m.group(1)) for m in pat.finditer(text)]
    return [v for v in vals if v is not None]

def page_text_or_ocr(page, dpi=300, langs="spa+eng"):
    raw = page.get_text("text")
    if raw and raw.strip():
        return raw, "nativo"
    if pytesseract is None:
        raise RuntimeError("pytesseract no disponible.")
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    img_bytes = pix.tobytes("png")
    img = Image.open(BytesIO(img_bytes)).convert("RGB")
    return pytesseract.image_to_string(img, lang=langs), "ocr"

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    st.info("Procesando PDF…")
    rows = []
    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc, start=1):
            txt, fuente = page_text_or_ocr(page, dpi=dpi, langs=langs)
            consumos = extract_consumos(txt)
            for c in consumos:
                rows.append({"pagina": i, "consumo_kwh": c, "fuente": fuente})

    df = pd.DataFrame(rows)
    if not df.empty:
        st.success(f"✅ Encontrados {len(df)} consumos")
        st.dataframe(df, use_container_width=True)
        buffer = BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        st.download_button(
            "⬇️ Descargar Excel",
            data=buffer.getvalue(),
            file_name="consumos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.warning("No se encontraron consumos. Sube el DPI o revisa el patrón de búsqueda.")

    os.remove(pdf_path)

