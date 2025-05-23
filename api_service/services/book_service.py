from models.book import Book, db

class BookService:
    @staticmethod
    def get_all_books():
        return Book.query.all()

    @staticmethod
    def get_book_by_id(book_id):
        return Book.query.get(book_id)

    @staticmethod
    def reduce_stock(book_id, quantity):
        book = Book.query.get(book_id)
        if book and book.stock >= quantity:
            book.stock -= quantity
            db.session.commit()
            return True
        return False
