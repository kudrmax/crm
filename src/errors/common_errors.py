class UnprocessableEntityError(Exception):
    pass


class ContactNotFoundErr(Exception):
    pass


class NameNotFoundInState(Exception):
    pass


class ContactAlreadyExistsErr(Exception):
    pass


class ContactIdNotFoundErr(Exception):
    pass

# TODO убрать все лишние исключения
