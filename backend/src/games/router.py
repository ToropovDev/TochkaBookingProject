from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database import get_async_session
from backend.src.games.models import game
from backend.src.games.schemas import GameCreate
from backend.src.teams.models import team, empty_team_dict
from backend.src.auth.models import User, user
from backend.src.auth.config import current_verified_user
from backend.src.games.scheduler import scheduler, update_games_played_count

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


async def get_game_by_id(session: AsyncSession, game_id: int) -> dict:
    query = select(game).where(game.c.id == game_id)
    result = await session.execute(query)
    return dict(result.mappings().one())


async def create_team(session: AsyncSession, creator_id: int) -> int:
    new_team = empty_team_dict
    new_team['creator'] = creator_id
    create_team_stmt = insert(team).values(new_team)
    team_id = (await session.execute(create_team_stmt)).inserted_primary_key_rows[0][0]
    return team_id


async def add_game_to_team(session: AsyncSession, game_create: GameCreate, team_id: int) -> None:
    if team_id != 0:
        return
    team_id = await create_team(session, game_create.creator)
    if game_create.team_1 == 0:
        game_create.team_1 = team_id
    elif game_create.team_2 == 0:
        game_create.team_2 = team_id


async def increment_games_organized(session: AsyncSession, user_id: int) -> None:
    stmt = (update(user)
            .where(user.c.id == user_id)
            .values(games_organized=user.c.games_organized + 1))
    await session.execute(stmt)


async def add_game_to_scheduler(game_id: int, session: AsyncSession, game_create: GameCreate) -> None:
    game_create.datetime = game_create.datetime.replace(tzinfo=None)
    scheduler.add_job(update_games_played_count, 'date', args=[game_id, session], run_date=game_create.datetime)


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
        await add_game_to_team(session, game_create, game_create.team_1)
        await add_game_to_team(session, game_create, game_create.team_2)
        stmt = insert(game).values(**game_create.dict())
        created_game = await session.execute(stmt)
        await increment_games_organized(session, current_user.id)
        await session.commit()
        game_id = created_game.inserted_primary_key[0]
        await add_game_to_scheduler(game_id, session, game_create)
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
