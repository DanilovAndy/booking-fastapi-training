from app.bookings.dao import BookingDAO
from datetime import datetime


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(user_id=1,
                                       room_id=1,
                                       date_from=datetime.strptime("2024-07-15", "%Y-%m-%d"),
                                       date_to=datetime.strptime("2024-07-30", "%Y-%m-%d")
                                       )

    assert new_booking.user_id == 1
    assert new_booking.room_id == 1

    await BookingDAO.find_by_id(new_booking.id)

    assert new_booking is not None
