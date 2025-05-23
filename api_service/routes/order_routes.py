from flask import Blueprint, jsonify, request
from services.order_service import OrderService

order_routes = Blueprint('order_routes', __name__)

@order_routes.route('/', methods=['POST'])
def place_order():
    """
    Place a new order
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            book_id:
              type: integer
            quantity:
              type: integer
    responses:
      201:
        description: Order placed successfully
        schema:
          properties:
            id:
              type: integer
            book_id:
              type: integer
            quantity:
              type: integer
            status:
              type: string
      400:
        description: Missing fields or insufficient stock
    """
    data = request.get_json()
    book_id = data.get('book_id')
    quantity = data.get('quantity')

    if not book_id or not quantity:
        return jsonify({'error': 'Missing book_id or quantity'}), 400
    
    if not book_id or not quantity or quantity <= 0:
      return jsonify({'error': 'Missing or invalid book_id or quantity'}), 400

    order = OrderService.place_order(book_id, quantity)
    if order:
        return jsonify(order.to_dict()), 201
    else:
        return jsonify({'error': 'Book not available or insufficient stock'}), 400

@order_routes.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """
    Get order status by order ID
    ---
    parameters:
      - name: order_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Order details
        schema:
          properties:
            id:
              type: integer
            book_id:
              type: integer
            quantity:
              type: integer
            status:
              type: string
      404:
        description: Order not found
    """
    order = OrderService.get_order_by_id(order_id)
    if order:
        return jsonify(order.to_dict()), 200
    return jsonify({'error': 'Order not found'}), 404
