from typing import List

from fastapi import APIRouter, Depends

from src.api.stats.dao import DAOStats
from src.api.stats.schemas import SDayCount

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"],
)


@router.get("/count_of_interactions")
async def get_count_of_interactions(
        dao: DAOStats = Depends()
) -> List[SDayCount]:
    return await dao.get_stat_count_of_interactions()


@router.get("/count_of_interactions/{name}")
async def get_count_of_interactions(
        name: str,
        dao: DAOStats = Depends()
) -> List[SDayCount]:
    return await dao.get_stat_count_of_interactions(name)


@router.get("/days_count_since_last_interaction")
async def days_count_since_last_interaction(
        dao: DAOStats = Depends()
) -> List[SDayCount]:
    return await dao.get_days_count_since_last_interaction()


@router.get("/days_count_since_last_interaction/{name}")
async def days_count_since_last_interaction(
        name: str,
        dao: DAOStats = Depends()
) -> List[SDayCount]:
    return await dao.get_days_count_since_last_interaction(name)
