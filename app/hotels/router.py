from datetime import date, datetime, timedelta
from typing import List

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.exceptions import RoomCannotBeBooked
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotelInfo

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SHotelInfo]:
    if date_from > date_to:
        raise RoomCannotBeBooked
    if (date_to - date_from).days > 31:
        raise RoomCannotBeBooked
    hotels = await HotelsDAO.find_all(location, date_from, date_to)
    return hotels
