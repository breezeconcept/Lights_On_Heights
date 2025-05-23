# api_service/seed.py

from models.db import db 
from models.book import Book
from models.order import Order
from app import app  # This gives access to the initialized app + db

def seed_data():
    with app.app_context():
        # Drop existing tables and recreate (use cautiously!)
        db.drop_all()
        db.create_all()

        # Add books
        books = [
            Book(title="The Pragmatic Programmer", author="Andrew Hunt", price=45.00, stock=10),
            Book(title="Clean Code", author="Robert C. Martin", price=40.00, stock=5),
            Book(title="Python Crash Course", author="Eric Matthes", price=38.00, stock=8),
        ]
        db.session.add_all(books)
        db.session.commit()

        # Add one order for testing
        order = Order(book_id=books[0].id, quantity=2, total_price=90.00)
        db.session.add(order)
        db.session.commit()

        print("✅ Seeded database with sample books and one order.")

if __name__ == "__main__":
    seed_data()
