from datetime import date, datetime, timedelta

from fastapi import Query

from app.utility.dependencies.schemas import SBookingDates


def search_dates_normaliser_query_parameters(
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


def search_dates_normaliser_body_parameters(
        booking_dates: SBookingDates
):
    today_date = datetime.today().date()

    # date_from before date_to
    if booking_dates.date_from > booking_dates.date_to:
        booking_dates.date_from, booking_dates.date_to = booking_dates.date_to, booking_dates.date_from

    # if 0-day interval selected
    if booking_dates.date_from == booking_dates.date_to:
        booking_dates.date_to += timedelta(days=1)

    # date_from in bounds of today and 89 days
    booking_dates.date_from = max(booking_dates.date_from, today_date)
    booking_dates.date_from = min(booking_dates.date_from, today_date + timedelta(days=88))

    # date_to in bounds of tomorrow and 90 days
    booking_dates.date_to = max(booking_dates.date_to, today_date + timedelta(days=1))
    booking_dates.date_to = min(booking_dates.date_to, today_date + timedelta(days=89))

    return booking_dates

