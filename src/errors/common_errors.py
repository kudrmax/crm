class NotFoundError(Exception):
    pass


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
