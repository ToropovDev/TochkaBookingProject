from datetime import datetime
from smtplib import SMTP_SSL

from celery import Celery

from backend.src.base_config import CELERY_BROKER_URL, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
from backend.src.scheduler.email_templates import get_email_template_verify, get_email_template_notify, get_email_template_ics

celery_app = Celery("auth", broker_url=CELERY_BROKER_URL)


@celery_app.task
def send_email_verify(
        username: str,
        user_email: str,
        token: str,
        subject: str
) -> None:
    email = get_email_template_verify(username, user_email, token, subject)
    with SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)


@celery_app.task
def send_email_notify(
        username: str,
        user_email: str,
        subject: str,
        game_name: str,
        game_place: str,
        game_datetime: datetime,
) -> None:
    email = get_email_template_notify(username, user_email, subject, game_name, game_place, game_datetime)
    with SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)


@celery_app.task
def send_ics_file(
        username: str,
        user_email: str,
        subject: str,
        game_details: dict
) -> None:
    email = get_email_template_ics(username, user_email, subject, game_details)
    with SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)