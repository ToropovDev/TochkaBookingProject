from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column
from src.teams.models import team

metadata = MetaData()

game_status = Table(
    'game_status',
    metadata,
    Column("code", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False),
)

game = Table(
    "game",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("place", String, nullable=False),
    Column("datetime", TIMESTAMP, nullable=False),
    Column("status", Integer, ForeignKey(game_status.c.code)),
    Column("team_1", Integer, ForeignKey(team.c.id)),
    Column("team_2", Integer, ForeignKey(team.c.id)),
)
