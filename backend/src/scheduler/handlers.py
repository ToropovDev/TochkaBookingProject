from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.games.models import game
from src.teams.models import team


async def get_game_teams(
        session: AsyncSession,
        game_id: int
) -> tuple[int, int]:
    game_query = select(game).where(game.c.id == game_id)
    result = await session.execute(game_query)
    current_game = dict(result.mappings().one())
    team_1_id: int = current_game['team_1']
    team_2_id: int = current_game['team_2']
    return team_1_id, team_2_id


async def get_team_players(
        session: AsyncSession,
        team_id: int
) -> list[int]:
    team_query = select(team).where(team.c.id == team_id)
    team_data = dict((await session.execute(team_query)).mappings().one())
    players = []
    for key, value in team_data.items():
        if key not in ['id', 'creator'] and value is not None:
            players.append(value)
    return players
