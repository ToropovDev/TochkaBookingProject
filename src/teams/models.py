from sqlalchemy import MetaData, Integer, Table, Column, ForeignKey

from src.auth.models import user
metadata = MetaData()

team = Table(
    "team",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("opposite", Integer, ForeignKey(user.c.id), nullable=True, default=None),
    Column("outside_1", Integer, ForeignKey(user.c.id), nullable=True, default=None),
    Column("outside_2", Integer, ForeignKey(user.c.id), nullable=True, default=None),
    Column("setter", Integer, ForeignKey(user.c.id), nullable=True, default=None),
    Column("middle_1", Integer, ForeignKey(user.c.id), nullable=True, default=None),
    Column("middle_2", Integer, ForeignKey(user.c.id), nullable=True, default=None),
    Column("libero", Integer, ForeignKey(user.c.id), nullable=True, default=None),
)

empty_team_dict = {"opposite": None,
                   "outside_1": None,
                   "outside_2": None,
                   "setter": None,
                   "middle_1": None,
                   "middle_2": None,
                   "libero": None}
