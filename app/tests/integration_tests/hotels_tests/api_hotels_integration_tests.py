import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("location,date_from,date_to,status_code,detail",[
    ("Санкт-Петербург", "2024-01-01", "2023-01-01", 400, "Date from cannot be after date to"),
    ("Санкт-Петербург", "2024-01-01", "2024-04-01", 400, "Cannot book hotel for so long"),
    ("Санкт-Петербург", "2024-01-01", "2024-01-10", 200, None),
])
async def test_get_hotels_by_location_and_time(
        location,
        date_from,
        date_to,
        status_code,
        detail,
        ac: AsyncClient
):
    response = await ac.get(f"/hotels/{location}", params={"date_from": date_from,
                                                           "date_to": date_to})
    assert response.status_code == status_code
    if str(status_code).startswith("4"):
        assert response.json()["detail"] == detail

