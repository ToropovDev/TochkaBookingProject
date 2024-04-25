from datetime import datetime

from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column, JSON, Boolean
from database import Base

metadata = MetaData()

game_status = Table(
    'game_status',
    metadata,
    Column("code", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False),
)

team = Table(
    "team",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("opposite", String, nullable=True),
    Column("outside_1", String, nullable=True),
    Column("outside_2", String, nullable=True),
    Column("setter", String, nullable=True),
    Column("middle_1", String, nullable=True),
    Column("middle_2", String, nullable=True),
    Column("libero", String, nullable=True),
)

game = Table(
    "game",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("place", String, nullable=False),
    Column("datetime", TIMESTAMP, nullable=False),
    Column("status", Integer, ForeignKey(game_status.c.code)),
    Column("team_1", Integer, ForeignKey(team.c.id)),
    Column("team_2", Integer, ForeignKey(team.c.id)),
)


