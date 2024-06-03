from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database import get_async_session
from backend.src.teams.schemas import TeamCreate
from backend.src.teams.models import team
from backend.src.teams.handlers import get_position_name, update_filled_games
from backend.src.auth.models import User
from backend.src.auth.config import current_verified_user

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


@router.get("/")
async def get_all_teams(session: AsyncSession = Depends(get_async_session)) -> dict:
    return await handle_get_all_teams(session)


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


@router.post("/")
async def add_team(
    team_create: TeamCreate = Depends(TeamCreate),
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await handle_add_team(team_create, user, session)


async def handle_add_team(team_create: TeamCreate, user: User, session: AsyncSession) -> dict:
    try:
        team_create.creator = user.id
        team_create = team_create.dict()
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


@router.patch("/{team_id}")
async def update_team(
    team_id: int,
    positions: TeamCreate,
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await handle_update_team(team_id, positions, user, session)


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


@router.delete("/{team_id}")
async def delete_team(
    team_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await handle_delete_team(team_id, session)


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


@router.post("/join/{team_id}")
async def join_team(
    team_id: int,
    position: int,
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await handle_join_team(team_id, position, user, session)


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
