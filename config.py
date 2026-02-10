"""
Configuration module for the application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Application
    APP_NAME = os.getenv('APP_NAME', 'Sample Python GKE App')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    PORT = int(os.getenv('PORT', 8080))
    
    # GCP
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', '')
    GCP_REGION = os.getenv('GCP_REGION', 'us-central1')
    GKE_CLUSTER_NAME = os.getenv('GKE_CLUSTER_NAME', '')
    
    # Container
    CONTAINER_REGISTRY = os.getenv('CONTAINER_REGISTRY', 'gcr.io')
    IMAGE_NAME = os.getenv('IMAGE_NAME', 'sample-python-gke-app')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': ProductionConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'production')
    return config.get(env, config['default'])
