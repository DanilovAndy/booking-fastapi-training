from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query, status

from app.exceptions import RoomCannotBeBooked
from app.hotels.dao import HotelsDAO

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/{location}")
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
):
    if date_from > date_to:
        raise RoomCannotBeBooked
    if (date_to - date_from).days > 31:
        raise RoomCannotBeBooked
    hotels = await HotelsDAO.find_all(location, date_from, date_to)
    return hotels
