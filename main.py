import pandas as pd
import openpyxl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import logging
import os
from dotenv import load_dotenv
load_dotenv()  # Carrega .env automaticamente
from flask import Flask, request, jsonify

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para enviar email via SMTP Gmail
def enviar_email(destinatario, assunto, corpo, anexo_path=None):
    try:
        # Configurações do Gmail via variáveis de ambiente
        gmail_user = os.getenv('GMAIL_USER')
        gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not gmail_user or not gmail_app_password:
            raise ValueError("Variáveis de ambiente GMAIL_USER e GMAIL_APP_PASSWORD não configuradas.")
        
        # Cria a mensagem
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'plain'))
        
        # Anexa o arquivo se fornecido
        if anexo_path:
            with open(anexo_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(anexo_path)}')
                msg.attach(part)
        
        # Envia o email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_app_password)
        text = msg.as_string()
        server.sendmail(gmail_user, destinatario, text)
        server.quit()
        
        logging.info(f"Email enviado com sucesso para {destinatario}.")
    except Exception as e:
        logging.error(f"Erro ao enviar email: {str(e)}")
        raise

# Função para ler template de email
def ler_template(caminho_template):
    try:
        with open(caminho_template, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"Template {caminho_template} não encontrado.")
        raise

# Função para enviar email inicial
def email_inicial(email_destino):
    corpo = ler_template('index.txt')
    enviar_email(email_destino, 'Processo Iniciado - Conversor de Planilha para Bling', corpo)

# Função para enviar email de progresso
def email_progresso(email_destino):
    corpo = ler_template('main.txt')
    enviar_email(email_destino, 'Progresso - Conversor de Planilha para Bling', corpo)

# Função principal para conversão e envio de email de sucesso
def disparo_automatico(email_destino, planilha_path):
    try:
        # Envia email inicial
        email_inicial(email_destino)
        
        # Lê a planilha (Excel ou CSV)
        if planilha_path.endswith('.csv'):
            df = pd.read_csv(planilha_path)
        else:
            df = pd.read_excel(planilha_path, engine='openpyxl')
        
        logging.info(f"Planilha lida com sucesso: {planilha_path}")
        
        # Envia email de progresso
        email_progresso(email_destino)
        
        # Assume estrutura padrão: colunas como 'Produto', 'SKU', 'Preço', 'Estoque' etc.
        # Mapeia para formato Bling (ajuste conforme necessário)
        # Aqui assumimos que as colunas já estão corretas ou fazemos mapeamento simples
        df_bling = df[['Produto', 'SKU', 'Preço', 'Estoque']]  # Ajuste as colunas conforme a estrutura real
        
        # Gera novo Excel convertido
        output_path = 'planilha_convertida.xlsx'
        df_bling.to_excel(output_path, index=False, engine='openpyxl')
        
        logging.info(f"Planilha convertida gerada: {output_path}")
        
        # Lê corpo do email de sucesso
        corpo_sucesso = ler_template('sucesso.txt')
        
        # Envia email de sucesso com anexo
        enviar_email(email_destino, 'Conversão Concluída - Planilha para Bling', corpo_sucesso, output_path)
        
        logging.info("Processo concluído com sucesso.")
        
    except Exception as e:
        logging.error(f"Erro no processo: {str(e)}")
        # Envia email de falha
        corpo_falha = f"Ocorreu um erro durante o processamento: {str(e)}"
        try:
            enviar_email(email_destino, 'Erro - Conversor de Planilha para Bling', corpo_falha)
        except:
            logging.error("Falha ao enviar email de erro.")
        raise

# Aplicação Flask para deploy no Vercel/FastAPI
app = Flask(__name__)

@app.route('/converter', methods=['POST'])
def converter():
    try:
        data = request.json
        email_destino = data.get('email_destino')
        planilha_path = data.get('planilha_path')
        
        if not email_destino or not planilha_path:
            return jsonify({'error': 'Parâmetros email_destino e planilha_path são obrigatórios.'}), 400
        
        disparo_automatico(email_destino, planilha_path)
        return jsonify({'message': 'Conversão iniciada com sucesso.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)