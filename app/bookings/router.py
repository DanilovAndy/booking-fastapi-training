from datetime import date

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter
from fastapi_versioning import version

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_cur_user
from app.users.models import Users
from app.tasks.tasks import send_booking_confirmation_email

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("")
# @version(1)
async def get_bookings(user: Users = Depends(get_cur_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
# @version(1)
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: Users = Depends(get_cur_user)
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked

    s_new_booking_adapter = TypeAdapter(SNewBooking)
    email_data = s_new_booking_adapter.validate_python(booking.__dict__)
    send_booking_confirmation_email.delay(email_data.__dict__, user.email)
    return booking


@router.delete("/{booking_id}")
# @version(1)
async def delete_booking(
        booking_id: int,
        user: Users = Depends(get_cur_user)
):
    await BookingDAO.delete(id=booking_id, user_id=user.id)
