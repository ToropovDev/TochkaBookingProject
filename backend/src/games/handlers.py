from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.auth.models import user
from backend.src.games.models import game
from backend.src.games.schemas import GameCreate
from backend.src.teams.models import empty_team_dict, team


async def get_game_by_id(session: AsyncSession, game_id: int) -> dict:
    query = select(game).where(game.c.id == game_id)
    result = await session.execute(query)
    return dict(result.mappings().one())


async def create_team(session: AsyncSession, creator_id: int) -> int:
    new_team = empty_team_dict
    new_team['creator'] = creator_id
    create_team_stmt = insert(team).values(new_team)
    team_id = (await session.execute(create_team_stmt)).inserted_primary_key_rows[0][0]
    return team_id


async def add_game_to_team(session: AsyncSession, game_create: GameCreate, team_id: int, game_creator: int) -> None:
    if team_id != 0:
        return
    team_id = await create_team(session, game_creator)
    if game_create.team_1 == 0:
        game_create.team_1 = team_id
    elif game_create.team_2 == 0:
        game_create.team_2 = team_id


async def increment_games_organized(session: AsyncSession, user_id: int) -> None:
    stmt = (update(user)
            .where(user.c.id == user_id)
            .values(games_organized=user.c.games_organized + 1))
    await session.execute(stmt)
