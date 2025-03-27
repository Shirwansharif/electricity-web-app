from flask import Flask, render_template, request, send_file, jsonify
import os
import io
import csv
import matplotlib.pyplot as plt
import datetime

app = Flask(__name__)

# Sample price slabs (same as in your desktop app)
price_slabs = [
    {"from": 1, "to": 450, "price": 18},
    {"from": 451, "to": 900, "price": 24},
    {"from": 901, "to": 1500, "price": 42},
    {"from": 1501, "to": 2100, "price": 72},
    {"from": 2101, "to": 3000, "price": 90},
    {"from": 3001, "to": 5000, "price": 180},
]

def calculate_kwh(watt, hours, quantity, days):
    return (watt * hours * quantity * days) / 1000

def calculate_cost(total_kwh):
    total_cost = 0
    remaining = total_kwh
    sorted_slabs = sorted(price_slabs, key=lambda x: x['from'])

    for slab in sorted_slabs:
        if remaining <= 0:
            break
        slab_range = slab['to'] - slab['from'] + 1
        used = min(remaining, slab_range)
        total_cost += used * slab['price']
        remaining -= used

    if remaining > 0:
        total_cost += remaining * sorted_slabs[-1]['price']

    return total_cost

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    devices = data.get('devices', [])
    total_kwh = 0
    device_data = []

    for dev in devices:
        try:
            name = dev['device']
            watt = float(dev['watt'])
            hours = float(dev['hours'])
            qty = int(dev['quantity'])
            days = int(dev['days'])
            kwh = calculate_kwh(watt, hours, qty, days)
            total_kwh += kwh
            device_data.append({"name": name, "kwh": kwh})
        except:
            continue

    total_cost = calculate_cost(total_kwh)
    return jsonify({
        "total_kwh": round(total_kwh, 2),
        "total_cost": round(total_cost, 2),
        "devices": device_data
    })

@app.route('/chart.png')
def chart():
    # Example data (should be dynamic)
    devices = [('TV', 120.5), ('Fridge', 220.1), ('AC', 350.7)]
    labels = [d[0] for d in devices]
    sizes = [d[1] for d in devices]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
