# The publisher will connect to RabbitMQ, send a single message, then exit.

# dependency
# pip install pika

import pika

import logging
logger = logging.getLogger(__name__)

import os
from dotenv import load_dotenv

load_dotenv()

QUEUE_URL = os.getenv('QUEUE_URL')
QUEUE_NAME = os.getenv('QUEUE_NAME')
# MESSAGE='{"key": "some", "value": "info"}'

def producer(MESSAGE):
    # connect to a broker hosted on 'QUEUE_URL'
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=QUEUE_URL))
    channel = connection.channel()

    # declare/create a queue
    channel.queue_declare(queue=QUEUE_NAME)

    # publish message to the queue
    # exchange='' => use the default exchange
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=MESSAGE)
    logger.info(f"Message: '{MESSAGE}' published to the queue.")
    print(f" [x] Sent '{MESSAGE}'")

    # close the connection
    connection.close()