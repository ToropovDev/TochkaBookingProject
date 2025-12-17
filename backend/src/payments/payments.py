import json
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from yookassa import Configuration, Payment

from src.base_config import YOOKASSA_ACCOUNT_ID, YOOKASSA_SECRET_KEY
from src.payments.handlers import add_payment_to_db, update_payment

Configuration.account_id = YOOKASSA_ACCOUNT_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


async def create_payment(
    amount: float,
    description: str,
    user_id: int,
    game_id: int,
    session: AsyncSession,
) -> dict:
    payment = Payment.create(
        {
            "amount": {"value": str(amount), "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": "127.0.0.1",
            },
            "capture": True,
            "description": description,
        },
        uuid.uuid4(),
    )
    print(1)
    created_payment_data = (await check_payment(payment.id, session))[1]
    await add_payment_to_db(created_payment_data, user_id, game_id, session)

    return {
        "confirmation_url": payment.confirmation.confirmation_url,
        "payment_id": payment.id,
    }


async def check_payment(payment_id: str, session: AsyncSession) -> (bool, dict):
    print(2)
    payment = json.loads(Payment.find_one(payment_id).json())
    check_stmt = payment["status"] != "pending"
    if check_stmt:
        await update_payment(payment_id, payment, session)
    return check_stmt, payment
