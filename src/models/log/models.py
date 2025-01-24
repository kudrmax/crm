import dataclasses
import datetime as dt


@dataclasses.dataclass
class MLog:
    id: int
    contact_id: str
    datetime: dt.datetime
    log: str
