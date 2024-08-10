from datetime import datetime

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", [
    (4, "2030-05-01", "2030-05-15", 3, 200),
    (4, "2030-05-02", "2030-05-16", 4, 200),
    (4, "2030-05-03", "2030-05-17", 5, 200),
    (4, "2030-05-04", "2030-05-18", 6, 200),
    (4, "2030-05-05", "2030-05-19", 7, 200),
    (4, "2030-05-06", "2030-05-20", 8, 200),
    (4, "2030-05-07", "2030-05-21", 9, 200),
    (4, "2030-05-08", "2030-05-22", 10, 200),
    (4, "2030-05-09", "2030-05-23", 10, 409),
    (4, "2030-05-10", "2030-05-24", 10, 409),
])
async def test_add_and_get_booking(
        room_id,
        date_from,
        date_to,
        status_code,
        booked_rooms,
        authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": datetime.strptime(date_from, "%Y-%m-%d"),
        "date_to": datetime.strptime(date_to, "%Y-%m-%d"),
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) == booked_rooms


async def test_get_and_delete_all_bookings(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/bookings")
    assert response.json()
    for booking in response.json():
        await authenticated_ac.delete(f"/bookings/{booking['id']}")
    response = await authenticated_ac.get("/bookings")
    assert not response.json()


@pytest.mark.parametrize("room_id,date_from,date_to", [
    (6, "2030-05-06", "2030-05-20")
])
async def test_booking_crud(room_id, date_from, date_to, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", params={
        "room_id": room_id,
        "date_from": datetime.strptime(date_from, "%Y-%m-%d"),
        "date_to": datetime.strptime(date_to, "%Y-%m-%d"),
    })
    booking_id = response.json()["id"]
    assert isinstance(booking_id, int)

    response = await authenticated_ac.get("/bookings")
    for booking in response.json():
        if booking['id'] == booking_id:
            break
    else:
        assert 0

    await authenticated_ac.delete(f"/bookings/{booking_id}")

    response = await authenticated_ac.get("/bookings")
    for booking in response.json():
        if booking['id'] == booking_id:
            assert 0
    else:
        assert 1



