from flask import Flask, request, jsonify
from datetime import datetime
import csv
import os

app = Flask(__name__)

# צור קובץ CSV אם לא קיים
csv_file = "trades_log.csv"
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Symbol", "Direction", "Entry", "Stop", "Take", "Status", "PnL", "Notes"])

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    print("📩 איתות חדש התקבל:")
    print(data)

    # קריאה לערכים
    symbol = data.get("symbol")
    direction = data.get("direction")
    entry = data.get("entry")
    stop = data.get("stop")
    take = data.get("take")
    time = data.get("time", datetime.now().isoformat())

    # שמירה לקובץ CSV
    with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([time, symbol, direction, entry, stop, take, "", "", ""])

    return jsonify({"status": "success", "message": "Signal saved"}), 200

if __name__ == "__main__":
    app.run(port=5001)
