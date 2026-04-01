import xml.etree.ElementTree as ET
from datetime import datetime

def processar_xml(xml_content, marca, cest, markup, modo):
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    root = ET.fromstring(xml_content)
    data_atual = datetime.now().strftime('%d%m%Y')
    seq = 1
    produtos = []
    
    volumes_element = root.find('.//nfe:transp/nfe:vol/nfe:qVol', ns)
    volumes = volumes_element.text if volumes_element is not None else ""
    
    for det in root.findall('.//nfe:det', ns):
        cProd = det.find('.//nfe:prod/nfe:cProd', ns).text
        xProd = det.find('.//nfe:prod/nfe:xProd', ns).text
        NCM = det.find('.//nfe:prod/nfe:NCM', ns).text
        CFOP = det.find('.//nfe:prod/nfe:CFOP', ns).text
        EAN_element = det.find('.//nfe:prod/nfe:cEAN', ns)
        EAN = EAN_element.text if EAN_element is not None else ""
        qCom = float(det.find('.//nfe:prod/nfe:qCom', ns).text)
        vUnCom = float(det.find('.//nfe:prod/nfe:vUnCom', ns).text)
        orig_element = det.find('.//nfe:ICMS*/nfe:orig', ns)
        orig = orig_element.text if orig_element is not None else ""
        
        preco_venda = vUnCom * markup
        codigo_pai = f"{cProd}/{data_atual}-{seq}"
        seq += 1
        
        if modo == 'VARIAÇÃO':
            estoque_pai = 0
            is_pai_pai = True
            produto_pai = {
                'cProd': cProd,
                'xProd': xProd,
                'NCM': NCM,
                'CEST': cest,
                'EAN': EAN,
                'qCom': qCom,
                'vUnCom': vUnCom,
                'orig': orig,
                'CFOP': CFOP,
                'Volumes': volumes,
                'marca': marca,
                'preco_venda': preco_venda,
                'codigo_pai': codigo_pai,
                'codigo_filho': "",
                'estoque': estoque_pai,
                'peso_liquido': 0.8,
                'peso_bruto': 1.0,
                'largura': 30,
                'altura': 30,
                'profundidade': 30,
                'is_pai': is_pai_pai
            }
            produtos.append(produto_pai)
            
            for i in range(1, int(qCom) + 1):
                codigo_filho = f"{codigo_pai}-{i}"
                produto_filho = {
                    'cProd': cProd,
                    'xProd': xProd,
                    'NCM': NCM,
                    'CEST': cest,
                    'EAN': EAN,
                    'qCom': qCom,
                    'vUnCom': vUnCom,
                    'orig': orig,
                    'CFOP': CFOP,
                    'Volumes': volumes,
                    'marca': marca,
                    'preco_venda': preco_venda,
                    'codigo_pai': codigo_pai,
                    'codigo_filho': codigo_filho,
                    'estoque': 1,
                    'peso_liquido': 0.8,
                    'peso_bruto': 1.0,
                    'largura': 30,
                    'altura': 30,
                    'profundidade': 30,
                    'is_pai': False
                }
                produtos.append(produto_filho)
        else:  # modo == 'SIMPLES'
            estoque = qCom
            produto = {
                'cProd': cProd,
                'xProd': xProd,
                'NCM': NCM,
                'CEST': cest,
                'EAN': EAN,
                'qCom': qCom,
                'vUnCom': vUnCom,
                'orig': orig,
                'CFOP': CFOP,
                'Volumes': volumes,
                'marca': marca,
                'preco_venda': preco_venda,
                'codigo_pai': codigo_pai,
                'codigo_filho': "",
                'estoque': estoque,
                'peso_liquido': 0.8,
                'peso_bruto': 1.0,
                'largura': 30,
                'altura': 30,
                'profundidade': 30,
                'is_pai': True
            }
            produtos.append(produto)
    
    return produtos