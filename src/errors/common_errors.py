from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Item not found"


class AlreadyExistsError(Exception):
    pass


class UnprocessableEntityError(Exception):
    pass


class InternalServerError(Exception):
    def __init__(
            self,
            details: str | None = None,
    ):
        self.status_code = 500
        self.details = details


class UnknownError(Exception):
    def __init__(
            self,
            status_code: int | None = None,
            details: str | None = None,
    ):
        self.status_code = status_code
        self.details = details
