from fastapi import FastAPI, UploadFile, Form, FileResponse
from fastapi.responses import FileResponse
import os
from services.conversor_xml import processar_xml
from services.gerar_excel import gerar_excel

app = FastAPI()

@app.post("/converter")
async def converter(
    xml_file: UploadFile,
    marca: str = Form(...),
    cest: str = Form(...),
    markup: float = Form(...),
    modo: str = Form(...),
    data: str = Form(...)
):
    xml_content = xml_file.file.read()
    produtos = processar_xml(xml_content, marca, cest, markup, modo, data)
    os.makedirs("output", exist_ok=True)
    output_path = "output/bling_produtos.xlsx"
    gerar_excel(produtos, output_path)
    return FileResponse(output_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="bling_produtos.xlsx")