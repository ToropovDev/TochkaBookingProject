from datetime import datetime

from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.payments.models import payment


async def add_payment_to_db(
        payment_data: dict,
        user_id: int,
        game_id: int,
        session: AsyncSession,
) -> None:
    try:
        print(payment_data['created_at'])
        new_payment = {
            "id": payment_data["id"],
            "status": payment_data["status"],
            "amount": payment_data["amount"]["value"],
            "currency": payment_data["amount"]["currency"],
            "user_id": user_id,
            "game_id": game_id,
            "description": payment_data["description"],
            "created_at": datetime.fromisoformat(payment_data["created_at"][:-1]),
            "captured_at": None,
        }
        stmt = insert(payment).values(**new_payment)
        await session.execute(stmt)
        await session.commit()
    except Exception as e:
        print(e)


async def update_payment(
        payment_id: str,
        payment_data: dict,
        session: AsyncSession) -> None:
    try:
        stmt = (update(payment).where(payment.c.id == payment_id).values({
            "status": payment_data["status"],
            "captured_at": datetime.fromisoformat(payment_data["captured_at"][:-1]),
        }))
        await session.execute(stmt)
        await session.commit()
    except Exception as e:
        print(e)
