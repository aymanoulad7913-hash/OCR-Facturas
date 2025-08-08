
# Despliegue en Streamlit Cloud

## Archivos necesarios en tu repo de GitHub
- app_ocr_facturas.py
- requirements.txt  (este archivo)
- packages.txt      (instala Tesseract y español en el contenedor)

## Pasos
1) Sube estos archivos a un repositorio nuevo en GitHub.
2) Ve a https://share.streamlit.io/ y elige "Deploy a public app from GitHub".
3) Selecciona tu repo, rama (main) y el archivo principal: app_ocr_facturas.py
4) Pulsa "Deploy". La primera vez tardará unos minutos (instala paquetes).
5) Cuando termine, tendrás una URL pública de tu app.

## Notas
- Tesseract se instala con `tesseract-ocr` y el idioma español con `tesseract-ocr-spa` (via packages.txt).
- Si tu PDF está muy escaneado, en la app sube el DPI a 300–400 y deja idiomas como "spa+eng".
- Si quieres añadir más idiomas, agrega su paquete correspondiente (p. ej. `tesseract-ocr-por` para portugués) a packages.txt y vuelve a desplegar.
