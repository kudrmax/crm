class ContactNotFoundError(Exception):
    def __init__(self, name: str):
        self.name = name


class ContactAlreadyExistsError(Exception):
    def __init__(self, name: str):
        self.name = name


class InternalServerError(Exception):
    pass
