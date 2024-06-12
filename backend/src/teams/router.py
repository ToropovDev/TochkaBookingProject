from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.teams.schemas import TeamCreate
from src.auth.models import User
from src.auth.config import current_verified_user
from src.teams.handlers import handle_get_all_teams, handle_add_team, handle_update_team, handle_delete_team, \
    handle_join_team, handle_get_team, handle_get_my_teams

router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


@router.get("/")
async def get_all_teams(session: AsyncSession = Depends(get_async_session)) -> dict:
    return await handle_get_all_teams(session)


@router.get("/{team_id}")
async def get_team(
        team_id: int,
        user: User = Depends(current_verified_user),
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        current_game = await handle_get_team(team_id, session)
        return {
            "status": "success",
            "data": current_game,
            "details": None
        }
    except Exception as e:
        return {"status": "error", "data": None, "details": str(e)}


@router.get("/my/")
async def get_my_teams(user: User = Depends(current_verified_user),
                       session: AsyncSession = Depends(get_async_session)) -> dict:
    return await handle_get_my_teams(user.id, session)


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


