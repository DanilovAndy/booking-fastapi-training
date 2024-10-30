from datetime import date

from pydantic import BaseModel


class SBookingDates(BaseModel):
    date_from: date
    date_to: date


class SHotelId(BaseModel):
    hotel_id: int


class SRoomId(BaseModel):
    room_id: int

