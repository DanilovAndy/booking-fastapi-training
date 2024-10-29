from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends

from app.hotels.rooms.dao import RoomsDAO
from app.hotels.router import search_dates_normaliser

router = APIRouter(prefix="/api/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        normalised_dates=Depends(search_dates_normaliser)
):
    date_from = normalised_dates['date_from']
    date_to = normalised_dates['date_to']
    rooms = await RoomsDAO.find_all(hotel_id, date_from, date_to)
    return rooms
