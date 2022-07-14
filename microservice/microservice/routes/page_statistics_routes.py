from fastapi import APIRouter

from microservice.database import (
    get_page_id,
    retrieve_page_statistics,
    retrieve_pages_statistics,
)
from microservice.models.page_statistics import ErrorResponseModel, ResponseModel

router = APIRouter()


@router.get("/api/statistics/", response_description="Pages statistics retrieved")
async def get_pages_statistics_data():
    pages_statistics = await retrieve_pages_statistics()
    if pages_statistics:
        return ResponseModel(
            pages_statistics, "Pages statistics data retrieved successfully"
        )
    return ResponseModel(pages_statistics, "Empty list returned")


@router.get(
    "/api/statistics/{innotter_id}/",
    response_description="Page statistics data retrieved",
)
async def get_page_statistics_data(innotter_id: int):
    page_statistics = await retrieve_page_statistics(await get_page_id(innotter_id))
    if page_statistics:
        return ResponseModel(
            page_statistics, "Page statistics data retrieved successfully"
        )
    return ErrorResponseModel(
        "An error occurred.", 404, "Page statistics doesn't exist."
    )
