from fastapi import HTTPException, status


class JWTError(Exception):
    pass


class AuthException(HTTPException):
    status_code = 500
    detail = ""
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self) -> None:
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=self.headers,
        )


class AuthFailedException(AuthException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authenticate failed"


class AuthTokenExpiredException(AuthException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Expired token"
