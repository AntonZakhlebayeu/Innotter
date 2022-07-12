import json

from microservice.database import (
    add_page_statistics,
    delete_page_statistics,
    get_page_id,
    update_page_statistics,
)
from microservice.models.page_statistics import (
    PageStatisticsSchema,
    UpdatePageStatisticsModel,
)


async def page_statistics_data(content_type: str, page_statistics: str):
    match content_type:
        case "page_created":
            page_statistics = PageStatisticsSchema.parse_raw(page_statistics).dict()
            await add_page_statistics(page_statistics)
        case "page_updated":
            updated_page_statistics = UpdatePageStatisticsModel.parse_raw(
                page_statistics
            ).dict()
            await update_page_statistics(
                await get_page_id(updated_page_statistics.get("id")),
                updated_page_statistics,
            )
        case "page_deleted":
            await delete_page_statistics(
                await get_page_id(int(json.loads(page_statistics).get("pk")))
            )
