from fastapi import Depends
from sqlalchemy import select, update, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.models import User
from backend.src.database import get_async_session
from backend.src.games.models import game
from backend.src.teams.models import team
from backend.src.teams.schemas import TeamCreate


def get_position_name(position_id: int) -> str:
    positions = {
        0: "opposite",
        1: "outside_1",
        2: "outside_2",
        3: "setter",
        4: "middle_1",
        5: "middle_2",
        6: "libero"
    }
    if position_id in positions:
        return positions[position_id]
    else:
        raise Exception("Invalid position")


async def is_team_filled(
        team_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> bool:
    try:
        query = select(team).where(team.c.id == team_id)
        result = await session.execute(query)
        data = dict(result.mappings().one())
        return all(value is not None for key, value in data.items() if key != "id" and key != "creator")
    except Exception as e:
        print(e)
        return False


async def get_filled_games(
        team_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> list:
    try:
        query = select(game).where((game.c.team_1 == team_id) | (game.c.team_2 == team_id))
        result = await session.execute(query)
        games = []
        data = [dict(row) for row in result.mappings().all()]
        for row in data:
            if await is_team_filled(row["team_1"], session) and await is_team_filled(row["team_2"], session):
                games.append(row["id"])
        return games
    except Exception as e:
        print(e)
        return []


async def update_filled_games(
        team_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> None:
    filled_games = await get_filled_games(team_id)
    filled_game: int
    for filled_game in filled_games:
        stmt = (update(game).where(game.c.id == filled_game).values(status=2))
        await session.execute(stmt)
    await session.commit()


async def handle_get_all_teams(session: AsyncSession) -> dict:
    try:
        query = select(team)
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


async def handle_get_my_teams(creator_id: int, session: AsyncSession) -> dict:
    try:
        query = select(team).where(team.c.creator == creator_id)
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


async def handle_get_team(team_id: int, session: AsyncSession) -> dict:
    query = select(team).where(team.c.id == team_id)
    result = await session.execute(query)
    return dict(result.mappings().one())


async def handle_add_team(team_create: TeamCreate, user: User, session: AsyncSession) -> dict:
    try:
        team_create = team_create.dict()
        team_create["creator"] = user.id
        stmt = insert(team).values(**team_create)
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


async def handle_update_team(team_id: int, positions: TeamCreate, user: User, session: AsyncSession) -> dict:
    new_positions = {key: value for key, value in positions.dict().items() if value != 0}
    try:
        stmt = (update(team)
                .where(team.c.id == team_id)
                .where(team.c.creator == user.id)
                .values(**new_positions))
        await session.execute(stmt)
        await session.commit()
        await update_filled_games(team_id, session)
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


async def handle_delete_team(team_id: int, session: AsyncSession) -> dict:
    try:
        stmt = delete(team).where(team.c.id == team_id)
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


async def handle_join_team(team_id: int, position: int, user: User, session: AsyncSession) -> dict:
    try:
        position_name = get_position_name(position)
        stmt = (update(team)
                .where(team.c.id == team_id)
                .values({position_name: user.id}))
        await session.execute(stmt)
        await session.commit()
        await update_filled_games(team_id, session)
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
