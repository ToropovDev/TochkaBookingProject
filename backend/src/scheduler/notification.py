from datetime import timedelta, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.games.models import game
from backend.src.auth.models import user
from backend.src.scheduler.clr import send_email_notify
from backend.src.scheduler.scheduler import scheduler
from backend.src.scheduler.handlers import get_game_teams, get_team_players


async def get_game_info(
        game_id: int,
        session: AsyncSession
) -> dict:
    query = select(game).where(game.c.id == game_id)
    result = dict((await session.execute(query)).mappings().one())
    return result


async def get_user_info(
        user_id: int,
        session: AsyncSession
) -> dict:
    query = select(user).where(user.c.id == user_id)
    result = dict((await session.execute(query)).mappings().one())
    return result


def delay_notification(
    username: str,
    user_email: str,
    subject: str,
    game_name: str,
    game_place: str,
    game_datetime: datetime,
) -> None:
    game_datetime = game_datetime.strftime('%d.%m.%Y %H:%M')
    send_email_notify.delay(username, user_email, subject, game_name, game_place, game_datetime)


async def add_notification(
        game_id: int,
        session: AsyncSession
):
    game_info = await get_game_info(game_id, session)
    team_1_id, team_2_id = await get_game_teams(session, game_id)
    team_1_players = await get_team_players(session, team_1_id)
    team_2_players = await get_team_players(session, team_2_id)
    players = list(set(team_1_players + team_2_players))
    for player in players:
        player_info = await get_user_info(player, session)
        scheduler.add_job(
            delay_notification,
            'date',
            args=[
                player_info['username'],
                player_info['email'],
                "Напоминание о игре",
                game_info['name'],
                game_info['place'],
                game_info['datetime'],
            ],
            run_date=game_info['datetime'] - timedelta(hours=2),
        )
