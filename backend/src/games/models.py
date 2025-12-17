from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column

from src.auth.models import user
from src.teams.models import team

metadata = MetaData()

game_status = Table(
    "game_status",
    metadata,
    Column("code", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False),
)

game_level = Table(
    "game_level",
    metadata,
    Column("code", Integer, primary_key=True),
    Column("name", String, nullable=False),
)

game = Table(
    "game",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("creator", Integer, ForeignKey(user.c.id), nullable=False),
    Column("name", String, nullable=False),
    Column("place", String, nullable=False),
    Column("datetime", TIMESTAMP, nullable=False),
    Column("status", Integer, ForeignKey(game_status.c.code)),
    Column("level", Integer, ForeignKey(game_level.c.code)),
    Column("team_1", Integer, ForeignKey(team.c.id)),
    Column("team_2", Integer, ForeignKey(team.c.id)),
    Column("amount", Integer, nullable=False),
)
