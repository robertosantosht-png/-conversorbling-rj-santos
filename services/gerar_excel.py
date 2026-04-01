import pandas as pd
from services.bling_padrao import BLING_COLUNAS

def gerar_excel(produtos, output_path):
    data = []
    for produto in produtos:
        row = {col: "" for col in BLING_COLUNAS}
        row["Código"] = produto.get("codigo_filho") or produto.get("codigo_pai", "")
        row["Descrição"] = produto.get("xProd", "")
        row["Unidade"] = "UN"
        row["NCM"] = produto.get("NCM", "")
        row["Origem"] = produto.get("orig", "")
        row["Preço"] = produto.get("preco_venda", "")
        row["Estoque"] = produto.get("estoque", "")
        row["Preço de custo"] = produto.get("vUnCom", "")
        row["Cód no fornecedor"] = produto.get("cProd", "")
        row["GTIN/EAN"] = produto.get("EAN", "")
        row["Peso líquido (Kg)"] = produto.get("peso_liquido", "")
        row["Peso bruto (Kg)"] = produto.get("peso_bruto", "")
        row["Largura do Produto"] = produto.get("largura", "")
        row["Altura do Produto"] = produto.get("altura", "")
        row["Profundidade do produto"] = produto.get("profundidade", "")
        row["Código Pai"] = produto.get("codigo_pai", "") if not produto.get("is_pai", True) else ""
        row["Produto Variação"] = "S" if not produto.get("is_pai", True) else "N"
        row["MARCA"] = produto.get("marca", "")
        row["CEST"] = produto.get("CEST", "")
        row["Volumes"] = produto.get("Volumes", "")
        row["Preço de compra"] = produto.get("vUnCom", "")
        data.append(row)
    df = pd.DataFrame(data, columns=BLING_COLUNAS)
    df.to_excel(output_path, index=False)
