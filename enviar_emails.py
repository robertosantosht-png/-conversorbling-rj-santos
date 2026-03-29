def enviar_email(destinatario, assunto, corpo, anexo_path=None):
    try:
        gmail_user = os.getenv('GMAIL_USER')
        gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not gmail_user or not gmail_app_password:
            raise ValueError("Variáveis GMAIL_USER e GMAIL_APP_PASSWORD ausentes no .env.")
        
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = destinatario
        msg['Subject'] = assunto
        msg.attach(MIMEText(corpo, 'plain'))
        
        if anexo_path:
            with open(anexo_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(anexo_path)}')
                msg.attach(part)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_app_password)
        text = msg.as_string()
        server.sendmail(gmail_user, destinatario, text)
        server.quit()
        
        logging.info(f"Email enviado para {destinatario}.")
    except Exception as e:
        logging.error(f"Erro SMTP: {str(e)}")
        raise