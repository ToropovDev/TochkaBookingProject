from pydantic import BaseModel


class TeamCreate(BaseModel):
    opposite: None | int
    outside_1: None | int
    outside_2: None | int
    setter: None | int
    middle_1: None | int
    middle_2: None | int
    libero: None | int
