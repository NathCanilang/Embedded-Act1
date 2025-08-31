from flask import Flask, render_template, Response, redirect, url_for, request, jsonify
from database import Database
from dht11 import DHT11_Data, Sensor_Data
from buzzer import BuzzerController
app = Flask(__name__)

db = Database()
db.createTable()
dht11 = DHT11_Data()
buzzer = BuzzerController()

#---------------------------

#---------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_current_data')
def get_current_data():
    sensor_data = dht11.get_current_reading()
    if not sensor_data:
        return jsonify({"temperature": None, "humidity": None}), 200
    
    db.insert_data(sensor_data.temperature, sensor_data.humidity)
    
    return jsonify({
        "temperature": sensor_data.temperature,
        "humidity": sensor_data.humidity    })

@app.route('/get_data_from_db')
def get_data_from_db():
    row = db.fetch_latest()
    if row:
        reading = {
            "id": row[0],
            "temperature": row[1],
            "humidity": row[2],
            "timestamp": row[3]
        }
        return jsonify(reading)
    else:
        return jsonify({}), 200 #sucess muan if wala pang data

@app.route('/start_buzzer', methods=["POST"])
def start_buzzer():
    buzzer.start()
    return jsonify({"status": "buzzer started"})

@app.route('/stop_buzzer', methods=["POST"])
def stop_buzzer():
    buzzer.stop()
    return jsonify({"status": "buzzer stopped"})

if __name__ == '__main__':
    app.run()


