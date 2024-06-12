from datetime import datetime as dt
from pydantic import BaseModel


class GameCreate(BaseModel):
    name: str
    place: str
    datetime: dt = dt.utcnow()
    status: int = 0
    level: int = 0
    team_1: int = 0
    team_2: int = 0
    amount: int = 0
