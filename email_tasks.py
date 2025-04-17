from app import app
from email.message import EmailMessage
import smtplib
import os

@app.task(bind=True, max_retries=3)
@app.task(bind=True, max_retries=3)
def send_email_async(self, email_data):
    try:
        msg = EmailMessage()
        msg['Subject'] = email_data['subject']
        msg['From'] = email_data.get('from', 'no-reply@andresr.com')
        msg['To'] = email_data['to']
        
        # Envío real
        with smtplib.SMTP(os.getenv('SMTP_HOST'), os.getenv('SMTP_PORT')) as server:
            server.starttls()
            server.login(os.getenv('SMTP_USER'), os.getenv('SMTP_PASS'))
            server.send_message(msg)
            
        return True
    except Exception as e:
        self.retry(exc=e, countdown=60)  # Intentar cada minuto