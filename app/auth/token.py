import uuid
import jwt

from datetime import timedelta, datetime, timezone
from typing import Optional

from fastapi import Response

from app.auth.dao import BlackListTokenDAO
from app.auth.exceptions import JWTError, AuthFailedException
from app.config import settings
from app.auth.schemas import TokenPair, JwtTokenSchema
from app.users.models import Users

REFRESH_COOKIE_NAME = "refresh"
SUB = "sub"
EXP = "exp"
IAT = "iat"
JTI = "jti"


def _get_utc_now():
    return datetime.now(timezone.utc)


def _create_access_token(payload: dict, minutes: Optional[int] = None) -> JwtTokenSchema:
    expire = _get_utc_now() + timedelta(
        minutes=minutes or settings.ACCESS_TOKEN_EXPIRES_MINUTES
    )

    payload[EXP] = expire

    token = JwtTokenSchema(
        token=jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM),
        payload=payload,
        expire=expire,
    )

    return token


def _create_refresh_token(payload: dict) -> JwtTokenSchema:
    expire = _get_utc_now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_MINUTES)

    payload[EXP] = expire

    token = JwtTokenSchema(
        token=jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM),
        expire=expire,
        payload=payload,
    )

    return token


def create_token_pair(user: Users) -> TokenPair:
    payload = {SUB: str(user.id), JTI: str(uuid.uuid4()), IAT: _get_utc_now()}

    return TokenPair(
        access=_create_access_token(payload={**payload}),
        refresh=_create_refresh_token(payload={**payload}),
    )


async def decode_access_token(token: str):
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        black_list_token = await BlackListTokenDAO.find_one_or_none(id=payload[JTI])
        if black_list_token:
            raise JWTError("Token is blacklisted")
    except JWTError:
        raise AuthFailedException()

    return payload


def refresh_token_state(token: str):
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError as ex:
        print(str(ex)) #FIXME
        raise AuthFailedException()

    return {"token": _create_access_token(payload=payload).token}


def mail_token(user: Users):
    """Return 2 hour lifetime access_token"""
    payload = {SUB: str(user.id), JTI: str(uuid.uuid4()), IAT: _get_utc_now()}
    return _create_access_token(payload=payload, minutes=2 * 60).token


def add_refresh_token_cookie(response: Response, token: str):
    exp = _get_utc_now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_MINUTES)
    exp.replace(tzinfo=timezone.utc)

    response.set_cookie(
        key="refresh",
        value=token,
        expires=int(exp.timestamp()),
        httponly=True,
    )
