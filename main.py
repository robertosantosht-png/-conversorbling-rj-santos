from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

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
    # PROCESSA O XML (seu código antigo entra aqui)
    nome_arquivo = "saida.xlsx"

    # devolve página de sucesso
    with open("sucesso.html", "r", encoding="utf-8") as f:
        html = f.read()
        html = html.replace("{nome_cliente}", nome_cliente)
        html = html.replace("{arquivo}", nome_arquivo)

    return HTMLResponse(html)

@app.get("/download/{arquivo}")
def download(arquivo: str):
    return FileResponse(arquivo, media_type="application/vnd.ms-excel")