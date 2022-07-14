from microservice.database import (
    get_amount_of_likes,
    get_page_id,
    update_page_statistics,
)


async def update_likes_count(innotter_id: int, field):
    match field:
        case "like_created":
            await update_page_statistics(
                await get_page_id(innotter_id),
                data={"amount_of_likes": await get_amount_of_likes(innotter_id) + 1},
            )
        case "like_deleted":
            await update_page_statistics(
                await get_page_id(innotter_id),
                data={"amount_of_likes": await get_amount_of_likes(innotter_id) - 1},
            )
