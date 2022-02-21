from flask import Blueprint, request, jsonify
from helpers.verify_token import token_required
from helpers.tokens import decrypt_token
from database_controler import mysql
from datetime import datetime
from helpers.database_querys import get_id_account

transaction_routes = Blueprint('transaction_routes', __name__)

@transaction_routes.route('/add-transaction', methods=['POST'])
@token_required
def add_transaction():
    set_data = request.get_json()
    date_transaction = datetime.now().strftime("%Y-%m-%d")
    account_in = get_id_account(set_data["account_in"])
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call make_transaction(%s, %s, %s, %s, %s)',
                               (
                                   set_data["description"],
                                   set_data["account_out"],
                                   account_in,
                                   set_data["ammount"],
                                   date_transaction
                               ))
        connection.commit()
        response = jsonify({
            "message":"your transaction is successfully added"
        })
        response.status_code=200
        return response
    except Exception as e:
        response = jsonify({
            "message":"sorry an error ocurred",
            "error":str(e)
        })
        response.status_code=500
        return response

@transaction_routes.route('/get-transactions/<int:id>', methods=['GET'])
@token_required
def get_transactions(id):
    try:
        connection = mysql.connect()
        database_query = connection.cursor()
        database_query.execute('call get_transactions_information(%s)',
                               (id))
        transactions_information = database_query.fetchall()
        connection.commit()
        if(len(transactions_information)>0):
            response = jsonify({
                "message":"this is data of your transactions",
                "data":transactions_information
            })
            response.status_code=200
            return response
        else:
            response = jsonify({
                "message":"sorry you dont make a transaction"
            })
            response.status_code=200
            return response
    except Exception as e:
        response = jsonify({
            "message":"sorry an error ocurred",
            "error":str(e)
        })
        response.status_code=500
        print(str(e))
        return response


