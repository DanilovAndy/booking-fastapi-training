from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.exceptions import DateFromCannotBeAfterDateTo, CannotBookHotelForLongPeriod
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotelInfo
from app.utility.dependencies.parameters import search_dates_normaliser_query_parameters

router = APIRouter(prefix="/api/hotels", tags=["Hotels"])


@router.get("")
@cache(expire=20)
async def get_hotels_by_location_and_time(
        location: str = '',
        normalised_date=Depends(search_dates_normaliser_query_parameters)
) -> List[SHotelInfo]:
    date_from = normalised_date['date_from']
    date_to = normalised_date['date_to']

    if (date_to - date_from).days > 90:
        raise CannotBookHotelForLongPeriod
    hotels = await HotelsDAO.find_all(date_from=date_from, date_to=date_to, location=location)
    return hotels


@router.get("/id/{hotel_id}", include_in_schema=True)
async def get_hotel_by_id(
        hotel_id: int,
):
    return await HotelsDAO.find_one_or_none(id=hotel_id)
