class ContactNotFoundError(Exception):
    def __init__(self, name: str | None = None):
        self.name = name


class ContactAlreadyExistsError(Exception):
    def __init__(self, name: str | None = None):
        self.name = name


class LogNotFoundError(Exception):
    pass

class InternalServerError(Exception):
    pass
