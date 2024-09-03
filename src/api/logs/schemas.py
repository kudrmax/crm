import datetime
from uuid import UUID

from pydantic import BaseModel


class SLogCreate(BaseModel):
    contact_id: UUID
    date: datetime.datetime
    text: str | None = None
