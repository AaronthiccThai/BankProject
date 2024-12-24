from flask import Blueprint, request, jsonify
import psycopg2
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta, timezone
import random
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

DB_HOST = 'localhost'
DB_USER = 'admin' 
DB_PASSWORD = 'admin'
DB_NAME = 'bankdb'

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
# Should be stored in env var but ceebs :D 
SECRET_KEY = "SKIBIDIRIZZ"

def verify_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None, "Token is missing or invalid"
    token = auth_header.split(" ")[1] 
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token, None
    except jwt.ExpiredSignatureError:
        return None, "Token has expired"
    except jwt.InvalidTokenError:
        return None, "Token is invalid"        
    
    
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
    
    cursor.execute("SELECT id FROM users WHERE email = %s;", (email,))
    new_user = cursor.fetchone()
        
    token = jwt.encode({
        'user_id': new_user[0],  # Assuming user[0] is the user ID
        'exp':  datetime.now(timezone.utc) + timedelta(hours=1)  # Token expiration time (1 hour)
    }, SECRET_KEY, algorithm='HS256')    
    

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "User registered successfully!", "token": token})    

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
    
    token = jwt.encode({
        'user_id': existing_user[0],  # Assuming user[0] is the user ID
        'exp':  datetime.now(timezone.utc) + timedelta(hours=1)  # Token expiration time (1 hour)
    }, SECRET_KEY, algorithm='HS256')    
        
    return jsonify({"status": "success", "message": "User logged in successfully!", "token": token})    


@bank_routes.route('/bank/addcard', methods=['POST'])
def add_card():
    decoded_token, error = verify_token()
    if not decoded_token:
        return jsonify({"status": "error", "message": "Token is missing!"}), 403
    
    user_id = decoded_token.get("user_id")
    if not user_id:
        return jsonify({"status": "error", "message": "Invalid token payload"}), 401            

    conn = get_db_connection()
    cursor = conn.cursor()   
    cursor.execute("SELECT name from users where id = %s", (user_id,))        
    name =  cursor.fetchone()
    if not name:
        cursor.close()
        conn.close()
        return jsonify({"status": "error", "message": "User not found"}), 404            
    name = name[0]     
  
    data = request.get_json()
    card_number = data.get("cardNumber")
    exp_date = data.get("expDate")
    cvv = data.get("cvv")
    if not card_number or not exp_date or not cvv:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    cursor.execute("""INSERT INTO BankCard (CardID, name, expdate, cvv, ownerID)
                    VALUES (%s, %s, %s, %s, %s)""", (card_number, name, exp_date, cvv, user_id))
      
    conn.commit()       
    cursor.close()   
    conn.close()
    return jsonify({"status": "success", "message": "Card added successfully!"}), 200
    
    
@bank_routes.route('/bank/getcard', methods=['GET'])
def get_cards():
    
    decoded_token, error = verify_token()
    if not decoded_token:
        return jsonify({"status": "error", "message": "Token is missing!"}), 403
    
    user_id = decoded_token.get("user_id")
    if not user_id:
        return jsonify({"status": "error", "message": "Invalid token payload"}), 401       
        
    conn = get_db_connection()
    cursor = conn.cursor()        
    
    cursor.execute("select b.CardID, b.balance from BankCard b where b.ownerID = %s", (user_id,))
    result = cursor.fetchall()
    print(result)
    cards = [{"card_id": row[0], "balance": row[1]} for row in result]
    cursor.close()
    conn.close()
    return jsonify({"status" : "success", "cards": cards}), 200

