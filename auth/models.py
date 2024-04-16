from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey, Table, Column, JSON, Boolean
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from datetime import datetime

from database import metadata, Base

role = Table(
    "role",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(20), nullable=False),
    Column("permissions", JSON, nullable=True),
)

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(50), nullable=False),
    Column("username", String(20), nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_on", TIMESTAMP, nullable=False, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey("role.c.id"), nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("is_superuser", Boolean, nullable=False, default=False),
    Column("is_verifier", Boolean, nullable=False, default=False),
)


class User(SQLAlchemyBaseUserTableUUID[int], Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)