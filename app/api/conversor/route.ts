import { NextRequest, NextResponse } from "next/server";
import { XMLParser } from "fast-xml-parser";
import * as XLSX from "xlsx";

export const runtime = "nodejs"; // IMPORTANTE: evitar Edge Runtime

export async function POST(req: NextRequest) {
  try {
    const form = await req.formData();

    const xmlFile = form.get("xml") as File;
    const nome = form.get("nome") as string;
    const email = form.get("email") as string;
    const markup = parseFloat(form.get("markup") as string);
    const cest = form.get("cest") as string;
    const modo = form.get("modo_conversao") as string;
    const marca_padrao = form.get("marca_padrao") as string;

    if (!xmlFile || !nome || !email || isNaN(markup) || !cest || !modo || !marca_padrao) {
      return NextResponse.json({ error: "Campos obrigatórios ausentes." }, { status: 400 });
    }

    // ----- LER XML -----
    const text = await xmlFile.text();

    const parser = new XMLParser({
      ignoreAttributes: false,
      ignoreNameSpace: true,
      alwaysCreateTextNode: false
    });

    const parsed: any = parser.parse(text);
    const nfe = parsed.nfeProc?.NFe?.infNFe;

    const fornecedor = nfe.emit.xNome || "";
    const dets = Array.isArray(nfe.det) ? nfe.det : [nfe.det];

    // ----- PREPARAR PLANILHA -----
    const header = [
      "ID","Código","Descrição","Unidade","NCM","Origem","Preço","Valor IPI fixo",
      "Observações","Situação","Estoque","Preço de custo","Cód no fornecedor",
      "Fornecedor","Localização","Estoque maximo","Estoque minimo","Peso líquido (Kg)",
      "Peso bruto (Kg)","GTIN/EAN","GTIN/EAN da embalagem","Largura do Produto",
      "Altura do Produto","Profundidade do produto","Data Validade",
      "Descrição do Produto no Fornecedor","Descrição Complementar","Itens p/ caixa",
      "Produto Variação","Tipo Produção","Classe de enquadramento do IPI",
      "Código da lista de serviços","Tipo do item","Grupo de Tags/Tags","Tributos",
      "Código Pai","Código Integração","Grupo de produtos","MARCA","CEST",
      "Volumes","Descrição Curta","Cross-Docking","URL Imagens Externas",
      "Link Externo","Meses Garantia no Fornecedor","Clonar dados do pai",
      "Condição do produto","Frete Grátis","Número FCI","Vídeo","Departamento",
      "Unidade de medida","Preço de compra","Valor base ICMS ST para retenção",
      "Valor ICMS ST para retenção","Valor ICMS próprio do substituto",
      "Categoria do produto","Informações Adicionais"
    ];

    const rows: any[] = [];
    rows.push(header);

    const hoje = new Date();
    const dataCodigo = `${String(hoje.getDate()).padStart(2,"0")}${String(hoje.getMonth()+1).padStart(2,"0")}${hoje.getFullYear()}`;

    let contador = 1;

    for (const det of dets) {
      const prod = det.prod;
      const imposto = det.imposto?.ICMS || {};

      const cProd = prod.cProd || "";
      const xProd = prod.xProd || "";
      const uCom = prod.uCom || "";
      const qComRaw = parseFloat(prod.qCom || "0");
      const qCom = Math.floor(qComRaw); // ✔ opção A confirmada
      const vUnCom = parseFloat(prod.vUnCom || "0");
      const preco = vUnCom * markup;

      const NCM = prod.NCM || "";
      const cEAN = prod.cEAN || "";

      // Origem ICMS
      const origem =
        imposto.ICMS00?.orig ??
        imposto.ICMS10?.orig ??
        imposto.ICMS20?.orig ??
        imposto.ICMS30?.orig ??
        imposto.ICMS40?.orig ??
        imposto.ICMS51?.orig ??
        imposto.ICMS70?.orig ??
        imposto.ICMS90?.orig ??
        imposto.ICMSSN101?.orig ??
        imposto.ICMSSN102?.orig ??
        imposto.ICMSSN201?.orig ??
        imposto.ICMSSN202?.orig ??
        imposto.ICMSSN500?.orig ??
        imposto.ICMSSN900?.orig ??
        "";

      const codigoPai = `${cProd}/${dataCodigo}-${String(contador).padStart(2,"0")}`;
      contador++;

      // ---------- MODO SIMPLES ----------
      if (modo === "Simples") {
        rows.push([
          "", codigoPai, xProd, uCom, NCM, origem, preco.toFixed(2), "",
          "", "Ativo", qCom, vUnCom, cProd,
          fornecedor, "", "", "", 0.8,
          1.0, cEAN, "", 30,
          30, 30, "",
          xProd, "", "",
          "Simples", "Terceiro", "",
          "", "Mercadoria para Revenda", "", "",
          codigoPai, "", "", marca_padrao, cest,
          1, "", "", "",
          "", "", "Não",
          "Novo", "Não", "", "", "Adulto",
          "Centímetros", vUnCom, "",
          "", "",
          "", ""
        ]);
      }

      // ---------- MODO VARIAÇÃO ----------
      else if (modo === "Variação") {

        // PAI
        rows.push([
          "", codigoPai, xProd, uCom, NCM, origem, preco.toFixed(2), "",
          "", "Ativo", "", vUnCom, cProd,
          fornecedor, "", "", "", 0.8,
          1.0, cEAN, "", 30,
          30, 30, "",
          xProd, "", "",
          "Variação", "Terceiro", "",
          "", "Mercadoria para Revenda", "", "",
          "", "", "", marca_padrao, cest,
          1, "", "", "",
          "", "", "Não",
          "Novo", "Não", "", "", "Adulto",
          "Centímetros", vUnCom, "",
          "", "",
          "", ""
        ]);

        // FILHOS
        for (let i = 1; i <= qCom; i++) {
          const codigoFilho = `${codigoPai}-${i}`;

          rows.push([
            "", codigoFilho, xProd, uCom, NCM, origem, preco.toFixed(2), "",
            "", "Ativo", 1, vUnCom, cProd,
            fornecedor, "", "", "", 0.8,
            1.0, cEAN, "", 30,
            30, 30, "",
            xProd, "", "",
            "Variação", "Terceiro", "",
            "", "Mercadoria para Revenda", "", "",
            codigoPai, "", "", marca_padrao, cest,
            1, "", "", "",
            "", "", "Sim",
            "Novo", "Não", "", "", "Adulto",
            "Centímetros", vUnCom, "",
            "", "",
            "", ""
          ]);
        }
      }
    }

    // ----- GERAR XLSX -----
    const ws = XLSX.utils.aoa_to_sheet(rows);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Produtos");

    const buffer = XLSX.write(wb, { type: "buffer", bookType: "xlsx" });

    return new NextResponse(buffer, {
      headers: {
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "Content-Disposition": "attachment; filename=produtos.xlsx"
      }
    });

  } catch (err) {
    console.error(err);
    return NextResponse.json({ error: "Erro interno ao gerar XLSX" }, { status: 500 });
  }
}