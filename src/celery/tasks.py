from smtplib import SMTP
from socket import gaierror
from celery import Celery
from email.message import EmailMessage
from src.celery.config import celery_settings

celery_app = Celery(
    "complmnt_celery",
    broker=celery_settings.broker_url)

@celery_app.task
def print_message(text:str):
    print(text)

@celery_app.task(
    autoretry_for = (ConnectionError,TimeoutError,gaierror),
    retry_backoff = 10,
    retry_jitter = False,
    max_retries = 2
    )
def send_email(to_email,subject,body):
    msg = EmailMessage()
    msg["From"] = "noreply@compliment.com"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)
    with SMTP(host="maildev",port=1025,timeout=5) as smtp:
        smtp.send_message(msg)