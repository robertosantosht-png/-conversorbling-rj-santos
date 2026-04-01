from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
import subprocess
import shutil
import os

app = FastAPI()

# ROTA PRINCIPAL – SERVE index.html
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

# ROTA DE CONVERSÃO
@app.post("/converter")
async def converter(
    file: UploadFile = File(...)
):
    xml_path = f"/tmp/{file.filename}"

    # Salva XML no /tmp
    with open(xml_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Cria pasta xml/ e copia o arquivo
    os.makedirs("xml", exist_ok=True)
    shutil.copy(xml_path, "xml")

    # Executa conversor_xml.py
    result = subprocess.run(["python", "conversor_xml.py"], capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": result.stderr}

    # Verifica planilha
    if not os.path.exists("IMPORTAR_BLING.xlsx"):
        return {"error": "IMPORTAR_BLING.xlsx not found"}

    # Copia para /tmp
    shutil.copy("IMPORTAR_BLING.xlsx", "/tmp/IMPORTAR_BLING.xlsx")

    # Redireciona para sucesso
    return RedirectResponse(url="/sucesso", status_code=303)

# ROTA DE SUCESSO – SERVE sucesso.html
@app.get("/sucesso", response_class=HTMLResponse)
async def sucesso():
    with open("sucesso.html", "r", encoding="utf-8") as f:
        return f.read()

# DOWNLOAD DA PLANILHA
@app.get("/download/{arquivo}")
async def download(arquivo: str):
    file_path = f"/tmp/{arquivo}"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=arquivo)
    return {"error": "File not found"}