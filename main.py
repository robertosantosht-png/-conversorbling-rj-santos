from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.responses import RedirectResponse
import subprocess
import shutil
import os

app = FastAPI()

@app.get("/")
async def root():
    from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
    
@app.post("/converter")
async def converter(file: UploadFile = File(...)):
    # Save uploaded XML to /tmp
    xml_path = f"/tmp/{file.filename}"
    with open(xml_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Copy to xml folder
    xml_folder = "xml"
    os.makedirs(xml_folder, exist_ok=True)
    shutil.copy(xml_path, xml_folder)
    
    # Run conversor_xml.py
    result = subprocess.run(["python", "conversor_xml.py"], capture_output=True, text=True)
    if result.returncode != 0:
        return {"error": "Failed to run conversor_xml.py"}
    
    # Check for IMPORTAR_BLING.xlsx
    xlsx_path = "IMPORTAR_BLING.xlsx"
    if not os.path.exists(xlsx_path):
        return {"error": "IMPORTAR_BLING.xlsx not found"}
    
    # Copy to /tmp
    tmp_xlsx = "/tmp/IMPORTAR_BLING.xlsx"
    shutil.copy(xlsx_path, tmp_xlsx)
    
    # Redirect to sucesso
    return RedirectResponse(url="/sucesso", status_code=303)

@app.get("/sucesso")
async def sucesso():
    @app.get("/sucesso", response_class=HTMLResponse)
async def sucesso():
    with open("sucesso.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/download/{arquivo}")
async def download(arquivo: str):
    file_path = f"/tmp/{arquivo}"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=arquivo)
    return {"error": "File not found"}