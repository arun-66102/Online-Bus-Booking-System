from flask import Flask, render_template, request, send_file, jsonify
import qrcode
from io import BytesIO
import requests

app = Flask(__name__)

# Predefined fares between stops
fares = {
    ("Stop_A", "Stop_B"): 10,
    ("Stop_A", "Stop_C"): 25,
    ("Stop_A", "Stop_D"): 45,
    ("Stop_B", "Stop_C"): 15,
    ("Stop_A", "Stop_B"): 35,
    ("Stop_C", "Stop_D"): 20,
}

# UPI ID for receiving payments
YOUR_UPI_ID = "akalyas0503-1@okicici"

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    source = request.args.get('source')
    destination = request.args.get('destination')

    if not source or not destination or source == destination:
        return "Invalid source or destination", 400

    # Calculate total fare
    stops = ["Stop_A", "Stop_B", "Stop_C", "Stop_D"]
    source_index = stops.index(source)
    destination_index = stops.index(destination)

    if source_index > destination_index:
        return "Invalid route", 400

    total_fare = sum(fares[(stops[i], stops[i + 1])] for i in range(source_index, destination_index))

    # Generate UPI Payment Link
    upi_link = f"upi://pay?pa={YOUR_UPI_ID}&pn=BusTicket&am={total_fare}&cu=INR&tn=BusTicketPayment"

    # Generate QR Code
    qr = qrcode.make(upi_link)
    img_io = BytesIO()
    qr.save(img_io)
    img_io.seek(0)

    # Notify conductor app about pending payment
    requests.post("http://127.0.0.1:5002/payment_initiated", json={"route": f"{source}-{destination}", "amount": total_fare})

    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
