from typing import List

from fastapi import APIRouter, Depends

from src.api.stats.dao import DAOStats
from src.api.stats.schemas import SDayCount

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"],
)

@router.get("/count_of_interactions")
async def get_stats(
        dao: DAOStats = Depends()
) -> List[SDayCount]:
    return await dao.get_stat_count_of_interasions()
