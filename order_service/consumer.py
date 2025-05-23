import pika
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api_service.models.book import Book, Base as BookBase
from api_service.models.order import Order, Base as OrderBase
from dotenv import load_dotenv
from pathlib import Path

# Step 1: Load .env from the root directory
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Step 2: Read from environment
DATABASE_URL = os.getenv("DATABASE_URL")
# print("DATABASE_URL =", DATABASE_URL)

# Step 3: Check if it's loaded
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Check your .env or dotenv loading logic.")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

# Setup database connection
engine = create_engine(DATABASE_URL)
BookBase.metadata.bind = engine
OrderBase.metadata.bind = engine
Session = sessionmaker(bind=engine)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()
channel.queue_declare(queue='order_queue', durable=True)

def callback(ch, method, properties, body):
    session = Session()
    try:
        data = json.loads(body)
        order = session.query(Order).get(data['order_id'])
        book = session.query(Book).get(data['book_id'])

        if order and book and book.stock >= data['quantity']:
            book.stock -= data['quantity']
            order.status = 'confirmed'
        else:
            order.status = 'failed'

        session.commit()
        print(f"Processed order {order.id}: {order.status}")
    except Exception as e:
        print("Error processing order:", str(e))
        session.rollback()
    finally:
        session.close()
        ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='order_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
