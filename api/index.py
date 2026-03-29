from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ConverterRequest(BaseModel):
    nome: str
    email: str
    xml: str

@app.get("/")
def home():
    return {"status": "ok"}

@app.post("/converter")
def converter(dados: ConverterRequest):
    return {
        "mensagem": "Dados recebidos com sucesso",
        "nome": dados.nome,
        "email": dados.email,
        "tamanho_xml": len(dados.xml)
    }

handler = app