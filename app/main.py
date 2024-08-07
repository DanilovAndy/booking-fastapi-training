from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from typing import Annotated, AsyncIterator
from datetime import date
from pydantic import BaseModel

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from sqladmin import Admin

from app.admin_panel.views import UsersAdmin, BookingsAdmin, HotelsAdmin, RoomsAdmin
from app.admin_panel.auth import authentication_backend
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.pages.router import router as router_pages
from app.images.router import router as router_image


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_image)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


class HotelsSearchArgs:
    def __init__(self,
                 location: str,
                 date_from: date,
                 date_to: date,
                 has_spa: Annotated[bool, Query()] = None,
                 stars: Annotated[int, Query(ge=0, le=5)] = None
                 ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


@app.get("/hotels")
def get_hotels(
        search_args: HotelsSearchArgs = Depends()
) -> list[SHotel]:
    hotels = [
        {
            "address": "ул. Центральная",
            "name": "Московский",
            "stars": 4
        }
    ]
    return hotels
