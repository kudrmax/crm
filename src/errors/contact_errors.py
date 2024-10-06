from src.errors import NotFoundError


class ContactError(Exception):
    def __init__(self, name: str | None = None):
        self.name = name


class ContactNotFoundError(ContactError, NotFoundError):
    pass


class ContactAlreadyExistsError(ContactError):
    pass
