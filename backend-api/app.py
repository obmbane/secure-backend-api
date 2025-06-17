from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Required for APIM testing

inventory = [
    {"id": 1, "name": "Laptop", "stock": 20},
    {"id": 2, "name": "Phone", "stock": 50},
]

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)