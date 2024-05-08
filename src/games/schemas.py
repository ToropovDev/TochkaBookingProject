from datetime import datetime as dt
from pydantic import BaseModel


class GameCreate(BaseModel):
    creator: int
    name: str
    place: str
    datetime: dt
    status: int
    team_1: int
    team_2: int


