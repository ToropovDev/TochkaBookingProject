from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, Table
from json import load

from backend.src.auth.models import role
from backend.src.database import get_async_session
from backend.src.games.models import game_status, game_level

router = APIRouter(
    prefix="/admin/fill_default",
    tags=["Fill default data"],
)


def get_default_data() -> dict:
    with open("default_data.json", "r", encoding="utf-8") as default_data_file:
        default_data = load(default_data_file)
    return default_data


async def check_table(table: Table, session: AsyncSession) -> bool:
    query = await session.execute(select(table).limit(1))
    return not query.fetchone()


async def check_tables(session: AsyncSession) -> (bool, bool, bool):
    async with session.begin():
        role_is_empty = await check_table(role, session)
        game_status_is_empty = await check_table(game_status, session)
        game_level_is_empty = await check_table(game_level, session)
    return role_is_empty, game_status_is_empty, game_level_is_empty


async def fill_table(table: Table, table_data: list, session: AsyncSession) -> None:
    for item in table_data:
        stmt = insert(table).values(**item)
        await session.execute(stmt)
    await session.commit()


@router.post("/")
async def fill_default_data(session: AsyncSession = Depends(get_async_session)) -> None:
    role_is_empty, game_status_is_empty, game_level_is_empty = await check_tables(session)

    default_data = get_default_data()
    role_data = default_data["role_data"]
    game_status_data = default_data["game_status_data"]
    game_level_data = default_data["game_level_data"]

    if role_is_empty:
        await fill_table(role, role_data, session)
    if game_status_is_empty:
        await fill_table(game_status, game_status_data, session)
    if game_level_is_empty:
        await fill_table(game_level, game_level_data, session)
