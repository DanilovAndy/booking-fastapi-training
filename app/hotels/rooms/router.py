from datetime import date, datetime, timedelta

from fastapi import APIRouter, Query

from app.hotels.rooms.dao import RoomsDAO

router = APIRouter(prefix="/api/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"),
):
    rooms = await RoomsDAO.find_all(hotel_id, date_from, date_to)
    return rooms
