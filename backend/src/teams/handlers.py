from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database import get_async_session
from backend.src.games.models import game
from backend.src.teams.models import team


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
