from celery import Celery

from src.celery.config import celery_settings

celery_app = Celery(
    "complmnt_celery",
    broker=celery_settings.broker_url)

@celery_app.task
def print_message(text:str):
    print(text)