from pydantic import BaseModel


class TeamCreate(BaseModel):
    id: int
    opposite: int
    outside_1: int
    outside_2: int
    setter: int
    middle_1: int
    middle_2: int
    libero: int
