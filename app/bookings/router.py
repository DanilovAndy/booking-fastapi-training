from fastapi import APIRouter

from app.bookings.dao import BookingDAO


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("")
async def get_bookings():
    return await BookingDAO.find_all()
