from pathlib import Path

from pydantic import EmailStr

from app.config import settings
from app.tasks.celery_config import celery_app
from PIL import Image
import smtplib

from app.tasks.email_templates import create_booking_confirmation_template


@celery_app.task
def process_pic(
        path: str,
):
    im_path = Path(path)
    im = Image.open(path)
    im_resized = im.resize((1000, 500))
    im_resized_2 = im.resize((200, 100))
    im_resized.save(f"app/static/images/resized1_{im_path.name}")
    im_resized_2.save(f"app/static/images/resized2_{im_path.name}")


@celery_app.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr,
):
    email_to_mock = settings.SMTP_USER
    msg_content = create_booking_confirmation_template(booking, email_to_mock)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
