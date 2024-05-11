from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.games.models import game
from src.games.schemas import GameCreate
from src.teams.models import team, empty_team_dict
from src.auth.models import User
from src.auth.config import current_verified_user

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


@router.get("/")
async def get_all_games(
        status: int = None,
        session: AsyncSession = Depends(get_async_session)
) -> dict:
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
async def add_game(
        game_create: GameCreate,
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        create_team_stmt = insert(team).values(empty_team_dict)
        if game_create.team_1 == 0 and game_create.team_2 == 0:
            team1_id = (await session.execute(create_team_stmt)).inserted_primary_key_rows[0][0]
            team2_id = (await session.execute(create_team_stmt)).inserted_primary_key_rows[0][0]
            game_create.team_1 = team1_id
            game_create.team_2 = team2_id
            await session.commit()
        elif game_create.team_1 == 0 and game_create.team_2 != 0:
            team1_id = (await session.execute(create_team_stmt)).inserted_primary_key_rows[0][0]
            game_create.team_1 = team1_id
            await session.commit()
        elif game_create.team_2 == 0 and game_create.team_1 != 0:
            team2_id = (await session.execute(create_team_stmt)).inserted_primary_key_rows[0][0]
            game_create.team_2 = team2_id
            await session.commit()
        game_create.datetime = game_create.datetime.replace(tzinfo=None)
        game_create.creator = user.id
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
