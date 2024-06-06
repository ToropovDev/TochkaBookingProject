import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from yookassa import Configuration, Payment
from backend.src.base_config import YOOKASSA_ACCOUNT_ID, YOOKASSA_SECRET_KEY

Configuration.account_id = YOOKASSA_ACCOUNT_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


def create_payment(
        amount: float,
        description: str,
) -> dict:
    payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency":  "RUB"
        },
        "confirmation": {
            "type":  "redirect",
            "return_url":   "127.0.0.1",
        },
        "capture": True,
        "description": description,
    }, uuid.uuid4())

    return {
        "confirmation_url": payment.confirmation.confirmation_url,
        "payment_id": payment.id,
    }


def check_payment(payment_id: str):
    payment = Payment.find_one(payment_id)
    return payment.json()
