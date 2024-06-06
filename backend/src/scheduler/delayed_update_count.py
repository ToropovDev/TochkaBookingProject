from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.models import user
from backend.src.games.schemas import GameCreate
from backend.src.scheduler.handlers import get_game_teams, get_team_players
from backend.src.scheduler.scheduler import scheduler


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


async def add_game_to_scheduler(game_id: int, session: AsyncSession, game_create: dict) -> None:
    game_create["datetime"] = game_create["datetime"].replace(tzinfo=None)
    scheduler.add_job(update_games_played_count, 'date', args=[game_id, session], run_date=game_create["datetime"])
