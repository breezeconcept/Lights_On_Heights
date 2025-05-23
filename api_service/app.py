# api_service/app.py
from flask import Flask
from flask_cors import CORS
from models.db import db
from models import book, order
from routes.book_routes import book_routes
from routes.order_routes import order_routes
from flasgger import Swagger
from dotenv import load_dotenv
from pathlib import Path
import os

# Step 1: Load .env from the root directory
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Step 2: Read from environment
DATABASE_URL = os.getenv("DATABASE_URL")
# print("DATABASE_URL =", DATABASE_URL)

# Step 3: Check if it's loaded
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Check your .env or dotenv loading logic.")

# Step 4: Initialize app
app = Flask(__name__)
CORS(app)
Swagger(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return "API is Running!"

# Register routes
app.register_blueprint(book_routes, url_prefix='/books')
app.register_blueprint(order_routes, url_prefix='/orders')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
