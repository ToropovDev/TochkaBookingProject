from datetime import datetime
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.base_config import SMTP_USER
from src.games.calendar import create_icalendar_file


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


def get_email_template_ics(
        username: str,
        user_email: str,
        subject: str,
        game_details: dict
) -> MIMEMultipart:
    email = MIMEMultipart()
    email['Subject'] = subject
    email['From'] = SMTP_USER
    email['To'] = user_email

    body = (
        '<div>'
        f'<p>Здравствуйте, {username}, у вас есть предстоящая запись на игру:'
        f'<br>Игра: <b>{game_details["name"]}</b>'
        f'<br>Место:  <b>{game_details["place"]}</b>'
        f'<br>Время:   <b>{game_details["datetime"]}</b>'
        f'</p>'
        '</div>'
    )
    email.attach(MIMEText(body, 'html'))

    ics_content = create_icalendar_file(game_details)

    part = MIMEBase('text', 'calendar')
    part.set_payload(ics_content)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="event.ics"')
    email.attach(part)

    return email
