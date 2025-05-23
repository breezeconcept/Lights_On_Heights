from flask import Flask, request
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret!')
socketio = SocketIO(app, cors_allowed_origins="*")

clients = {}

@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    user_id = data.get('user_id')
    status = data.get('status')
    order_id = data.get('order_id')

    if user_id in clients:
        socketio.emit('order_status', {'order_id': order_id, 'status': status}, room=clients[user_id])
        return {'message': 'Notification sent'}, 200
    return {'message': 'User not connected'}, 404

@socketio.on('connect')
def handle_connect():
    user_id = request.args.get('user_id')
    if user_id:
        clients[user_id] = request.sid
        print(f"User {user_id} connected with session ID {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    for user_id, sid in list(clients.items()):
        if sid == request.sid:
            del clients[user_id]
            print(f"User {user_id} disconnected")
            break

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=7000)
