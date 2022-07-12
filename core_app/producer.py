import json

import pika


def publish(method, body):
    connection = pika.BlockingConnection(
        pika.URLParameters("amqp://guest:guest@rabbit:5672")
    )
    channel = connection.channel()
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange="",
        routing_key="statistics",
        body=json.dumps(body),
        properties=properties,
    )
