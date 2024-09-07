import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.v1 import validator


class SLogRead(BaseModel):
    id: int
    contact_id: UUID
    datetime: dt.datetime
    log: str


class SLogCreate(BaseModel):
    contact_id: UUID
    log: str
