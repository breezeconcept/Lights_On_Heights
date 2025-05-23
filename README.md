# 📚 Bookstore Microservices Project

This project is a microservices-based architecture for an **online bookstore**. It comprises four main backend services:

- `api_service` - The central gateway to interact with users
- `ai_service` - Summarizes books using AI (OpenAI/Gemini)
- `order_service` - Handles placing and processing orders
- `websocket_service` - Sends real-time notifications to users about order status updates

Each service is containerized using Docker and communicates via HTTP and RabbitMQ.

---

## 📦 Services Overview

### 1. 🛡️ `api_service`

Acts as the **API Gateway**.

- Handles user requests for:
  - Listing books
  - Viewing book details
  - Submitting summaries
  - Placing orders
- Delegates tasks to appropriate microservices

**Runs on**: `http://localhost:5000`

---

### 2. 🧠 `ai_service`

Responsible for **AI-powered book summarization**.

- Accepts a book's content or text
- Returns a concise summary using OpenAI or Gemini
- Only accessible via `api_service`

**Runs on**: `http://localhost:5001`

---

### 3. 🛒 `order_service`

Manages **order placement** and **inventory updates**.

- Validates stock before placing orders
- Sends order messages via RabbitMQ to update stock or trigger downstream actions

**Runs on**: `http://localhost:5002`

---

### 4. 🔔 `websocket_service`

Handles **real-time notifications** using WebSockets.

- Users connect with a `user_id`
- When an order is processed, `order_service` or others can notify the user via POST request

**Runs on**: `http://localhost:6000`

---

## 🧪 Testing the System

### ✅ Test Order Placement

```bash
curl -X POST http://localhost:5002/ \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1, "quantity": 2}'
````

Expected: `201 Created` response with the order details.

---

### ✅ Test AI Summary (via `api_service`)

```bash
curl -X POST http://localhost:5000/summary \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1, "content": "Book content goes here..."}'
```

Expected: JSON with a summary.

---

### ✅ Test WebSocket Notification

1. Connect with a WebSocket client like [wscat](https://github.com/websockets/wscat):

```bash
npx wscat -c ws://localhost:6000?user_id=123
```

2. Trigger notification:

```bash
curl -X POST http://localhost:6000/notify \
  -H "Content-Type: application/json" \
  -d '{"user_id": "123", "order_id": 1, "status": "processing"}'
```

Expected: WebSocket receives:

```json
{"order_id": 1, "status": "processing"}
```

---

## 🐇 RabbitMQ Integration

* `order_service` publishes to `order_queue`
* Inventory service or others (not included here) can consume this queue to reduce stock or perform further processing

---

## ⚙️ Running the Project

Make sure Docker and RabbitMQ are running. Each service should be started individually or via `docker-compose`.

```bash
# Example (for Flask apps)
cd api_service
flask run --host=0.0.0.0 --port=5000
```

---

## 🗂 Project Structure

```
bookstore_project/
├── api_service/
├── ai_service/
├── order_service/
├── websocket_service/
└── docker-compose.yml  
```

---

## 📬 Contact

For questions or contributions, reach out to Arinze Peter.

```
