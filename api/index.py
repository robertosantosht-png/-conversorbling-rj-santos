# api/index.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ConverterRequest(BaseModel):
    email_destino: str
    planilha_path: str

@app.get("/")
def home():
    return {"status": "ok"}