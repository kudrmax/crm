from pydantic import BaseModel


class SDayCount(BaseModel):
    name: str
    day_count: int
