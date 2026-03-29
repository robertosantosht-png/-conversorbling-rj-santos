from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pandas as pd
import xml.etree.ElementTree as ET

app = FastAPI()

# Rota principal (health check)
@app.get("/")
def home():
    return {"status": "ok"}


# Rota de conversão com upload de XML
@app.post("/converter")
async def converter(file: UploadFile = File(...)):
    try:
        # Lê o arquivo enviado
        conteudo = await file.read()

        # Converte XML
        root = ET.fromstring(conteudo)

        # Extrai dados simples (estrutura base)
        linhas = []
        for item in root.iter():
            linhas.append({
                "tag": item.tag,
                "valor": item.text
            })

        # Cria DataFrame
        df = pd.DataFrame(linhas)

        # Salva Excel temporário (obrigatório no Vercel)
        caminho = "/tmp/arquivo.xlsx"
        df.to_excel(caminho, index=False)

        # Retorna o arquivo para download
        return FileResponse(
            path=caminho,
            filename="planilha.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return {"erro": str(e)}


# Necessário para o Vercel
handler = app