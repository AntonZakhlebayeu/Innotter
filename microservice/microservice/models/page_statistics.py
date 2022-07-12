from typing import Optional

from pydantic import BaseModel, Field


class PageStatisticsSchema(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    uuid: str = Field(...)
    description: str = Field(...)
    amount_of_posts: int = 0
    amount_of_likes: int = 0
    amount_of_followers: int = 0

    class Config:
        schema_extra = {
            "example": {
                "id": 25,
                "name": "Test Page",
                "uuid": "new-page-uuid",
                "description": "description of the page",
                "amount_of_posts": 2,
                "amount_of_likes": 25,
                "amount_of_followers": 15,
            }
        }


class UpdatePageStatisticsModel(BaseModel):
    id: int
    name: Optional[str]
    uuid: Optional[str]
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "innotter_id": 25,
                "page_name": "Test Page",
                "uuid": "new-page-uuid",
                "description": "description of the page",
                "amount_of_posts": 2,
                "amount_of_likes": 25,
                "amount_of_followers": 15,
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
