from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.teams.schemas import TeamCreate
from src.teams.models import team
from src.teams.handlers import position_handler
from src.auth.models import User
from src.auth.config import current_verified_user


router = APIRouter(
    prefix="/teams",
    tags=["teams"],
)


@router.get("/")
async def get_all_teams(session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = select(team)
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
async def add_team(team_create: TeamCreate,
                   user: User = Depends(current_verified_user),
                   session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        team_create.creator = user.id
        team_create = team_create.dict()
        for key in team_create.keys():
            if key == "id":
                continue
            if team_create[key] == 0:
                team_create[key] = None

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


@router.post("/join/{team_id}")
async def join_game(team_id: int,
                    position: int,
                    user: User = Depends(current_verified_user),
                    session: AsyncSession = Depends(get_async_session)):
    try:
        position = position_handler(position)
        stmt = update(team).where(team.c.id == team_id).values({position: user.id})
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
