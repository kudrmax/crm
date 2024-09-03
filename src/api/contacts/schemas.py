import datetime
from uuid import UUID

from pydantic import BaseModel


class SContactCreate(BaseModel):
    name: str


class SContactUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    telegram: str | None = None
    birthday: datetime.date | None = None
    area: str | None = None
