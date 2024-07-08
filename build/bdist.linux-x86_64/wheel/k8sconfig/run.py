from app import app  # Import the initialized Quart application
from quart import request
from prometheus_client import Counter, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
import time

# Create Prometheus metrics to track request counts and latencies.
REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Counter('request_latency_seconds', 'Request latency', ['method', 'endpoint'])

@app.before_request
async def before_request():
    request.start_time = time.time()

@app.after_request
async def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.method, request.path).inc(request_latency)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route('/')
async def hello():
    return 'Hello'

@app.route('/metrics')
async def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

def main():
    app.run(host='127.0.0.1', port=5000)

if __name__ == '__main__':
    main()  # Start the server



