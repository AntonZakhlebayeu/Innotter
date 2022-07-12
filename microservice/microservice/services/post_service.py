from microservice.database import (
    get_amount_of_posts,
    get_page_id,
    update_page_statistics,
)


async def update_posts_count(innotter_id: int, field):
    match field:
        case "post_created":
            await update_page_statistics(
                await get_page_id(innotter_id),
                data={"amount_of_posts": await get_amount_of_posts(innotter_id) + 1},
            )
        case "post_deleted":
            await update_page_statistics(
                await get_page_id(innotter_id),
                data={"amount_of_posts": await get_amount_of_posts(innotter_id) - 1},
            )
