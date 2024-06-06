from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database import get_async_session
from backend.src.games.models import game
from backend.src.games.schemas import GameCreate
from backend.src.games.handlers import get_game_by_id, add_game_to_team, increment_games_organized
from backend.src.scheduler.delayed_update_count import add_game_to_scheduler
from backend.src.scheduler.notification import add_notification
from backend.src.auth.models import User
from backend.src.auth.config import current_verified_user
from backend.src.payments.payments import create_payment

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
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "details": str(e)
        }


@router.get("/{game_id}")
async def get_game(
        game_id: int,
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        current_game = await get_game_by_id(session, game_id)
        return {
            "status": "success",
            "data": current_game,
            "details": None
        }
    except Exception as e:
        return {"status": "error", "data": None, "details": str(e)}


@router.post("/")
async def add_game(
        game_create: GameCreate = Depends(GameCreate),
        current_user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        await add_game_to_team(session, game_create, game_create.team_1, current_user.id)
        await add_game_to_team(session, game_create, game_create.team_2, current_user.id)
        game_create = game_create.dict()
        game_create["creator"] = current_user.id
        stmt = insert(game).values(**game_create)
        created_game = await session.execute(stmt)
        await increment_games_organized(session, current_user.id)
        await session.commit()
        game_id = created_game.inserted_primary_key[0]
        await add_game_to_scheduler(game_id, session, game_create)
        await add_notification(game_id, session)

        payment = {}
        if game_create["amount"] != 0:
            payment = create_payment(game_create["amount"], game_create["name"])

        return {
            "status": "success",
            "data": payment,
            "details": None
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "details": str(e)
        }


@router.get("/{game_id}/check_payment")
async def get_check_payment(
        game_id: int,
        payment_id: str,
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    ...


@router.patch("/{game_id}")
async def update_game(
        game_id: int, game_create: GameCreate = Depends(GameCreate),
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        current_game = await get_game_by_id(session, game_id)
        if current_game['creator'] != user.id:
            raise Exception("You are not the creator of this game")
        game_create.datetime = game_create.datetime.replace(tzinfo=None)
        for key, value in game_create.dict().items():
            if (current_game[key] != value
                    and key != "creator"
                    and key != "team_1"
                    and key != "team_2"):
                current_game[key] = value
        stmt = update(game).where(game.c.id == game_id).values(**current_game)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": None}
    except Exception as e:
        return {"status": "error",
                "data": None,
                "details": str(e)}


@router.patch("/{game_id}/change_status")
async def change_game_status(
        game_id: int,
        new_status: int,
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        current_game = await get_game_by_id(session, game_id)
        if current_game['creator'] != user.id:
            raise Exception("You are not the creator of this game")
        stmt = update(game).where(game.c.id == game_id).values(status=new_status)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": None
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "details": str(e)
        }


@router.delete("/{game_id}")
async def delete_game(
        game_id: int,
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        current_game = await get_game_by_id(session, game_id)
        if current_game['creator'] != user.id:
            raise Exception("You are not the creator of this game")
        stmt = delete(game).where(game.c.id == game_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": None
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "details": str(e)
        }
