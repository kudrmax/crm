import dataclasses
import datetime as dt


@dataclasses.dataclass
class MContact:
    id: int = None
    name: str = None
    phone: str = None
    telegram: str = None
    birthday: str = None
    created_at: dt.datetime = None
    updated_at: dt.datetime = None


@dataclasses.dataclass
class MContactCreate:
    name: str = None
    phone: str = None
    telegram: str = None
    birthday: dt.datetime = None


@dataclasses.dataclass
class MContactUpdate:
    name: str = None
    phone: str = None
    telegram: str = None
    birthday: dt.datetime = None
