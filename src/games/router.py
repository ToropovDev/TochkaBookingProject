from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
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
        query = select(game).where(game.c.id == game_id)
        result = await session.execute(query)
        current_game = dict(result.mappings().one())
        return {
            "status": "success",
            "data": current_game,
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
        game_create: GameCreate = Depends(GameCreate),
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        new_team = empty_team_dict
        new_team['creator'] = user.id
        create_team_stmt = insert(team).values(new_team)
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


@router.patch("/{game_id}")
async def update_game(
        game_id: int,
        game_create: GameCreate = Depends(GameCreate),
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        query = select(game).where(game.c.id == game_id)
        result = await session.execute(query)
        current_game = dict(result.mappings().one())
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
            "details": None
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "details": str(e)
        }


@router.patch("/{game_id}/change_status")
async def change_game_status(
        game_id: int,
        new_status: int,
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        query = select(game).where(game.c.id == game_id)
        result = await session.execute(query)
        current_game = dict(result.mappings().one())
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
        query = select(game).where(game.c.id == game_id)
        result = await session.execute(query)
        current_game = dict(result.mappings().one())
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
