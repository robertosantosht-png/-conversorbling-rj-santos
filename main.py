from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()


import shutil
import os

@app.post("/converter")
async def converter_xml(
    nome_cliente: str = Form(...),
    email_cliente: str = Form(...),
    markup: float = Form(...),
    cest: str = Form(...),
    modo: str = Form(...),
    marca: str = Form(""),
    xml_file: UploadFile = None
):

    # 🔹 CONTEÚDO DO XML ENVIADO PELO CLIENTE
    conteudo_xml = await xml_file.read()

    # 🔹 CAMINHO TEMPORÁRIO NO RAILWAY
    xml_temporario = "/tmp/entrada.xml"

    # 🔹 SALVAR O XML TEMPORARIAMENTE
    with open(xml_temporario, "wb") as f:
        f.write(conteudo_xml)

    # 🔹 CRIAR PASTA 'xml' QUE O SEU SCRIPT USA
    os.makedirs("xml", exist_ok=True)

    # 🔹 COPIAR O XML PARA A PASTA DO SEU SCRIPTS
    shutil.copy(xml_temporario, f"xml/{xml_file.filename}")

    # 🔹 EXECUTAR O SCRIPT DE CONVERSÃO
    # 3. Agora chamamos seu script para gerar o Excel
    import subprocess
    subprocess.run(["python3", "conversor_xml.py"], check=True)

    # 🔹 ARQUIVO QUE SEU SCRIPT GERA
    caminho_excel = "IMPORTAR_BLING.xlsx"

    # 🔹 COPIAR PARA /tmp PARA PERMITIR DOWNLOAD
    caminho_tmp = "/tmp/IMPORTAR_BLING.xlsx"
    shutil.copy(caminho_excel, caminho_tmp)

    # 🔹 ABRIR PÁGINA DE SUCESSO
    with open("sucesso.html", "r", encoding="utf-8") as f:
        html = f.read().replace("{nome_cliente}", nome_cliente)

    return HTMLResponse(html)
    # ---------------------------------------------------

    # Carrega página de sucesso
    with open("sucesso.html", "r", encoding="utf-8") as f:
        html = f.read()
        html = html.replace("{nome_cliente}", nome_cliente)
        html = html.replace("{arquivo}", nome_arquivo)

    return HTMLResponse(html)


@app.get("/download/{arquivo}")
def download(arquivo: str):

    caminho = f"/tmp/{arquivo}"

    # Evita Internal Server Error
    if not os.path.exists(caminho):
        return HTMLResponse(
            "<h1>Erro: Arquivo não encontrado no servidor.</h1>",
            status_code=404
        )

    return FileResponse(
        caminho,
        media_type="application/vnd.ms-excel",
        filename=arquivo
    )