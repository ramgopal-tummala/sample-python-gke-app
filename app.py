"""
Flask application for GKE deployment
"""
import os
from flask import Flask, jsonify, request, g
from datetime import datetime
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Load configuration from environment variables
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
app.config['APP_NAME'] = os.getenv('APP_NAME', 'Sample Python GKE App')
app.config['VERSION'] = os.getenv('APP_VERSION', '1.1.0')

# In-memory storage for demo purposes
users_db = []
request_count = 0

@app.before_request
def before_request():
    """Log and track request information"""
    global request_count
    request_count += 1
    g.start_time = time.time()
    logger.info(f"Request {request_count}: {request.method} {request.path}")

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

@app.after_request
def after_request(response):
    """Log response information"""
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        logger.info(f"Response: {response.status_code} - {elapsed:.3f}s")
    return response

@app.route('/api/info')
def api_info():
    """API information endpoint"""
    return jsonify({
        'app_name': app.config['APP_NAME'],
        'version': app.config['VERSION'],
        'environment': app.config['ENV'],
        'endpoints': [
            {'path': '/', 'methods': ['GET'], 'description': 'Home endpoint'},
            {'path': '/health', 'methods': ['GET'], 'description': 'Health check'},
            {'path': '/readiness', 'methods': ['GET'], 'description': 'Readiness check'},
            {'path': '/api/info', 'methods': ['GET'], 'description': 'API information'},
            {'path': '/api/metrics', 'methods': ['GET'], 'description': 'Application metrics'},
            {'path': '/api/data', 'methods': ['GET', 'POST'], 'description': 'Data operations'},
            {'path': '/api/users', 'methods': ['GET', 'POST'], 'description': 'User operations'},
            {'path': '/api/users/<id>', 'methods': ['GET', 'PUT', 'DELETE'], 'description': 'User by ID'}
        ],
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/metrics')
def metrics():
    """Application metrics endpoint"""
    return jsonify({
        'total_requests': request_count,
        'total_users': len(users_db),
        'uptime': 'N/A',  # Would need app start time to calculate
        'status': 'running',
        'timestamp': datetime.utcnow().isoformat()
    })

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

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    """Users endpoint - list all or create new user"""
    if request.method == 'POST':
        user_data = request.get_json()
        if not user_data or 'name' not in user_data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Name is required'
            }), 400
        
        user = {
            'id': len(users_db) + 1,
            'name': user_data['name'],
            'email': user_data.get('email', ''),
            'created_at': datetime.utcnow().isoformat()
        }
        users_db.append(user)
        logger.info(f"Created user: {user['id']}")
        return jsonify(user), 201
    else:
        return jsonify({
            'users': users_db,
            'total': len(users_db),
            'timestamp': datetime.utcnow().isoformat()
        })

@app.route('/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(user_id):
    """Get, update, or delete a specific user"""
    user = next((u for u in users_db if u['id'] == user_id), None)
    
    if not user:
        return jsonify({
            'error': 'Not Found',
            'message': f'User {user_id} not found'
        }), 404
    
    if request.method == 'GET':
        return jsonify(user)
    
    elif request.method == 'PUT':
        user_data = request.get_json()
        if 'name' in user_data:
            user['name'] = user_data['name']
        if 'email' in user_data:
            user['email'] = user_data['email']
        user['updated_at'] = datetime.utcnow().isoformat()
        logger.info(f"Updated user: {user_id}")
        return jsonify(user)
    
    elif request.method == 'DELETE':
        users_db.remove(user)
        logger.info(f"Deleted user: {user_id}")
        return jsonify({
            'message': f'User {user_id} deleted successfully'
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
