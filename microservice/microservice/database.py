import os
from pathlib import Path

import motor.motor_asyncio
from bson.objectid import ObjectId
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
MONGO_DETAILS = os.getenv("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.page_statistics
page_statistics_collection = database.get_collection("page_statistics_collection")


async def get_page_id(innotter_id: int):
    page_statistics = await page_statistics_collection.find_one({"id": innotter_id})
    if page_statistics:
        return page_statistics_helper(page_statistics).get("id")
    return None


async def get_amount_of_likes(innotter_id: int):
    page_statistics = await page_statistics_collection.find_one({"id": innotter_id})
    if page_statistics:
        return page_statistics_helper(page_statistics).get("amount_of_likes")
    return None


async def get_amount_of_posts(innotter_id: int):
    page_statistics = await page_statistics_collection.find_one({"id": innotter_id})
    if page_statistics:
        return page_statistics_helper(page_statistics).get("amount_of_posts")
    return None


async def get_amount_of_followers(innotter_id: int):
    page_statistics = await page_statistics_collection.find_one({"id": innotter_id})
    if page_statistics:
        return page_statistics_helper(page_statistics).get("amount_of_followers")
    return None


def page_statistics_helper(page_statistics) -> dict:
    return {
        "id": str(page_statistics["_id"]),
        "name": page_statistics["name"],
        "uuid": page_statistics["uuid"],
        "description": page_statistics["description"],
        "amount_of_posts": page_statistics["amount_of_posts"],
        "amount_of_likes": page_statistics["amount_of_likes"],
        "amount_of_followers": page_statistics["amount_of_followers"],
    }


async def retrieve_pages_statistics():
    list_page_statistics = []
    async for page_statistics in page_statistics_collection.find():
        list_page_statistics.append(page_statistics_helper(page_statistics))
    return list_page_statistics


async def add_page_statistics(page_statistics_data: dict) -> dict:
    page_statistics = await page_statistics_collection.insert_one(page_statistics_data)
    new_page_statistics = await page_statistics_collection.find_one(
        {"_id": page_statistics.inserted_id}
    )
    return page_statistics_helper(new_page_statistics)


async def retrieve_page_statistics(id: str) -> dict:
    page_statistics = await page_statistics_collection.find_one({"_id": ObjectId(id)})
    if page_statistics:
        return page_statistics_helper(page_statistics)


async def update_page_statistics(id: str, data: dict):
    if len(data) < 1:
        return False
    page_statistics = await page_statistics_collection.find_one({"_id": ObjectId(id)})
    if page_statistics:
        updated_page_statistic = await page_statistics_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_page_statistic:
            return True
        return False


async def delete_page_statistics(id: str):
    page_statistics = await page_statistics_collection.find_one({"_id": ObjectId(id)})
    if page_statistics:
        await page_statistics_collection.delete_one({"_id": ObjectId(id)})
        return True
