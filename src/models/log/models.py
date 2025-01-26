import dataclasses
import datetime as dt


@dataclasses.dataclass
class MLog:
    id: int
    contact_id: int
    text: str
    datetime: dt.datetime


@dataclasses.dataclass
class MLogCreate:
    contact_id: int
    text: str
    datetime: dt.datetime


@dataclasses.dataclass
class MLogUpdate:
    contact_id: int
    text: str
    datetime: dt.datetime
