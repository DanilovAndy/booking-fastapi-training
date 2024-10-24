from datetime import date, datetime, timedelta
from typing import List

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.exceptions import DateFromCannotBeAfterDateTo, CannotBookHotelForLongPeriod
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotelInfo

router = APIRouter(prefix="/api/hotels", tags=["Hotels"])


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
) -> List[SHotelInfo]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 90:
        raise CannotBookHotelForLongPeriod
    hotels = await HotelsDAO.find_all(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}", include_in_schema=True)
async def get_hotel_by_id(
        hotel_id: int,
):
    return await HotelsDAO.find_one_or_none(id=hotel_id)
