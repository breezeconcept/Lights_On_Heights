from .db import db
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, default='processing')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "quantity": self.quantity,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
