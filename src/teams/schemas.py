from pydantic import BaseModel


class TeamCreate(BaseModel):
    creator: int = 0
    opposite: None | int = None
    outside_1: None | int = None
    outside_2: None | int = None
    setter: None | int = None
    middle_1: None | int = None
    middle_2: None | int = None
    libero: None | int = None
