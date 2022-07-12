from microservice.database import (
    get_amount_of_followers,
    get_page_id,
    update_page_statistics,
)


async def update_followers_count(innotter_id: int, field):
    match field:
        case "follower_added":
            await update_page_statistics(
                await get_page_id(innotter_id),
                data={
                    "amount_of_followers": await get_amount_of_followers(innotter_id) + 1
                },
            )
        case "follower_deleted":
            await update_page_statistics(
                await get_page_id(innotter_id),
                data={
                    "amount_of_followers": await get_amount_of_followers(innotter_id) - 1
                },
            )
