from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from services.conversor_xml import processar_xml
from services.gerar_excel import gerar_excel
import os

app = FastAPI()

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# Servir arquivos estáticos (CSS, JS, imagens, se quiser adicionar depois)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota para abrir o index.html
@app.get("/", response_class=HTMLResponse)
def abrir_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/converter")
async def converter_xml(
    xml_file: UploadFile,
    markup: float = Form(...),
    cest: str = Form(...),
    modo: str = Form(...),
    marca: str = Form("")
):
    xml_content = await xml_file.read()
    produtos = processar_xml(xml_content, marca, cest, markup, modo)

    output_path = "output/produtos.xlsx"
    gerar_excel(produtos, output_path)

    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="produtos.xlsx"
    )