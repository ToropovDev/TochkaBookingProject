from sqlalchemy import MetaData, Integer, Table, Column, ForeignKey

from src.auth.models import user
metadata = MetaData()

team = Table(
    "team",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("opposite", Integer, ForeignKey(user.c.id), nullable=True),
    Column("outside_1", Integer, ForeignKey(user.c.id), nullable=True),
    Column("outside_2", Integer, ForeignKey(user.c.id), nullable=True),
    Column("setter", Integer, ForeignKey(user.c.id), nullable=True),
    Column("middle_1", Integer, ForeignKey(user.c.id), nullable=True),
    Column("middle_2", Integer, ForeignKey(user.c.id), nullable=True),
    Column("libero", Integer, ForeignKey(user.c.id), nullable=True),
)