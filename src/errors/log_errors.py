from src.errors import NotFoundError


class LogError(Exception):
    pass


class LogNotFoundError(LogError, NotFoundError):
    pass
