from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

app = Flask(__name__)

REQUEST_COUNT = Counter('app_request_count', 'Total request count', ['method', 'endpoint'])

@app.route('/')
def home():
    REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
    return "Hello, Flask!"

@app.route('/api/items', methods=['GET'])
def list_items():
    REQUEST_COUNT.labels(method='GET', endpoint='/api/items').inc()
    items = [{"id":1,"name":"item1"}, {"id":2,"name":"item2"}]
    return jsonify(items)

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Intentional secret for lab detection
ADMIN_PASSWORD = "SuperSecretHardcodedPassword123"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
