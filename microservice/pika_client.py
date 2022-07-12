import json
import os
import uuid
from pathlib import Path

import pika
from aio_pika import connect_robust
from dotenv import load_dotenv

from microservice.services.follower_service import update_followers_count
from microservice.services.like_service import update_likes_count
from microservice.services.page_service import page_statistics_data
from microservice.services.post_service import update_posts_count

BASE_DIR = Path(__file__).resolve()
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
RABBIT_URL = os.getenv("RABBIT_URL")
RABBIT_QUEUE_NAME = os.getenv("RABBIT_QUEUE_NAME")


class PikaClient:
    def __init__(self, process_callable):
        self.publish_queue_name = RABBIT_QUEUE_NAME
        self.connection = pika.BlockingConnection(pika.URLParameters(RABBIT_URL))
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable

    async def consume(self, loop):
        connection = await connect_robust(RABBIT_URL)
        channel = await connection.channel()
        queue = await channel.declare_queue(RABBIT_QUEUE_NAME)
        await queue.consume(self.process_incoming_message, no_ack=False)

        return connection

    async def process_incoming_message(self, message):

        await message.ack()
        body = message.body

        if body:
            self.process_callable(json.loads(body))

            match message.properties.content_type.split("_")[0]:
                case "like":
                    await update_likes_count(
                        innotter_id=int(body.decode("utf-8")),
                        field=message.properties.content_type,
                    ),
                case "page":
                    await page_statistics_data(
                        message.properties.content_type, body.decode("utf-8")
                    ),
                case "post":
                    await update_posts_count(
                        innotter_id=int(body.decode("utf-8")),
                        field=message.properties.content_type,
                    ),
                case "follower":
                    await update_followers_count(
                        innotter_id=int(body.decode("utf-8")),
                        field=message.properties.content_type,
                    ),

    def send_message(self, message: dict):
        self.channel.basic_publish(
            exchange="",
            routing_key=self.publish_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=str(uuid.uuid4())
            ),
            body=json.dumps(message),
        )
