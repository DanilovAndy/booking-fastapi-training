from datetime import date, timedelta, datetime

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.bookings.router import add_booking, get_bookings
from app.hotels.rooms.router import get_rooms
from app.hotels.router import get_hotels_by_location_and_time, get_hotel_by_id

router = APIRouter(
    prefix="",
    tags=["Frontend"]
)

templates = Jinja2Templates(directory="app/templates")


def get_month_days(date: datetime = datetime.today()):
    counter = datetime(date.year, date.month, datetime.today().day, tzinfo=date.tzinfo)
    date_list = []
    for _ in range(90):
        date_list.append(
            {"date": counter.date(), "date_formatted": counter.strftime("%Y-%m-%d")}
        )
        counter += timedelta(days=1)
    return date_list


def format_number_thousand_separator(
        number: int,
        separator: str = " ",
):
    return f"{number:,}".replace(",", separator)


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/hotels/{location}", response_class=HTMLResponse)
async def get_hotels_page(
        request: Request,
        location: str,
        date_to: date,
        date_from: date,
        hotels=Depends(get_hotels_by_location_and_time),
):
    dates = get_month_days()
    if date_from > date_to:
        date_to, date_from = date_from, date_to
    # Автоматически ставим дату заезда позже текущей даты
    date_from = max(datetime.today().date(), date_from)
    # Автоматически ставим дату выезда не позже, чем через 180 дней
    date_to = min((datetime.today() + timedelta(days=180)).date(), date_to)
    return templates.TemplateResponse(
        "hotels_and_rooms/hotels.html",
        {
            "request": request,
            "hotels": hotels,
            "location": location,
            "date_to": date_to.strftime("%Y-%m-%d"),
            "date_from": date_from.strftime("%Y-%m-%d"),
            "dates": dates,
        },
    )


@router.get("/hotels/{hotel_id}/rooms", response_class=HTMLResponse)
async def get_rooms_page(
        request: Request,
        date_from: date,
        date_to: date,
        rooms=Depends(get_rooms),
        hotel=Depends(get_hotel_by_id),
):
    date_from_formatted = date_from.strftime("%d.%m.%Y")
    date_to_formatted = date_to.strftime("%d.%m.%Y")
    booking_length = (date_to - date_from).days
    return templates.TemplateResponse(
        "hotels_and_rooms/rooms.html",
        {
            "request": request,
            "hotel": hotel,
            "rooms": rooms,
            "date_from": date_from,
            "date_to": date_to,
            "booking_length": booking_length,
            "date_from_formatted": date_from_formatted,
            "date_to_formatted": date_to_formatted,
        },
    )


@router.post("/successful_booking", response_class=HTMLResponse)
async def get_successful_booking_page(
        request: Request,
        _=Depends(add_booking),
):
    return templates.TemplateResponse(
        "bookings/booking_successful.html", {"request": request}
    )


@router.get("/bookings", response_class=HTMLResponse)
async def get_bookings_page(
        request: Request,
        bookings=Depends(get_bookings),
):
    return templates.TemplateResponse(
        "bookings/bookings.html",
        {
            "request": request,
            "bookings": bookings,
            "format_number_thousand_separator": format_number_thousand_separator,
        },
    )
