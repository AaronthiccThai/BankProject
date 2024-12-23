from flask import Flask, jsonify
import psycopg2
from psycopg2 import sql
from .routes import auth_routes, bank_routes, transaction_routes
from flask_cors import CORS

def create_app() -> Flask:    
    app = Flask(__name__)
    CORS(app)
    app.config
    
    app.config['DATABASE_HOST'] = 'localhost'  
    app.config['DATABASE_USER'] = 'admin'  
    app.config['DATABASE_PASSWORD'] = 'admin'  
    app.config['DATABASE_NAME'] = 'bankdb'    
    app.config['PORT'] = '5432' 
    try:
        conn = psycopg2.connect(
            host=app.config['DATABASE_HOST'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            dbname=app.config['DATABASE_NAME']
        )
    except ConnectionError as e:
        print(f"Database error connection: {e}")    
        
    app.register_blueprint(auth_routes)  # Register the blueprint
    app.register_blueprint(bank_routes)
    return app