from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from services.conversor_xml import processar_xml
from services.gerar_excel import gerar_excel
import os

app = FastAPI()

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