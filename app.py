from flask import Flask, render_template, Response, redirect, url_for, request, jsonify
from dht11 import DHT11_Data, Sensor_Data
app = Flask(__name__)

dht11 = DHT11_Data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_current_data')
def get_current_data():
    sensor_data = dht11.get_current_reading()   
    if not sensor_data:
        return jsonify({"error": "Sensor error"}), 400
    else:
        return jsonify({
            "temperature": sensor_data.temperature,
            "humidity": sensor_data.humidity})
    
if __name__ == '__main__':
    app.run()


