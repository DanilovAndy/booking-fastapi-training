from datetime import date

from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import TypeAdapter
from fastapi_versioning import version

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SNewBooking
from app.exceptions import RoomCannotBeBooked
from app.users.dependencies import get_cur_user
from app.users.models import Users
from app.tasks.tasks import send_booking_confirmation_email
from app.utility.dependencies.parameters import search_dates_normaliser_body_parameters
from app.utility.dependencies.schemas import SBookingDates, SRoomId

router = APIRouter(
    prefix="/api/bookings",
    tags=["Bookings"]
)


@router.get("")
# @version(1)
async def get_bookings(user: Users = Depends(get_cur_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("", status_code=201)
# @version(1)
async def add_booking(
        background_tasks: BackgroundTasks,
        # room_id: int, date_from: date, date_to: date,
        #booking_data: SNewBooking = Depends(search_dates_normaliser_body_parameters),
        room_id: SRoomId,
        booking_dates: SBookingDates = Depends(search_dates_normaliser_body_parameters),
        user: Users = Depends(get_cur_user)
):
    print(booking_dates)
    print(room_id)
    booking = await BookingDAO.add(user.id, room_id.room_id, booking_dates.date_from, booking_dates.date_to)
    if not booking:
        raise RoomCannotBeBooked

    s_new_booking_adapter = TypeAdapter(SNewBooking)
    email_data = s_new_booking_adapter.validate_python(booking.__dict__)
    send_booking_confirmation_email.delay(email_data.__dict__, user.email)
    return booking


@router.delete("", status_code=204)
# @version(1)
async def delete_booking(
        booking_id: int,
        user: Users = Depends(get_cur_user)
):

    await BookingDAO.delete(id=booking_id, user_id=user.id)
