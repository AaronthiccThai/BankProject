
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
main_routes = Blueprint('main_routes', __name__)


@main_routes.route('/', methods=['GET'])
def example():
    return jsonify({"status HOLY POGGERS": "ok"}), 200    
