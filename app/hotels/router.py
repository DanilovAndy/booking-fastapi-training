from datetime import date, datetime, timedelta
from typing import List

from fastapi import APIRouter, Query, Depends
from fastapi_cache.decorator import cache

from app.exceptions import DateFromCannotBeAfterDateTo, CannotBookHotelForLongPeriod
from app.hotels.dao import HotelsDAO
from app.hotels.schemas import SHotelInfo

router = APIRouter(prefix="/api/hotels", tags=["Hotels"])


def search_dates_normaliser(
        date_from: date = Query(..., description=f"For example, {datetime.today().date()}"),
        date_to: date = Query(..., description=f"For example, {(datetime.today() + timedelta(days=7)).date()}")

):
    today_date = datetime.today().date()

    # date_from before date_to
    if date_from > date_to:
        date_from, date_to = date_to, date_from

    # if 0-day interval selected
    if date_from == date_to:
        date_to += timedelta(days=1)

    # date_from in bounds of today and 89 days
    date_from = max(date_from, today_date)
    date_from = min(date_from, today_date + timedelta(days=88))

    # date_to in bounds of tomorrow and 90 days
    date_to = max(date_to, today_date + timedelta(days=1))
    date_to = min(date_to, today_date + timedelta(days=89))

    return {'date_from': date_from, 'date_to': date_to}


@router.get("")
@cache(expire=20)
async def get_hotels_by_location_and_time(
        location: str = '',
        normalised_date=Depends(search_dates_normaliser)
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
