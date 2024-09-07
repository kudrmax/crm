from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


# class SLogData(BaseModel):
#     log_str: str
#     date: datetime.date


class SLogRead(BaseModel):
    id: int
    contact_id: UUID
    datetime: datetime
    log: str


class SLogCreate(BaseModel):
    contact_id: UUID
    datetime: datetime
    log: str

class SLogGetByDate(BaseModel):
    contact_id: UUID
    datetime: datetime