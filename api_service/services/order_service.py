from models.order import Order, db
from models.book import Book
import pika
import json
import os

class OrderService:
    @staticmethod
    def place_order(book_id, quantity):
        book = Book.query.get(book_id)
        if not book or book.stock < quantity:
            return None

        total_price = book.price * quantity
        order = Order(book_id=book_id, quantity=quantity, total_price=total_price, status='processing')
        db.session.add(order)
        db.session.commit()

        # Send message to RabbitMQ to update inventory
        OrderService.send_order_to_queue(order)
        return order

    @staticmethod
    def get_order_by_id(order_id):
        return Order.query.get(order_id)

    @staticmethod
    def send_order_to_queue(order):
        message = {
            "order_id": order.id,
            "book_id": order.book_id,
            "quantity": order.quantity
        }
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST", "rabbitmq")))
        channel = connection.channel()
        channel.queue_declare(queue='order_queue', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='order_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
