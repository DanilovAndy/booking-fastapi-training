from typing import List

from pydantic import BaseModel


class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
    image_id: int

    class Config:
        orm_mode = True


class SHotelInfo(SHotel):
    number_of_rooms_left: int

    class Config:
        orm_mode = True
