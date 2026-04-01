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
    # Aqui entra seu PROCESSAMENTO DO XML
    # ---------------------------------------------------
    # Exemplo simples (você deve substituir pelo seu código):
    conteudo_xml = await xml_file.read()

    # Nome único para evitar conflito
    nome_arquivo = "saida.xlsx"
    caminho_tmp = f"/tmp/{nome_arquivo}"

    # Salva TEMPORARIAMENTE na nuvem (Railway)
    with open(caminho_tmp, "wb") as f:
        f.write(conteudo_xml)
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