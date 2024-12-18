from flask import Blueprint, request, jsonify

"""
Endpoints:
    Auth - auth_routes:
        Register
        Login
    Card - bank_routes:
        Add bank card
        View bank card
    Transactions - bank_routes:
        Transfer money
        Withdraw money
        Deposit money
        View transactions

"""

from flask import Blueprint, jsonify
auth_routes = Blueprint('auth', __name__)

temp = {}
@auth_routes.route('/auth/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    print(password, username)
    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required!"}), 400

    if username in temp:
        return jsonify({"status": "error", "message": "User already exists!"}), 400    
    
    temp[username] = password
    return jsonify({"status": "success", "message": "User registered successfully!"})    

@auth_routes.route('/auth/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required!"}), 400
    
    if username not in temp:
        return jsonify({"status": "error", "message": "User is not registered in database!"}), 400
    
    if password != temp[username]:
        return jsonify({"status": "error", "message": "Password is incorrect"}), 400
    return jsonify({"status": "success", "message": "User logged in successfully!"})    
