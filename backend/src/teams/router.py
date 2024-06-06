from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database import get_async_session
from backend.src.teams.schemas import TeamCreate
from backend.src.auth.models import User
from backend.src.auth.config import current_verified_user
from backend.src.teams.handlers import handle_get_all_teams, handle_add_team, handle_update_team, handle_delete_team, \
    handle_join_team

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


@router.get("/")
async def get_all_teams(session: AsyncSession = Depends(get_async_session)) -> dict:
    return await handle_get_all_teams(session)


@router.post("/")
async def add_team(
    team_create: TeamCreate = Depends(TeamCreate),
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await handle_add_team(team_create, user, session)


@router.patch("/{team_id}")
async def update_team(
    team_id: int,
    positions: TeamCreate,
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await handle_update_team(team_id, positions, user, session)


@router.delete("/{team_id}")
async def delete_team(
    team_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await handle_delete_team(team_id, session)


@router.post("/join/{team_id}")
async def join_team(
    team_id: int,
    position: int,
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session)
) -> dict:
    return await handle_join_team(team_id, position, user, session)


