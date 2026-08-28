import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(destinatario, asunto, mensaje_html):
    """
    Envía un correo electrónico usando SMTP configurado por variables de entorno.
    Si no están configuradas las variables, muestra un log en la consola.
    """
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    if not smtp_user or not smtp_password:
        print(f"[EMAIL] Simulación de correo a {destinatario}: {asunto}\n{mensaje_html}")
        return False

    msg = MIMEMultipart("alternative")
    msg['Subject'] = asunto
    msg['From'] = f"TicketNow <{smtp_user}>"
    msg['To'] = destinatario

    part = MIMEText(mensaje_html, "html")
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, destinatario, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] No se pudo enviar el correo a {destinatario}: {str(e)}")
        return False
