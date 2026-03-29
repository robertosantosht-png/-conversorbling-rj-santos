from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import xml.etree.ElementTree as ET

app = FastAPI()

class ConverterRequest(BaseModel):
    nome: str
    email: str
    xml: str

@app.post("/converter")
def converter(dados: ConverterRequest):
    root = ET.fromstring(dados.xml)

    valores = []
    for item in root.iter():
        valores.append({
            "tag": item.tag,
            "valor": item.text
        })

    df = pd.DataFrame(valores)

    caminho = "/tmp/arquivo.xlsx"
    df.to_excel(caminho, index=False)

    return {
        "mensagem": "Arquivo gerado com sucesso",
        "linhas": len(df)
    }

@app.get("/")
def home():
    return {"status": "ok"}