import json
import pandas as pd
from lxml import etree

with open('/tmp/config.json', 'r') as f:
    config = json.load(f)

markup = config['markup']
cest = config['cest']
modo_conversao = config['modo_conversao']
marca_padrao = config['marca_padrao']

tree = etree.parse('/tmp/entrada.xml')
root = tree.getroot()
ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

data = []
for det in root.findall('.//nfe:det', ns):
    prod = det.find('nfe:prod', ns)
    if prod is None:
        continue
    
    codigo = prod.findtext('nfe:cProd', '', ns)
    descricao = prod.findtext('nfe:xProd', '', ns)
    unidade = prod.findtext('nfe:uCom', '', ns)
    ncm = prod.findtext('nfe:NCM', '', ns)
    ean = prod.findtext('nfe:cEAN', '', ns)
    preco_compra = float(prod.findtext('nfe:vUnCom', '0', ns))
    qtd = float(prod.findtext('nfe:qCom', '0', ns))
    
    preco = preco_compra * markup
    preco_custo = preco_compra
    estoque = qtd
    codigo_pai = codigo
    codigo_filho = ''
    marca = marca_padrao
    cfop = ''
    volumes = 1
    origem = ''
    peso_liquido = float(prod.findtext('nfe:qCom', '0', ns))  # assuming same as qtd for simplicity
    peso_bruto = peso_liquido
    largura = 0
    altura = 0
    profundidade = 0
    produto_variacao = ''
    
    if modo_conversao == 'Simples':
        data.append({
            'Código': codigo,
            'Descrição': descricao,
            'Unidade': unidade,
            'NCM': ncm,
            'CEST': cest,
            'EAN': ean,
            'Preço': preco,
            'Preço de custo': preco_custo,
            'Preço de compra': preco_compra,
            'Estoque': estoque,
            'Código Pai': '',
            'Código Filho': '',
            'Marca': marca,
            'CFOP': cfop,
            'Volumes': volumes,
            'Origem': origem,
            'Peso líquido': peso_liquido,
            'Peso bruto': peso_bruto,
            'Largura': largura,
            'Altura': altura,
            'Profundidade': profundidade,
            'Produto Variação': produto_variacao
        })
    elif modo_conversao == 'Variação':
        data.append({
            'Código': codigo_pai,
            'Descrição': descricao,
            'Unidade': unidade,
            'NCM': ncm,
            'CEST': cest,
            'EAN': ean,
            'Preço': preco,
            'Preço de custo': preco_custo,
            'Preço de compra': preco_compra,
            'Estoque': estoque,
            'Código Pai': codigo_pai,
            'Código Filho': '',
            'Marca': marca,
            'CFOP': cfop,
            'Volumes': volumes,
            'Origem': origem,
            'Peso líquido': peso_liquido,
            'Peso bruto': peso_bruto,
            'Largura': largura,
            'Altura': altura,
            'Profundidade': profundidade,
            'Produto Variação': 'Pai'
        })
        data.append({
            'Código': f'{codigo}-VAR',
            'Descrição': f'{descricao} - Variação',
            'Unidade': unidade,
            'NCM': ncm,
            'CEST': cest,
            'EAN': ean,
            'Preço': preco,
            'Preço de custo': preco_custo,
            'Preço de compra': preco_compra,
            'Estoque': estoque,
            'Código Pai': codigo_pai,
            'Código Filho': f'{codigo}-VAR',
            'Marca': marca,
            'CFOP': cfop,
            'Volumes': volumes,
            'Origem': origem,
            'Peso líquido': peso_liquido,
            'Peso bruto': peso_bruto,
            'Largura': largura,
            'Altura': altura,
            'Profundidade': profundidade,
            'Produto Variação': 'Filho'
        })

df = pd.DataFrame(data)
df.to_excel('IMPORTAR_BLING.xlsx', index=False)