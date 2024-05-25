from datetime import datetime as dt
from pydantic import BaseModel


class GameCreate(BaseModel):
    creator: int = 0
    name: str
    place: str
    datetime: dt = dt.utcnow()
    status: int = 0
    team_1: int = 0
    team_2: int = 0
