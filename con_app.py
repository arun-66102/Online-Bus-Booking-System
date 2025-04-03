from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Ticket counts
ticket_counts = {
    "Stop_A-Stop_B": 0,
    "Stop_A-Stop_C": 0,
    "Stop_A-Stop_D": 0,
    "Stop_B-Stop_C": 0,
    "Stop_B-Stop_D": 0,
    "Stop_C-Stop_D": 0
}

@app.route('/')
def home():
    return render_template('con_dash.html', ticket_counts=ticket_counts)

@app.route('/payment_initiated', methods=['POST'])
def payment_initiated():
    data = request.json
    route = data.get("route")
    
    if route in ticket_counts:
        ticket_counts[route] += 1
        socketio.emit('update_dashboard', ticket_counts)
        return jsonify({"status": "success", "message": "Payment registered!"})
    
    return jsonify({"status": "error", "message": "Invalid route!"})

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5002, debug=True)
