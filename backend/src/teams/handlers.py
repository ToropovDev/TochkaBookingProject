from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database import get_async_session
from backend.src.games.models import game
from backend.src.teams.models import team


def position_handler(position: id) -> str:
    match position:
        case 0:
            return "opposite"
        case 1:
            return "outside_1"
        case 2:
            return "outside_2"
        case 3:
            return "setter"
        case 4:
            return "middle_1"
        case 5:
            return "middle_2"
        case 6:
            return "libero"
        case _:
            raise Exception("Invalid position")


async def is_team_fill(
        team_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> bool:
    try:
        query = select(team).where(team.c.id == team_id)
        result = await session.execute(query)
        data = dict(result.mappings().one())
        for key, value in data.items():
            if key != "id" and key != "creator":
                if value is None:
                    return False
        return True
    except Exception as e:
        print(e)
        return False


async def get_filled_games(
        team_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> list:
    try:
        query = select(game).where(game.c.id == team_id)
        result = await session.execute(query)
        games = []
        data = [dict(row) for row in result.mappings().all()]
        for row in data:
            team_1_id = row["team_1"]
            team_2_id = row["team_2"]
            if await is_team_fill(team_1_id, session) and await is_team_fill(team_2_id, session):
                games += [row["id"]]
        return games
    except Exception as e:
        print(e)
        return []


async def update_filled_games(
        team_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> None:
    filled_games: list[int] = await get_filled_games(team_id)
    for filled_game in filled_games:
        stmt = (update(game)
                .where(game.c.id == filled_game)
                .values(status=2))
        await session.execute(stmt)
        await session.commit()
