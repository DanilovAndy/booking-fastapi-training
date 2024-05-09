from fastapi import FastAPI, Query
from typing import Union, Optional, Annotated
from datetime import date

app = FastAPI()


@app.get("/hotels")
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        has_spa: Annotated[bool, Query()] = None,
        stars: Annotated[int, Query()] = None
):
    has_spa
    stars
    return "Отель"
