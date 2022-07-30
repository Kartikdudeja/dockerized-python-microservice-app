# The publisher will connect to RabbitMQ, send a single message, then exit.

# dependency
# pip install pika

import pika

import logging
logger = logging.getLogger(__name__)

import os, psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv
load_dotenv()

QUEUE_URL = os.getenv('QUEUE_URL')
QUEUE_NAME = os.getenv('QUEUE_NAME')
# MESSAGE='{"key": "some", "value": "info"}'

TEST_DATABASE_HOSTNAME = os.getenv('TEST_DATABASE_HOSTNAME')
DOCKER_DATABASE_HOSTNAME = os.getenv('DOCKER_DATABASE_HOSTNAME')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

FETCH_QUERY_DURATION_SECONDS = int(os.getenv('FETCH_QUERY_DURATION_SECONDS'))

def initializeQueue():
    # connect to a broker hosted on 'QUEUE_URL'
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=QUEUE_URL))
    channel = connection.channel()

    # declare/create a queue
    channel.queue_declare(queue=QUEUE_NAME)

    logger.info('Queue Initialized.')

    # close the connection
    connection.close()

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
    # print(f" [x] Sent '{MESSAGE}'")

    # close the connection
    connection.close()

def Publisher():

    logger.info('test function called, retreiving data from database')
    #conn = psycopg2.connect(host=TEST_DATABASE_HOSTNAME, database=DATABASE_NAME, user=DATABASE_USERNAME, password=DATABASE_PASSWORD, cursor_factory=RealDictCursor)
    conn = psycopg2.connect(host=DOCKER_DATABASE_HOSTNAME, database=DATABASE_NAME, user=DATABASE_USERNAME, password=DATABASE_PASSWORD, cursor_factory=RealDictCursor)

    # Open a cursor to perform database operations
    cursor = conn.cursor()

    # Query the database and obtain data
    SQL = f""" SELECT key, value FROM data WHERE created_at BETWEEN (NOW() - (INTERVAL '{FETCH_QUERY_DURATION_SECONDS}s')) AND NOW(); """
    cursor.execute(SQL)
    data = cursor.fetchall()
    conn.commit()

    # Close communication with the database
    cursor.close()
    conn.close()

    # MESSAGE='{"key": "some", "value": "info"}'

    for index in range(len(data)):
        key = data[index]['key']
        value = data[index]['value']
        MESSAGE = f'{{"key": {key}, "value": {value}}}'

        logger.info(f" Publishing the Message: '{MESSAGE}' to the queue.")
        producer(MESSAGE)

    return data