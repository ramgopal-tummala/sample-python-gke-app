"""
Flask application for GKE deployment
"""
import os
from flask import Flask, jsonify, request
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load configuration from environment variables
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
app.config['APP_NAME'] = os.getenv('APP_NAME', 'Sample Python GKE App')
app.config['VERSION'] = os.getenv('APP_VERSION', '1.0.0')

@app.route('/')
def home():
    """Home endpoint"""
    return jsonify({
        'message': 'Welcome to Sample Python GKE App',
        'app_name': app.config['APP_NAME'],
        'version': app.config['VERSION'],
        'environment': app.config['ENV'],
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/readiness')
def readiness():
    """Readiness check endpoint for Kubernetes"""
    return jsonify({
        'status': 'ready',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/data', methods=['GET', 'POST'])
def data():
    """Sample API endpoint"""
    if request.method == 'POST':
        data = request.get_json()
        logger.info(f"Received data: {data}")
        return jsonify({
            'message': 'Data received successfully',
            'data': data,
            'timestamp': datetime.utcnow().isoformat()
        }), 201
    else:
        return jsonify({
            'message': 'Sample data endpoint',
            'method': 'GET',
            'timestamp': datetime.utcnow().isoformat()
        }), 200

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal error: {error}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
