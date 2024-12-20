from flask import Blueprint, request, jsonify
import psycopg2
from flask_cors import CORS

"""
Endpoints:
    Auth - auth_routes:
        Register
        Login
    Card - bank_routes:
        Add/Create bank card
        View bank card
    Transactions - transaction_routes:
        Transfer money
        Withdraw money
        Deposit money
        View transactions

"""

# Example: Your database connection details (you'll want to put this in your config)
DB_HOST = 'localhost'
DB_USER = 'admin'  # Adjust as needed
DB_PASSWORD = 'admin'
DB_NAME = 'bankdb'

# Function to connect to PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )
    return conn
    
auth_routes = Blueprint('auth', __name__)
bank_routes = Blueprint('bank', __name__)
transaction_routes = Blueprint('transaction', __name__)
CORS(auth_routes)
CORS(bank_routes)
CORS(transaction_routes)

@auth_routes.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()    
    email = data.get('email')
    fullname = data.get('name')
    password = data.get('password')
    dob = data.get('dob')
    address = data.get('address')

    conn = get_db_connection()
    cursor = conn.cursor()    
    cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        return jsonify({"status": "error", "message": "User already exists!"}), 400    
    
    cursor.execute("INSERT INTO users (email, name, password, dob, address) VALUES (%s, %s, %s, %s, %s)", 
                   (email, fullname, password, dob, address))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "User registered successfully!"})    

@auth_routes.route('/auth/login', methods=['POST']) 
def login():
    data = request.get_json()    
    email = data.get('email')
    password = data.get('password')
    
    conn = get_db_connection()
    cursor = conn.cursor()    
    cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
    existing_user = cursor.fetchone()
    

    if existing_user is None:
        return jsonify({"status": "error", "message": "Invalid User"}), 400
    stored_pw = existing_user[3]
    if password != stored_pw:
        return jsonify({"status": "error", "message": "Password is incorrect"}), 400

    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "User logged in successfully!"})    
