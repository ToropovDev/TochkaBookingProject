from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.games.models import game
from src.games.schemas import GameCreate

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


@router.get("/")
async def get_all_games(status: int = None, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(game).where(game.columns.status == status) if status else select(game)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all(),
            "details": None
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "details": str(e)
        }


@router.post("/")
async def add_game(game_create: GameCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        game_create.datetime = game_create.datetime.replace(tzinfo=None)
        stmt = insert(game).values(**game_create.dict())
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

