import asyncio

import uvicorn as uvicorn
from fastapi import FastAPI
from pika_client import PikaClient

from microservice.routes.page_statistics_routes import router as PageStatisticsRouter


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.log_incoming_message)

    @classmethod
    def log_incoming_message(cls, message: dict):
        print(message)


app = App()
app.include_router(PageStatisticsRouter, tags=["Pages"], prefix="")


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True, debug=True, workers=3)
