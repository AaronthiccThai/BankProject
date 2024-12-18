from flask import Flask, jsonify
import psycopg2
from psycopg2 import sql
from .routes import main_routes 

def create_app() -> Flask:    
    app = Flask(__name__)
    app.config
    
    # app.config['DATABASE_HOST'] = 'localhost'  
    # app.config['DATABASE_USER'] = 'admin'  
    # app.config['DATABASE_PASSWORD'] = 'admin'  
    # app.config['DATABASE_NAME'] = 'bank'    
    # app.config['PORT'] = '5432' 
    # try:
    #     conn = psycopg2.connect(
    #         host=app.config['DATABASE_HOST'],
    #         user=app.config['DATABASE_USER'],
    #         password=app.config['DATABASE_PASSWORD'],
    #         dbname=app.config['DATABASE_NAME']
    #     )
    # except ConnectionError as e:
    #     print(f"Database error connection: {e}")    
        
    app.register_blueprint(main_routes)  # Register the blueprint
    return app