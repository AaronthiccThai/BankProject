from flask import Blueprint, request, jsonify
import psycopg2
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta, timezone
import random
from decimal import Decimal

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
    
def get_user_id():
    decoded_token, error = verify_token()
    if not decoded_token:
        raise ValueError("Token is missing or invalid")
    
    user_id = decoded_token.get("user_id")
    if not user_id:
        raise ValueError("Invalid token payload")
    
    return user_id
    
    
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
        'user_id': new_user[0], 
        'exp':  datetime.now(timezone.utc) + timedelta(hours=5)
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
        'exp':  datetime.now(timezone.utc) + timedelta(hours=5)  # Token expiration time (1 hour)
    }, SECRET_KEY, algorithm='HS256')    
        
    return jsonify({"status": "success", "message": "User logged in successfully!", "token": token})    



@bank_routes.route('/bank/addcard', methods=['POST'])
def add_card():        
    user_id = get_user_id()
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
    

@bank_routes.route('/bank/removecard', methods=['DELETE'])
def remove_card():
    user_id = get_user_id()
    conn = get_db_connection()
    cursor = conn.cursor()    
    data = request.get_json()
    card_id = data.get('cardNumber')
    if not card_id:
        return jsonify({"status": "error", "message": "No card or user supplied"}), 400

    cursor.execute("Select balance from BankCard where CardID = %s", (card_id, ))
    result = cursor.fetchone()   
    if not result:
        return jsonify({"status": "error", "message": "No card found"}), 400     
    balance = result[0]
    if balance != 0:
        return jsonify({"status": "error", "message": "This account still has funds, cannot delete"}), 400
    # Transfer the fund to another card 
    cursor.execute("DELETE FROM BankCard WHERE CardID = %s", (card_id,))
    
    conn.commit()
    cursor.close()
    conn.close()   
    return jsonify({"status": "success", "message": "Successfully removed the card"}), 200

@bank_routes.route('/bank/getcard', methods=['GET'])
def get_cards():
    user_id = get_user_id()
    conn = get_db_connection()
    cursor = conn.cursor()        
    
    cursor.execute("select b.CardID, b.balance from BankCard b where b.ownerID = %s", (user_id,))
    result = cursor.fetchall()
    cards = [{"card_id": row[0], "balance": row[1]} for row in result]
    cursor.close()
    conn.close()
    return jsonify({"status" : "success", "cards": cards}), 200

@transaction_routes.route('/transaction/withdraw', methods=['POST'])
def withdraw():
    user_id = get_user_id()
    data =  request.get_json()
    amount = Decimal(data.get("amount"))
    card_id = data.get("targetCardID")
    if not amount or not card_id:
        return jsonify({"status": "error", "message": "No supplied amount or cardID"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance from BankCard where ownerID = %s and cardID = %s", (user_id, card_id))
    user_bal = cursor.fetchone()
    user_bal = user_bal[0]
    if user_bal < amount:
        return jsonify({"status": "error", "message": "Not enough funds"}), 400
    new_balance = user_bal - amount
    
    cursor.execute("UPDATE BankCard SET balance = %s WHERE ownerID = %s AND cardID = %s", (new_balance, user_id, card_id))
    cursor.execute("""INSERT INTO Transactions (source_CardID, target_CardID, transaction_type, amount)
                   VALUES (%s, NULL, 'Withdrawal', %s)""", (card_id, amount))    
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "Withdrawal successful"}), 200
    
@transaction_routes.route('/transaction/deposit', methods=['POST'])
def deposit():
    user_id = get_user_id()
    data = request.get_json()    
    amount = Decimal(data.get('amount'))
    target_card_id = data.get('targetCardID')
    print(amount, target_card_id)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance from BankCard where ownerID = %s and cardID = %s", (user_id, target_card_id))
    user_bal = cursor.fetchone()
    if not user_bal:
        return jsonify({"status": "error", "message": "Bank card does not exist"}), 400
    user_bal = user_bal[0]    
    new_balance = user_bal + amount
    
    cursor.execute("UPDATE BankCard SET balance = %s WHERE ownerID = %s AND cardID = %s", (new_balance, user_id, target_card_id))
    
    cursor.execute("""INSERT INTO Transactions (source_CardID, target_CardID, transaction_type, amount)
                   VALUES (NULL, %s, 'Deposit', %s)""", (target_card_id, amount))        
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "Deposit successful"}), 200
    
@transaction_routes.route('/transaction/transfer', methods=['POST'])
def transfer():
    user_id = get_user_id()
    data = request.get_json()
    amount = Decimal(data.get('amount'))
    target_card_id = data.get('transferCard')
    source_card_id = data.get('targetCardID')
    print(f"source card id: {source_card_id}, target card id: {target_card_id}")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance from BankCard where ownerID = %s and CardID = %s", (user_id, source_card_id))
    source_bal = cursor.fetchone()
    if not source_bal:
        return jsonify({"status": "error", "message": "Bank card does not exist"}), 400
    source_bal = source_bal[0]    
    
    if source_bal < amount:
        return jsonify({"status": "error", "message": "Insufficient funds"}), 400
    
    new_source_bal = source_bal - amount
    
    cursor.execute("SELECT balance from BankCard where cardID = %s", (target_card_id, ))
    target_bal = cursor.fetchone()
    if not target_bal:
        return jsonify({"status": "error", "message": "Bank card does not exist"}), 400
    target_bal = target_bal[0]
    
    new_target_bal = target_bal + amount
    
    cursor.execute("UPDATE BankCard SET balance = %s WHERE cardID = %s", (new_source_bal, source_card_id))
    cursor.execute("UPDATE BankCard SET balance = %s WHERE cardID = %s", (new_target_bal, target_card_id))
    
    cursor.execute("""INSERT INTO Transactions (source_CardID, target_CardID, transaction_type, amount)
                   VALUES (%s, %s, 'Transfer', %s)""", (source_card_id, target_card_id, amount))        
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "Successfully transferred funds"}), 200


@transaction_routes.route('/transaction/get_transactions', methods=['GET'])
def get_transactions():
    user_id = get_user_id()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT t.* 
        FROM Transactions t
        JOIN BankCard b ON t.source_CardID = b.CardID 
        WHERE b.ownerID = %s
        UNION 
        SELECT DISTINCT t.* 
        FROM Transactions t
        JOIN BankCard b ON t.target_CardID = b.CardID 
        WHERE b.ownerID = %s
    """, (user_id, user_id ))
    result = cursor.fetchall()
    print(result)
    transactions = [{"transaction": row[0], "source_card": row[1], "target_card": row[2], 
                    "transaction_type": row[3], "amount": row[4], "time": row[5]} for row in result]    
    cursor.close()
    conn.close()
    return jsonify({"status" : "success", "transactions": transactions}), 200    