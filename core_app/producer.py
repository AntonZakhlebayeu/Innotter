import json
import pika
from core_app.settings import BROKER_URL


def publish(method, body):
    connection = pika.BlockingConnection(
        pika.URLParameters(BROKER_URL)
    )
    channel = connection.channel()
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="",
        routing_key="statistics",
        body=json.dumps(body),
        properties=properties,
    )
