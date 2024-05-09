from fastapi import FastAPI, Query, Depends
from typing import Union, Optional, Annotated
from datetime import date
from pydantic import BaseModel

app = FastAPI()


class HotelsSearchArgs:
    def __init__(self,
                 location: str,
                 date_from: date,
                 date_to: date,
                 has_spa: Annotated[bool, Query()] = None,
                 stars: Annotated[int, Query(ge=0, le=5)] = None
                 ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


@app.get("/hotels")
def get_hotels(
        search_args: HotelsSearchArgs = Depends()
) -> list[SHotel]:
    hotels = [
        {
            "address": "ул. Центральная",
            "name": "Московский",
            "stars": 4
        }
    ]
    return hotels


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
def add_booking(booking: SBooking):
    pass
