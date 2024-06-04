from datetime import datetime
from email.message import EmailMessage

from backend.src.base_config import SMTP_USER


def get_email_template_verify(
        username: str,
        user_email: str,
        token: str,
        subject: str
) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<p>Здравствуйте, {username}, код подтверждения: {token}</p>'
        '</div>',
        subtype='html'
    )
    return email


def get_email_template_notify(
        username: str,
        user_email: str,
        subject: str,
        game_name: str,
        game_place: str,
        game_datetime: datetime,
) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = subject
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<p>Здравствуйте, {username}, у вас есть предстоящая запись на игру:'
        f'<br>Игра: <b>{game_name}</b>'
        f'<br>Место:  <b>{game_place}</b>'
        f'<br>Время:   <b>{game_datetime}</b>'
        f'</p>'
        '</div>',
        subtype='html'
    )
    return email
