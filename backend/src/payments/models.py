from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column

from src.auth.models import user
from src.games.models import game

metadata = MetaData()

payment = Table(
    "payment",
    metadata,
    Column('id', String, primary_key=True),
    Column("status", String, nullable=False),
    Column("amount", String, nullable=False),
    Column("currency", String, nullable=False),
    Column("user_id", Integer, ForeignKey(user.c.id), nullable=False),
    Column("game_id", Integer, ForeignKey(game.c.id), nullable=False),
    Column("description", String, nullable=False),
    Column("created_at", TIMESTAMP, nullable=False),
    Column("captured_at", TIMESTAMP, nullable=True),
)
