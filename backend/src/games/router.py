from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import current_verified_user
from src.auth.models import User
from src.database import get_async_session
from src.games.handlers import (
    get_game_by_id,
    add_game_to_team,
    increment_games_organized,
)
from src.games.models import game
from src.games.schemas import GameCreate
from src.payments.payments import create_payment, check_payment
from src.scheduler.delayed_update_count import add_game_to_scheduler
from src.scheduler.notification import add_notification
from src.scheduler.clr import send_ics_file

from src.payments.models import payment

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


@router.get("/")
async def get_all_games(session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = select(game)
        result = await session.execute(query)
        data = [dict(row) for row in result.mappings().all()]
        return {"status": "success", "data": data, "details": None}
    except Exception as e:
        return {"status": "error", "data": None, "details": str(e)}


@router.get("/my/")
async def get_my_games(
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        query = select(game).where(game.c.creator == user.id)
        result = await session.execute(query)
        data = [dict(row) for row in result.mappings().all()]
        return {"status": "success", "data": data, "details": None}
    except Exception as e:
        return {"status": "error", "data": None, "details": str(e)}


@router.get("/{game_id}")
async def get_game(
    game_id: int,
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        current_game = await get_game_by_id(session, game_id)
        return {"status": "success", "data": current_game, "details": None}
    except Exception as e:
        return {"status": "error", "data": None, "details": str(e)}


@router.post("/")
async def add_game(
    game_create: GameCreate = Depends(GameCreate),
    current_user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        await add_game_to_team(
            session, game_create, game_create.team_1, current_user.id
        )
        await add_game_to_team(
            session, game_create, game_create.team_2, current_user.id
        )
        game_create = game_create.dict()
        game_create["creator"] = current_user.id
        stmt = insert(game).values(**game_create)
        created_game = await session.execute(stmt)
        await increment_games_organized(session, current_user.id)
        await session.commit()
        game_id = created_game.inserted_primary_key[0]
        await add_game_to_scheduler(game_id, session, game_create)
        await add_notification(game_id, session)

        send_ics_file.delay(
            current_user.username,
            current_user.email,
            "Добавьте предстоящую игру в календарь",
            game_create,
        )

        payment = {}
        if game_create["amount"] != 0:
            print(0)
            payment = await create_payment(
                game_create["amount"],
                game_create["name"],
                current_user.id,
                game_id,
                session,
            )
        return {"status": "success", "data": payment, "details": None}
    except Exception as e:
        return {"status": "error", "data": None, "details": str(e)}


@router.patch("/check_payment_by_id")
async def check_payment_patch(
    payment_id: str,
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    is_not_pending, payment = await check_payment(payment_id, session)
    if is_not_pending:
        return {
            "status": "success",
            "data": {
                "payment_status": payment["status"],
                "captured_at": payment["captured_at"],
            },
            "details": None,
        }
    else:
        return {
            "status": "success",
            "data": {
                "payment_status": payment["status"],
            },
            "details": None,
        }


@router.patch("/{game_id}")
async def update_game(
    game_id: int,
    game_create: GameCreate = Depends(GameCreate),
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        current_game = await get_game_by_id(session, game_id)
        if current_game["creator"] != user.id:
            raise Exception("You are not the creator of this game")
        game_create.datetime = game_create.datetime.replace(tzinfo=None)
        for key, value in game_create.dict().items():
            if (
                current_game[key] != value
                and key != "creator"
                and key != "team_1"
                and key != "team_2"
            ):
                current_game[key] = value
        stmt = update(game).where(game.c.id == game_id).values(**current_game)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "data": None, "details": None}
    except Exception as e:
        return {"status": "error", "data": None, "details": str(e)}


@router.patch("/{game_id}/change_status")
async def change_game_status(
    game_id: int,
    new_status: int,
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        current_game = await get_game_by_id(session, game_id)
        if current_game["creator"] != user.id:
            raise Exception("You are not the creator of this game")
        stmt = update(game).where(game.c.id == game_id).values(status=new_status)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "data": None, "details": None}
    except Exception as e:
        return {"status": "error", "data": None, "details": str(e)}


@router.delete("/{game_id}")
async def delete_game(
    game_id: int,
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        current_game = await get_game_by_id(session, game_id)
        if current_game["creator"] != user.id:
            raise Exception("You are not the creator of this game")
        stmt = delete(payment).where(payment.c.game_id == game_id)
        await session.execute(stmt)
        await session.commit()
        stmt = delete(game).where(game.c.id == game_id)
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "data": None, "details": None}
    except Exception as e:
        return {"status": "error", "data": None, "details": str(e)}
