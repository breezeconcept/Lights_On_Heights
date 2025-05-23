from flask import Blueprint, jsonify, request
from services.book_service import BookService
import requests
import os

book_routes = Blueprint('book_routes', __name__)

@book_routes.route('/', methods=['GET'])
def get_books():
    """
    Get list of all books
    ---
    responses:
      200:
        description: A list of books
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              title:
                type: string
              author:
                type: string
              price:
                type: number
              stock:
                type: integer
    """
    books = BookService.get_all_books()
    return jsonify([book.to_dict() for book in books]), 200

@book_routes.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Get details of a specific book by ID
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Book details
        schema:
          properties:
            id:
              type: integer
            title:
              type: string
            author:
              type: string
            description:
              type: string
            price:
              type: number
            stock:
              type: integer
      404:
        description: Book not found
    """
    book = BookService.get_book_by_id(book_id)
    if book:
        return jsonify(book.to_dict()), 200
    return jsonify({'error': 'Book not found'}), 404

@book_routes.route('/<int:book_id>/summary', methods=['GET'])
def get_book_summary(book_id):
    """
    Get AI-generated summary for a book
    ---
    parameters:
      - name: book_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: AI-generated summary
        schema:
          properties:
            summary:
              type: string
      404:
        description: Book not found
      500:
        description: AI service failed
    """
    book = BookService.get_book_by_id(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    # Call the AI service to get summary
    try:
        ai_service_url = os.getenv("AI_SERVICE_URL", "http://192.168.40.5:8000/summary")
        response = requests.post(ai_service_url, json={"text": book.description})
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "AI service failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500