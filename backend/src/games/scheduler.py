from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.models import user
from backend.src.games.models import game
from backend.src.teams.models import team

scheduler = AsyncIOScheduler()


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


async def update_player_games_played(session: AsyncSession, player_id: int) -> None:
    update_count_stmt = (
        update(user)
        .where(user.c.id == player_id)
        .values({"games_played": user.c.games_played + 1})
    )
    await session.execute(update_count_stmt)


async def update_games_played_count(
        game_id: int,
        session: AsyncSession
) -> None:
    team_1_id, team_2_id = await get_game_teams(session, game_id)
    team_1_players = await get_team_players(session, team_1_id)
    team_2_players = await get_team_players(session, team_2_id)
    all_players = set(team_1_players + team_2_players)
    for player_id in all_players:
        await update_player_games_played(session, player_id)
    await session.commit()
    await session.close()
