from datetime import date

from sqlalchemy import and_, or_, select, func

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, engine
from app.hotels.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(Bookings.date_from >= date_from,
                             Bookings.date_from <= date_to
                             ),
                        and_(Bookings.date_from <= date_from,
                             Bookings.date_to > date_from
                             )
                        )
                    )
                ).cte("booked_rooms")

            rooms_left = select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id
                ).where(Rooms.id == room_id).group_by(
                    Rooms.quantity, booked_rooms.c.room_id
                )

            print(rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

            rooms_left = await session.execute(rooms_left)
            print(rooms_left.scalar())
